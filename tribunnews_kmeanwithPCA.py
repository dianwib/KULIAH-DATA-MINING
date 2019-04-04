
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np
import csv
from sklearn.cluster import KMeans
from sklearn.metrics import  silhouette_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

dataframe=pd.read_csv('baru.csv',encoding='utf-8',skiprows=0,index_col=0,sep=',')
df=dataframe.copy(deep=True)

pca=PCA(n_components=6)
principalcomponent=pca.fit_transform(df)
principaldf=pd.DataFrame(data=principalcomponent,columns=["PCA 1","PCA 2","PCA 3","PCA 4","PCA 5","PCA 6"])


print (principaldf)

new_csv=principaldf.to_csv('baru_withpca.csv')


dataframe = pd.read_csv('baru_withpca.csv', encoding='utf-8', skiprows=0, index_col=0, sep=',')

df = dataframe.copy(deep=True)

banyak_cluster = list(range(2, 149))
print ("Kmeans kluster dari 2 to 149: ", banyak_cluster)

temp=[]
for n_cluster in banyak_cluster:
    clusterer = KMeans(n_clusters=n_cluster)
    preds = clusterer.fit_predict((df))

    centers = clusterer.cluster_centers_
    score = silhouette_score(df, preds, metric='euclidean')
    temp.append(score)

    print ("Untuk kluster={},silhoute score :{} ".format(n_cluster, repr(score)))
    print(preds)

print ("kluster terbaik")
print ("kluster ke > "+str(temp.index(max(temp))+2)+" >silhout> "+str(max(temp)))

