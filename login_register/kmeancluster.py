import numpy  as np
import pandas as pd
from sklearn.cluster import KMeans
import re,joblib
from sklearn.decomposition import PCA
import nltk.corpus
from nltk.stem import WordNetLemmatizer
from unidecode                        import unidecode
from nltk.tokenize                    import word_tokenize
from nltk                             import SnowballStemmer
from sklearn.feature_extraction.text  import TfidfVectorizer
from sklearn.preprocessing            import normalize
from sklearn import cluster
from sklearn.metrics                  import silhouette_samples, silhouette_score
import matplotlib.pyplot  as plt
import seaborn as sns
import matplotlib.cm      as cm
data = pd.read_csv('reports.csv', encoding='utf-8')
data.columns = map(str.lower, data.columns)
corpus = data['data'].tolist()

def removeWords(listOfTokens, listOfWords):
    return [token for token in listOfTokens if token not in listOfWords]
def applyStemming(listOfTokens, stemmer):
    return [stemmer.stem(token) for token in listOfTokens]
def lemmentizer(listOfTokens,lemm):
    return [lemm.lemmatize(token, pos="v") for token in listOfTokens]


def twoLetters(listOfTokens):
    twoLetterWord = []
    for token in listOfTokens:
        if len(token) <= 2 or len(token) >= 21:
            twoLetterWord.append(token)
    return twoLetterWord

def processCorpus(corpus, language):   
    stopwords = nltk.corpus.stopwords.words(language)
    for document in corpus:
        index = corpus.index(document)
        corpus[index] = str(corpus[index]).replace(u'\ufffd', '8')   # Replaces the ASCII '�' symbol with '8'
        corpus[index] = corpus[index].replace(',', '')          # Removes commas
        corpus[index] = corpus[index].rstrip('\n')              # Removes line breaks
        corpus[index] = corpus[index].casefold()                # Makes all letters lowercase
        
        corpus[index] = re.sub('\W_',' ', corpus[index])        # removes specials characters and leaves only words
        corpus[index] = re.sub("\S*\d\S*"," ", corpus[index])   # removes numbers and words concatenated with numbers IE h4ck3r. Removes road names such as BR-381.
        corpus[index] = re.sub("\S*@\S*\s?"," ", corpus[index]) # removes emails and mentions (words with @)
        corpus[index] = re.sub(r'http\S+', '', corpus[index])   # removes URLs with http
        corpus[index] = re.sub(r'www\S+', '', corpus[index])    # removes URLs with www

        listOfTokens = word_tokenize(corpus[index])
        # listOfTokens = lemmentizer(listOfTokens, lemmen)
        twoLetterWord = twoLetters(listOfTokens)
        listOfTokens = removeWords(listOfTokens, stopwords)
        listOfTokens = removeWords(listOfTokens, twoLetterWord)
        # listOfTokens = applyStemming(listOfTokens, param_stemmer)
        

        corpus[index]   = " ".join(listOfTokens)
        corpus[index] = unidecode(corpus[index])
    return corpus

language = 'english'
corpus = processCorpus(corpus, language)
# print(corpus[18][0:460])
vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, ngram_range=(1,3))
X = vectorizer.fit_transform(corpus)
tf_idf = pd.DataFrame(data = X.toarray(), columns=vectorizer.get_feature_names())

final_df = tf_idf

# print("{} rows".format(final_df.shape[0]))
final_df.T.nlargest(5, 0)
# print(final_df.T.nlargest(5, 0))

def run_KMeans(max_k, data):
    max_k += 1
    kmeans_results = dict()
    for k in range(2 , max_k):
        kmeans = cluster.KMeans(n_clusters = k
                               , init = 'k-means++'
                               , n_init = 10
                               , tol = 0.0001
                               , random_state = 1
                               , algorithm = 'full')
        kmeans_results.update( {k : kmeans.fit(data)} )
    
    return kmeans_results
def printAvg(avg_dict):
    for avg in sorted(avg_dict.keys(), reverse=True):
        print("Avg: {}\tK:{}".format(avg.round(4), avg_dict[avg]))
        
