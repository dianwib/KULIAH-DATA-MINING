import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

data = pd.read_csv('baru.csv', index_col=0, encoding="utf-8", sep=';')
# print(data.info())
# print(data.head())


import numpy as np
import csv
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

filename = "baru.csv"

path_dir = ".\\"
dataframe = pd.read_csv('baru.csv', encoding='utf-8', skiprows=1, index_col=0, sep=',')

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

