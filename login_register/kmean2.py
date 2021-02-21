from csv import writer
import joblib
import pandas as pd
from sklearn.metrics import cluster
# interests=["data mining AI image processing classification regression"]
# kmean=joblib.load('Kmodel.pkl')
# tfidf=joblib.load('TFIDF.pkl')
# vect=tfidf.transform(interests)
# predict=kmean.predict(vect)
# print(predict)

clusters=joblib.load('clusters.pkl')
data1=clusters[0]

for a,d2 in clusters.items():
        l1=[]
        l2=[]
        unions=data1+d2
        for w in unions: 
                if w in data1: l1.append(1)
                else: l1.append(0) 
                if w in d2: l2.append(1) 
                else: l2.append(0) 
        c = 0
        for i in range(len(unions)): 
                c+= l1[i]*l2[i] 
        cosine = c / float((sum(l1)*sum(l2))**0.5) 
        if(cosine>0.4):
                data1=list(set(data1)|set(d2))
                print("similarity: ", cosine,a) 
print(data1)
# df=pd.read_csv('indexedReport.csv')
# for index, row in df.iterrows():
#     d=row.to_dict()
#     print(index)


# data = pd.read_csv('indexedReport.csv') 
# totalInstances=len(data)+1
# ls=[totalInstances, 'x','x','x',0]
# with open('indexedReport.csv','a',newline='') as reports:
#         writer_obj=writer(reports)
#         writer_obj.writerow(ls)
        