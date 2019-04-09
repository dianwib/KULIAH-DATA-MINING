
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np
import csv
from sklearn.cluster import KMeans
from sklearn.metrics import  silhouette_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


banyak_pca = list(range(3, 149))
dict_temp={}
for n_pca in banyak_pca:

    dataframe = pd.read_csv('baru_tfidv.csv', encoding='utf-8', skiprows=0, index_col=0, sep=',')
    df = dataframe.copy(deep=True)

    pca = PCA(n_components=n_pca)
    principalcomponent = pca.fit_transform(df)
    kolom=[]
    for i in range(n_pca):
        kolom.append("PCA"+str(i+1))

    principaldf = pd.DataFrame(data=principalcomponent, columns=kolom)

    #print (principaldf)

    new_csv = principaldf.to_csv('baru_withpca.csv')

    dataframe = pd.read_csv('baru_withpca.csv', encoding='utf-8', skiprows=0, index_col=0, sep=',')

    df = dataframe.copy(deep=True)

    banyak_cluster = list(range(2, 150))

    temp = []
    temp2=[]
    for n_cluster in banyak_cluster:
        clusterer = KMeans(n_clusters=n_cluster)
        preds = clusterer.fit_predict((df))

        centers = clusterer.cluster_centers_
        score = silhouette_score(df, preds, metric='euclidean')
        temp.append(score)

        # print ("Untuk kluster={},silhoute score :{} ".format(n_cluster, repr(score)))
        # print(preds)

    temp_besar=str(max(temp))
    temp_index_besar = str(temp.index(max(temp)) + 2)

    dict_temp[n_pca]={"kluster":temp_index_besar,"silhout":temp_besar}
    print("PCA > ",n_pca," terbaik pada ",dict_temp[n_pca])



baru=pd.DataFrame(columns=['n_PCA','kluster','silhout'])
baru['n_PCA']=banyak_pca
baru['kluster']=banyak_cluster
baru['silhout']=temp

print (baru.head())

baru.to_csv('klustering_allPCA.csv')