def plotSilhouette(df, n_clusters, kmeans_labels, silhouette_avg):
    fig, ax1 = plt.subplots(1)
    fig.set_size_inches(8, 6)
    ax1.set_xlim([-0.2, 1])
    ax1.set_ylim([0, len(df) + (n_clusters + 1) * 10])
    
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--") # The vertical line for average silhouette score of all the values
    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1])
    plt.title(("Silhouette analysis for K = %d" % n_clusters), fontsize=10, fontweight='bold')
    
    y_lower = 10
    sample_silhouette_values = silhouette_samples(df, kmeans_labels) # Compute the silhouette scores for each sample
    for i in range(n_clusters):
        ith_cluster_silhouette_values = sample_silhouette_values[kmeans_labels == i]
        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.nipy_spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper), 0, ith_cluster_silhouette_values, facecolor=color, edgecolor=color, alpha=0.7)

        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i)) # Label the silhouette plots with their cluster numbers at the middle
        y_lower = y_upper + 10  # Compute the new y_lower for next plot. 10 for the 0 samples
    plt.show()
    
        
def silhouette(kmeans_dict, df, plot=False):
    df = df.to_numpy()
    avg_dict = dict()
    for n_clusters, kmeans in kmeans_dict.items():      
        kmeans_labels = kmeans.predict(df)
        silhouette_avg = silhouette_score(df, kmeans_labels) # Average Score for all Samples
        avg_dict.update( {silhouette_avg : n_clusters} )
    
        if(plot): plotSilhouette(df, n_clusters, kmeans_labels, silhouette_avg)

k = 25
kmeans_results = run_KMeans(k, final_df)

# Plotting Silhouette Analysis
# silhouette(kmeans_results, final_df, plot=True)

def get_top_features_cluster(tf_idf_array, prediction, n_feats):
    labels = np.unique(prediction)
    dfs = []
    for label in labels:
        id_temp = np.where(prediction==label) # indices for each cluster
        x_means = np.mean(tf_idf_array[id_temp], axis = 0) # returns average score across cluster
        sorted_means = np.argsort(x_means)[::-1][:n_feats] # indices with top 20 scores
        features = vectorizer.get_feature_names()
        best_features = [(features[i], x_means[i]) for i in sorted_means]
        df = pd.DataFrame(best_features, columns = ['features', 'score'])
        dfs.append(df)
    return dfs

def plotWords(dfs, n_feats):
    plt.figure(figsize=(8, 4))
    cluster_data={}
    feature_data={}
    for i in range(0, len(dfs)):
        # plt.title(("Most Common Words in Cluster {}".format(i)), fontsize=10, fontweight='bold')
        # sns.barplot(x = 'score' , y = 'features', orient = 'h' , data = dfs[i][:n_feats])
        feature_data[i]=dfs[i][:n_feats].to_dict()
        cluster_data[i]=(dfs[i][:n_feats]['features'].tolist())
        # plt.show()
    joblib.dump(cluster_data,'clusters.pkl')
    joblib.dump(feature_data,'features.pkl')
    
best_result = 16
kmeans = kmeans_results.get(best_result)

final_df_array = final_df.to_numpy()
prediction = kmeans.predict(final_df)
n_feats = 20
dfs = get_top_features_cluster(final_df_array, prediction, n_feats)
plotWords(dfs, 15)

# Saving model
joblib.dump(kmeans,'Kmodel.pkl')
joblib.dump(vectorizer,"TFIDF.pkl")
labels = kmeans.labels_ 
data['label'] = labels


# saving the Labelled data
data.to_csv("indexedReport.csv",index=False)


# Plotting the data
# kmeans = KMeans(n_clusters = 5, init = 'k-means++', random_state = 0)
# kmean_indices = kmeans.fit_predict(X)
# tfidfnorm=normalize(X)
# tfidfarray=tfidfnorm.toarray()
# pca = PCA(n_components=2)
# scatter_plot_points = pca.fit_transform(tfidfarray)

# colors = ["r", "b", "c", "y", "m" ]

# x_axis = [o[0] for o in scatter_plot_points]
# y_axis = [o[1] for o in scatter_plot_points]
# fig, ax = plt.subplots(figsize=(20,10))

# ax.scatter(x_axis, y_axis, c=[colors[d] for d in kmean_indices])
# plt.show()


# prediction example
# predtfidf=vectorizer.transform(["kmeans text clustering using tfidf and cosine similarity"])
# print(kmeans.predict(predtfidf))

# ELbow method for k
# wcss = []
# for i in range(1, 26):
#     kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=1, random_state=0)
#     kmeans.fit(X)
#     wcss.append(kmeans.inertia_)
# plt.plot(range(1, 26), wcss)
# plt.title('Elbow Method')
# plt.xlabel('Number of clusters')
# plt.ylabel('WCSS')
# plt.show()