import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

dataframe = pd.read_csv('baru_tfidv.csv', encoding='utf-8', skiprows=0, index_col=0, sep=',')

df = dataframe.copy(deep=True)

banyak_cluster = list(range(2, 10))
print ("Kmeans kluster dari 2 to 149: ", banyak_cluster)

temp=[]
temp_pred=[]
for n_cluster in banyak_cluster:
    clusterer = KMeans(n_clusters=n_cluster)
    preds = clusterer.fit_predict((df))

    centers = clusterer.cluster_centers_
    score = silhouette_score(df, preds, metric='euclidean')
    temp.append(score)
    temp_pred.append(preds)

    print ("Untuk kluster={},silhoute score :{} ".format(n_cluster, repr(score)))
    print(preds)

print ("kluster terbaik")
print ("kluster ke > "+str(temp.index(max(temp))+2)+" >silhout> "+str(max(temp)))

print (banyak_cluster)
print (temp)



dataframe1 = pd.read_csv('vsm_baru.csv', encoding='utf-8', index_col=0, sep=',')


dataframe2=pd.DataFrame(columns=['kluster'])
dataframe2['kluster']=temp_pred[temp.index(max(temp))]
#gabung stlh di cluster
dataframe1=pd.concat([dataframe1,dataframe2],axis=1)
#print (dataframe1.head())
#print (len(temp_pred[temp.index(max(temp))]),"panjanggg")

#baru.to_csv('klustering_1099fitur.csv')

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier

#array = dataframe1.values
#X = array[:,0:10]
#Y = array[:,1099]
# feature extraction
#model = ExtraTreesClassifier(n_estimators=10000)
#model.fit(X, Y)
#print(model.feature_importances_)

#list_fitur=data.keys().to_list()



#clf = RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=-1)

# Train the classifier
#clf.fit(X, Y)

# Print the name and gini importance of each feature
#for feature in zip(list_fitur, clf.feature_importances_):
 #   print(feature)


X = dataframe1.drop('kluster', axis = 1)
y = dataframe1['kluster']
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

clf = RandomForestClassifier(n_estimators = 50, max_depth = 4)

scores = []
num_features = len(X.columns)
for i in range(num_features):
    col = X.columns[i]
    score = np.mean(cross_val_score(clf, X[col].values.reshape(-1,1), y, cv=10))
    scores.append((int(score*100), col))
    print (">>>>>>>>>>>>>>>>>>>>")
    print (i,">",col,"score:",score)

print(sorted(scores, reverse = True))

scores = sorted(scores, reverse=True)

print("The 5 best features selected by this method are :")
for i in range(5):
    print(scores[i][1])

print ("The 5 worst features selected by this method are :")
for i in range(5):
    print(scores[len(scores) - 1 - i][1])