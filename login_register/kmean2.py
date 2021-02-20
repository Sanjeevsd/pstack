import joblib
import pandas as pd
interests=["data mining AI image processing classification regression"]
kmean=joblib.load('Kmodel.pkl')
tfidf=joblib.load('TFIDF.pkl')
vect=tfidf.transform(interests)
predict=kmean.predict(vect)
print(predict)

# clusters=joblib.load('clusters.pkl')
# print(clusters[0])

# df=pd.read_csv('indexedReport.csv')
# for index, row in df.iterrows():
#     d=row.to_dict()
#     print(index)
