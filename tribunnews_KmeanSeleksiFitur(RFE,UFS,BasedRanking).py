import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

dataframe = pd.read_csv('baru_tfidv.csv', encoding='utf-8', skiprows=0, index_col=0, sep=',')

df = dataframe.copy(deep=True)

banyak_cluster = list(range(2, 150))
print ("Kmeans kluster dari 2 to 149: ", banyak_cluster)

temp = []
temp_pred = []
for n_cluster in banyak_cluster:
    clusterer = KMeans(n_clusters=n_cluster)
    preds = clusterer.fit_predict((df))

    centers = clusterer.cluster_centers_
    score = silhouette_score(df, preds, metric='euclidean')
    temp.append(score)
    temp_pred.append(preds)

    # print ("Untuk kluster={},silhoute score :{} ".format(n_cluster, repr(score)))
    # print(preds)

print ("kluster terbaik")
print ("kluster ke > " + str(temp.index(max(temp)) + 2) + " >silhout> " + str(max(temp)))

# print (banyak_cluster)
# print (temp)


dataframe1 = pd.read_csv('vsm_baru.csv', encoding='utf-8', index_col=0, sep=',')

dataframe2 = pd.DataFrame(columns=['kluster'])
dataframe2['kluster'] = temp_pred[temp.index(max(temp))]
dataframe1 = pd.concat([dataframe1, dataframe2], axis=1)

X = dataframe1.drop('kluster', axis=1)
y = dataframe1['kluster']

num_features = len(X.columns)


def print_best_worst(scores, n_ranking):
    scores = sorted(scores, reverse=True)

    fitur_terpilih = []
    print("The " + str(n_ranking) + " best features selected by this method are :")
    for i in range(n_ranking):
        fitur_terpilih.append(scores[i][1])
        print(scores[i][1])

    print ("The " + str(n_ranking) + " worst features selected by this method are :")
    for i in range(n_ranking):
        print(scores[len(scores) - 1 - i][1])
    K_mean(fitur_terpilih)


def RandomForest():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import cross_val_score

    clf = RandomForestClassifier(n_estimators=50, max_depth=4)

    scores = []
    num_features = len(X.columns)
    for i in range(num_features):
        col = X.columns[i]
        score = np.mean(cross_val_score(clf, X[col].values.reshape(-1, 1), y, cv=10))
        scores.append((int(score * 100), col))
        print (">>>>>>>>>>>>>>>>>>>>")
        print (i, ">", col, "score:", score)

    scores = sorted(scores, reverse=True)
    print ("Random Forest>>>>>>>")
    print("The 5 best features selected by this method are :")
    for i in range(5):
        print(scores[i][1])

    print ("The 5 worst features selected by this method are :")
    for i in range(5):
        print(scores[len(scores) - 1 - i][1])


def RFE(cek, n_ranking):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.feature_selection import RFE
    from sklearn.linear_model import LogisticRegression

    if cek == 1:
        print ("RFE (Recursive Feature Elimination) model LogisticRegression >>>>>>>")
        rfe = RFE(LogisticRegression(), n_features_to_select=1)


    elif cek == 2:
        print ("RFE (Recursive Feature Elimination) model RandomForest >>>>>>>")
        rfe = RFE(RandomForestClassifier(n_estimators=50), n_features_to_select=1)

    rfe.fit(X, y)
    scores = []

    for i in range(num_features):
        scores.append((rfe.ranking_[i], X.columns[i]))

    print (sorted(scores, reverse=True))
    print_best_worst(scores, n_ranking)


def UFS(cek, n_ranking):
    from sklearn.feature_selection import SelectKBest
    from sklearn.feature_selection import chi2, mutual_info_classif

    if cek == 1:
        print ("UFS (Univariate Feature Selection) model chi^2 >>>>>>>")
        test = SelectKBest(score_func=chi2, k=2)

    elif cek == 2:

        print ("UFS (Univariate Feature Selection) mutual_info_classif >>>>>>>")
        test = SelectKBest(score_func=mutual_info_classif, k=2)

    test.fit(X, y)
    scores = []
    for i in range(num_features):
        score = test.scores_[i]
        scores.append((score, X.columns[i]))

    print (sorted(scores, reverse=True))
    print_best_worst(scores, n_ranking)


def K_mean(data):
    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    dataframe = pd.read_csv('baru_tfidv.csv', encoding='utf-8', skiprows=0, index_col=0, sep=',')
    print (data)
    dataframe = dataframe.loc[:, dataframe.columns.isin(data)]

    print (dataframe.info())
    df = dataframe.copy(deep=True)
    banyak_cluster = list(range(2, 150))
    print ("Kmeans kluster dari 2 to 149: ", banyak_cluster)

    temp = []
    temp_pred = {}
    for n_cluster in banyak_cluster:
        clusterer = KMeans(n_clusters=n_cluster)
        preds = clusterer.fit_predict((df))

        centers = clusterer.cluster_centers_
        score = silhouette_score(df, preds, metric='euclidean')
        temp.append(score)
        temp_pred[n_cluster] = preds

        # print ("Untuk kluster={},silhoute score :{} ".format(n_cluster, repr(score)))
        # print(preds)

    print ("kluster terbaik")
    print ("kluster ke > " + str(temp.index(max(temp)) + 2) + " >silhout> " + str(max(temp)))
    index = int(temp.index(max(temp)))
    print (temp_pred.values()[index])


while True:
    print ("""\t\t\t
            >>>  Model Based Ranking:
                 Kita dapat menyesuaikan classfier untuk setiap fitur dan memberi peringkat kekuatan prediksi.
                 Metode ini memilih fitur yang paling kuat secara individual tetapi diabaikan
                 kekuatan prediksi ketika fitur digabungkan. Metode Random Forest digunakan dalam 
                 kasus ini karena kuat, nonlinier, dan tidak memerlukan penskalaan.

                 UFS (Univariate Feature Selection):
                 Digunakan untuk memilih fitur terbaik dengan menjalankan statistik univariate
                 tes seperti uji chi-squared, uji F-1, dan mutual information.

                 RFE (Rekursif Feature Extraction):
                 Metode ini berjalan secara rekursif memilih subset penting dari fitur berdasarkan 
                 pada atribut bawaan seperti koefisien atau kepentingan fitur dari estimator yang diberikan.

                 Kesimpulan :
                 Untuk Feature Selection, diperlukan penggabungan beberapa teknik ini dalam kombinasi dan cross validation
                 harus memberikan hasil yang bagus. Untuk Ranking Feature, penting untuk berhati-hati dalam memilih setiap metode.

              1. RFE model LinierRegresion                         
              2. RFE model RandomForest
              3. UFS model chi^2
              4. UFS model mutual_info_classif
              5. Model Based Ranking RandomForest
              6. Stop

              """)
    cek = int(input("pilih model feature ranking: "))
    n_ranking = int(input("Pilih banyak ranking: "))
    if cek == 1:
        RFE(1, n_ranking)
    elif cek == 2:
        RFE(2, n_ranking)
    elif cek == 3:
        UFS(1, n_ranking)
    elif cek == 4:
        UFS(2, n_ranking)
    elif cek == 5:
        RandomForest()
    elif cek == 6:
        break