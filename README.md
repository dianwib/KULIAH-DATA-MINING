160411100044 _ Dian Wibowo

**KULIAH WEB MINING 2019**

python2.7 (csv,BeautifulSoup4,xlsxwriter,xlrd,pandas,numpy,sklearn,sastrawi,sqlite3), database kamus besar bahasa indonesia, tambahan stopword.

Crawling web *"http://surabaya.tribunnews.com/topic/berita-gresik?&page=?"* sebanyak 5 page dengan rincian 1 page menampung 30 berita, jadi total dokumen /berita yang di crawling sekitar 150 dokumen.

**Tujuan :**

Melakukan Clustering atau pengelompokan berita berdasarkan single ngram (satu kata /fitur yang terdapat pada berita).







**Proses:**

1. ***Crawling*** merupakan proses pengambilan data (text) dari sebuah website menggunakan library python (urllib,Beautifulsoup).

   File:

   1. tribunnews_url >> mengambil setiap link berita pada setiap page url header, lalu disimpan pada file excel.

      ```
      import xlsxwriter
      
      workbook = xlsxwriter.Workbook('tribunnews_daftarlinkberita.xlsx')
      worksheet1 = workbook.add_worksheet()
      kumpulan_link=[]
      ```

      code diatas digunakan untuk membuat file excel baru yang bernama '*tribunnews_daftarlinkberita.xlsx'* yang digunakan untuk menyimpan setiap url link berita pada setiap page berita.

      ```
      def cari_link(page):
          import urllib as link
          from bs4 import BeautifulSoup
          import re
          print (page)
          html_page = link.urlopen("http://surabaya.tribunnews.com/topic/berita-gresik?&page="+str(page)).read()
          soup = BeautifulSoup(html_page, "lxml")def cari_link(page):
          import urllib as link
          from bs4 import BeautifulSoup
          import re
          print (page)
          html_page = link.urlopen("http://surabaya.tribunnews.com/topic/berita-gresik?&page="+str(page)).read()
          soup = BeautifulSoup(html_page, "lxml")
      ```

      code diatas merupakan proses crawling menggunakan library beautifulsoup4 untuk kemudian dikonversi ke dalam tag lxml(html) agar memudahkan kita dalam melakukan filter data yang akan diambil ketika proses crawling, pada website *http://surabaya.tribunnews.com/topic/berita-gresik?&page="+str(page)*, "<u>str(page)"</u> merupakan sebuah value dimana program akan melakukan crawling sebanyak nilai dari variabel page yang diinputkan oleh user.  

      ```
       for a in soup.findAll('h3', 'f20 ln24 fbo'):
              for link in a.findAll('a', attrs={'href': re.compile("^http://")}):
                  #print link.get('href')
                  kumpulan_link.append(link.get('href'))
      ```

      code diatas digunakan untuk mengambil value data (url/link) berita pada tag html yang mengandung attribut "*href*" pada setiap page halaman website.

      ```
      for i in range(1,6):
          cari_link(str(i))
      print len(kumpulan_link)
      
      for baris in range(len(kumpulan_link)):
          print (baris)
          print (kumpulan_link[baris])
          worksheet1.write(baris,1, str(kumpulan_link[baris]))
      workbook.close()
      ```

      code diatas digunakan untuk menjalankan fungsi crawling data sebanyak 5 page (1-5) website. dimana setiap page akan diambil 30 value (url/link) berita lalu akan di simpan ke dalam file excel yang telah di downlot tadi.

      total data yang diambil adalah 150 dokumen dengan rincian @page terdapat 30 berita.

   2. tribunnews_kedb >> melakukan crawling text (judul dan isi) berita pada setiap link yang ada di file excel, lalu menyimpannya pada database.

      ```
      for baris in range(data.nrows):
          print (">>>>>>>>>>>"+str(baris))
      
          from bs4 import BeautifulSoup
      
          value_data = data.cell_value(rowx=baris, colx=1)
          print (value_data)
          html = link.urlopen(str(value_data)).read()
      
          soup = BeautifulSoup(html, "lxml")
      
      
         for baris in range(data.nrows):
          print (">>>>>>>>>>>"+str(baris))
      
          from bs4 import BeautifulSoup
      
          value_data = data.cell_value(rowx=baris, colx=1)
          print (value_data)
          html = link.urlopen(str(value_data)).read()
      
          soup = BeautifulSoup(html, "lxml")
      
      
          berita = soup.find('h1', 'f50 black2 f400 crimson').get_text()
          berita = berita.strip()
          print(berita)
          isi = soup.find('div', 'side-article txt-article').get_text()
          isi=isi.replace('var unruly = window.unruly || {};unruly.native = unruly.native || {};unruly.native.siteId = 1082418;', '').replace('\t\t', '').replace(',', '').replace('googletag.cmd.push(function() { googletag.display("div-Inside-MediumRectangle"); });','')
          isi=isi.replace("googletag.cmd.push(function() { googletag.display('div-Inside-MediumRectangle'); });",'')
          isi=isi.replace("\n",'')
          isi= isi[22:]
          isi=isi.strip()
       berita = soup.find('h1', 'f50 black2 f400 crimson').get_text()
          berita = berita.strip()
          print(berita)
          isi = soup.find('div', 'side-article txt-article').get_text()
          isi=isi.replace('var unruly = window.unruly || {};unruly.native = unruly.native || {};unruly.native.siteId = 1082418;', '').replace('\t\t', '').replace(',', '').replace('googletag.cmd.push(function() { googletag.display("div-Inside-MediumRectangle"); });','')
          isi=isi.replace("googletag.cmd.push(function() { googletag.display('div-Inside-MediumRectangle'); });",'')
          isi=isi.replace("\n",'')
          isi= isi[22:]
          isi=isi.strip()
      ```

      code diatas digunakan untuk melakukan crawling data judul dan isi berita pada setiap url/link berita dimana untuk melakukan pengambilan judul dilakukan filter pada tag html  *('h1', 'f50 black2 f400 crimson')*, dan mengambil isi berita pada tag html *('div', 'side-article txt-article')*.

2. **Prepocessing**  merupakan proses seleksi kata / data yang akan di proses

   Tahapan:

   1. Tokenizing >> pemretelan setiap kata / string pembuangan tanda baca dll
   2. Stemming >> pengambilan kata baku serta penghapusan imbuhan kata
   3. Filtering >> pengambilan kata hasil tokenisasi yang bukan termasuk kata hubung

   menggunakan library (sastrawi)

   File:

   1. tribunnews_sastrawi >> melakukan semua proses prepocessing termasuk pengecekan setiap kata pada database bahasa indonesia serta penambahan fitur stopword (penambahan untuk mengecek kata hubung) .

      ```
          factory = StopWordRemoverFactory()
          stopword = factory.create_stop_word_remover()
          stop = stopword.remove(kalimat)
          stop = re.sub(r'\b\w{1,2}\b', '', stop)
      ```

      code diatas digunakan untuk melakukan proses filtering / menghilangkan kata yang dianggap sebagai kata hubung pada dokumen menggunakan library default dari sastrawi *StopWordRemoverFactory()*.

      ```
          factory = StemmerFactory()
          stemmer = factory.create_stemmer()
          katadasar = stemmer.stem(str(kalimat))
          katadasar = re.sub(r'\b\w{1,3}\b', '', katadasar).replace('-','')
      ```

      code diatas digunakan untuk melakukan proses stemming / proses menghilangkan imbuhan pada setiap kata yabf dianggap sebagai kata ber-imbuhan pada dokumen menggunakan library default dari sastrawi *StemmerFactory()*.

      ```
      elif (tribunnews_cekkamus.cek_kata(kata)==True and tribunnews_cekstopword.cek_kata(kata)==True):
      ```

      code diatas digunakan untuk mengecek setiap kata apakah terdapat pada database kamus besar bahasa indonesia dan mengecek apakah kata tersebut termasuk stopword tambahan.

      tribunnews_cekkamus >> berisi seluruh data kata yang terdapat pada kamus besar bahasa indonesia.

      tribunnews_cekstopword >> berisi kata hubung (stopword) tambahan, hal ini dikarenakan library stopword pada sastrawi kurang mengandung banyak kata hubung.

      

3. **Penjabaran matrik VSM** merupakan proses perhitungan / frekuensi kemunculan semua kata yang terdapat pada setiap dokumen ke dalam bentuk matrik.

   File:

   1. tribunnews_ambilfitur >> mengambil seluruh term atau seluruh kata pada semua dokumen.

      ```
      for row in rows:
          baris=""
          for j in row:
              j=j.replace(',', '')
              baris=baris+j+" "
      
          data.append(baris)
      ```

      code diatas digubakan untuk mengambil / menggabungkan seluruh isi term (kata) di seluruh dokumen, untuk selanjutnya dilakukan perhitungan kemunculan / frekuensi kemunculan kata pada di setiap dokumen.

   2. tribunnews_sastrawi_pilihfrekuaensiseringmuncul >> menghitung frekuensi kemunculan setiap kata dalam bentuk matrik lalu menyimpan ke dalam excel (konvert ke.csv).

      ```
      for baris in range(1,sheetdata.nrows):
          kolom=1
          for temp_fitur in hapus_fitur():
      
              if temp_fitur not in hitung_katatiapbaris()[baris-1]:
                  hasil = 0
                  #continue
              else:
                  hasil=hitung_katatiapbaris()[baris-1][temp_fitur]
              worksheet1.write(baris, kolom, int(hasil))
              kolom+=1
      workbook.close()
      ```

      code diatas digunakan untuk menghitung frekuensi kemunculan seluruh kata pada setiap dokumen, proses tersebut akan memakan waktu yang sangat lama tergantung banyaknya dokumen dan total seluruh kata / term (corpus). 

      total corpus pada project saya sekitar kurang lebih 2000 kata, 2000 kata tersebut akan dijadikan fitur setiap dokumen, jika dibiarkan hal tersebut nantinya akan menyebabkan proses modeling menjadi kurang bagus karena jumlah *total fitur(kata) terlalu banyak dibandingkan jumlah total dokumen*, oleh karena itu diperlukan *seleksi fitur* agar tidak seluruh (2000) kata dijadikan sebagai fitur, seleksi fitur juga bertujuan untuk mengurangi proses komputasi pada saat proses modeling.

   

4. P**erhitungan TF_IDV** merupakan proses menghitung pembobotan kata dalam suatu dokumen dan menjadikan ke bentuk terstruktur.

   File:

   1. tribunnews_tfidf >> melakukan proses perhitungan TF-IDF dan menjadikan ke bentuk matrik.

      ```
      for i in list_fitur:
      
          a=data[i].value_counts()
          a=float(len(list_fitur)-a[0])
          #temp=math.log((len(list_fitur)-1)/(a))
          temp = math.log(len(list_fitur) / (a)) + 1
          w.append(temp)
      ```

      code diatas digunakan untuk menghitung nilai tf_idf pada setiap kata di seluruh dokumen.

      ```
      for i in range(len(list_fitur)):
          temp=list_fitur[i]
          data[temp]*=w[i]
      print (data.head())
      
      data.to_csv('baru_tfidv.csv')
      ```

      code diatas digunakan untuk menyimpan nilai hasil perhitungan tf_idf ke dalam format file (.csv).

      format (.csv) digunakan untuk mempermudah melakukan operasi data science pada python dengan dikombinasikan dengan library pandas dll.

5. **Seleksi Fitur** merupakan proses penghapusan beberapa fitur yang dianggap tidak terlalu berpengaruh pada model, tujuan dari seleksi fitur adalah: 

   1. pertama kita akan membuat model yang akan kita buat menjadi lebih simple untuk di tafsirkan karena hanya menggunkan fitur yang dianggap penting saja serta tidak perlu menggunakan keseluruhan fitur jika itu berjumlah ribuan ataupun jutaan.

   2. kedua mengurangi proses komputasi.

       

   Metode:

   1. *PCA (Principal Component Analysis):* 

      Merupakan metode penyusutan / penyederhanaan fitur dari total keseluruhan fitur.

   2. *Model Based Ranking:* 

      Memungkinkan kita untuk menyesuaikan classfier untuk setiap fitur dan memberi peringkat kekuatan prediksi. Metode ini memilih fitur yang paling kuat secara individual tetapi diabaikan kekuatan prediksi ketika fitur digabungkan. Metode Random Forest digunakan dalam kasus ini karena kuat, nonlinier, dan tidak memerlukan penskalaan.   

   3. *UFS (Univariate Feature Selection):* 

      Digunakan untuk memilih fitur terbaik dengan menjalankan statistik univariate, seperti uji chi-squared, uji F-1, dan mutual information.

   4. *RFE (Rekursif Feature Extraction):*

      Metode ini berjalan secara rekursif memilih subset penting dari fitur berdasarkan 
      pada atribut bawaan seperti koefisien atau kepentingan fitur dari estimator yang diberikan.
                   
      <u>Kesimpulan :</u>  

      Untuk Feature Selection, diperlukan penggabungan beberapa teknik / metode, dalam hal ini kombinasi dan cross validation harus memberikan result / hasil yang bagus. Untuk Ranking Feature, hal yang perlu diperhatikan adalah untuk berhati-hati dalam memilih setiap metode yang akan digunakan.

      Model Random Forest banyak digunakan karena dianggap memiliki peringkat terbaik dalam hal menentukan pemilihan fitur terbaik / paling berpengaruh pada suatu model berdasar information gain. Random Forest bekerja dengan banyak n_estimator / tree (pohon keputusan) untuk menghasilkan hasil nilai keputusan yang terbaik.

      Semakin banyak n_estimator / tree (pohon keputusan) pada Random Forest maka akan memerlukan waktu komputasi yang lama menghasilkan nilai yang bagus / akurat. begitu pula sebaliknya jika menggunakan n_estimator sedikit.

   ​          

6. **Clustering** merupakan proses pengelompokan data berdasarkan kemiripan fitur tertentu

Metode:

1. Kmean Clustering merupakan salah satu algoritma untuk melakukan clustering. Fungsi algoritma ini yaitu untuk membagi data menjadi beberapa kelompok berdasarkan class inputan yang diterima / jumlah kelompok (cluster) yang diinginkan. Algoritma ini akan mengelompokkan data atau objek ke dalam adalah data atau objek kedalam setiap class .

File :

- tribunnews_KmeanSeleksiFitur(RFE,UFS,BasedRanking) .

   1. melakukan clustering dengan total corpus (total data) asli sebanyak 1099 fitur.

      ```
      banyak_cluster = list(range(2, 150))
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
      ```

      code diatas digunakan untuk melakukan proses clustering menggunakan metode *K-mean clustering*  menggunakan *euclidean* serta menghitung nilai *silhoutte* pada setiap cluster dengan menggunakan total corpus asli sebanyak kurang lebih 2000, untuk selanjutnya menampilkan nilai *silhoutte* terbaik

      pada cluster tertentu.

   2. melakukan pilihan 4 metode seleksi fitur (RFE model Linier Regresion ,RFE model random Forest, UFS model chi square, UFS mutual information), serta menginputkan berapa jumlah fitur yang di ingikan untuk dilakukan clustering .

      ```
      def RFE(cek, n_ranking):
          from sklearn.feature_selection import RFE
          from sklearn.linear_model import LogisticRegression
      
              print ("RFE (Recursive Feature Elimination) model LogisticRegression >>>>>>>")
              rfe = RFE(LogisticRegression(), n_features_to_select=1)
          rfe.fit(X, y)
          scores = []
          for i in range(num_features):
              scores.append((rfe.ranking_[i], X.columns[i]))
          print (sorted(scores, reverse=True))
          print_best_worst(scores, n_ranking)
      ```

      code diatas digunakan untuk melakukan proses seleksi fitur menggunakan metode *Logistic Regression*.

      ```
      def RFE(cek, n_ranking):
          from sklearn.ensemble import RandomForestClassifier
          from sklearn.feature_selection import RFE
              rfe = RFE(RandomForestClassifier(n_estimators=50), n_features_to_select=1)
          rfe.fit(X, y)
          scores = []
          for i in range(num_features):
              scores.append((rfe.ranking_[i], X.columns[i]))
      
          print (sorted(scores, reverse=True))
          print_best_worst(scores, n_ranking)
      ```

      code diatas digunakan untuk melakukan proses seleksi fitur menggunakan metode *Random Forest* menggunakan n_estimator pohon keputusan sebanyak 50 pohon.

      ```
      def UFS(cek, n_ranking):
          from sklearn.feature_selection import SelectKBest
          from sklearn.feature_selection import chi2, mutual_info_classif
              print ("UFS (Univariate Feature Selection) model chi^2 >>>>>>>")
              test = SelectKBest(score_func=chi2, k=2)
          test.fit(X, y)
          scores = []
          for i in range(num_features):
              score = test.scores_[i]
              scores.append((score, X.columns[i]))
      
          print (sorted(scores, reverse=True))
          print_best_worst(scores, n_ranking)
      ```

      code diatas digunakan untuk melakukan proses seleksi fitur menggunakan metode *Chi Square*.

      ```
      def UFS(cek, n_ranking):
          from sklearn.feature_selection import SelectKBest
          from sklearn.feature_selection import chi2, mutual_info_classif
              print ("UFS (Univariate Feature Selection) mutual_info_classif >>>>>>>")
              test = SelectKBest(score_func=mutual_info_classif, k=2)
      
          test.fit(X, y)
          scores = []
          for i in range(num_features):
              score = test.scores_[i]
              scores.append((score, X.columns[i]))
      
          print (sorted(scores, reverse=True))
          print_best_worst(scores, n_ranking)
      ```

      code diatas digunakan untuk melakukan proses seleksi fitur menggunakan metode *Mutual Information*.

   3. Model Based Ranking model Random Forest melakukan proses perhitungan gain setiap fitur, lalu melakukan perankingan berdasarkan nilai gain seluruh fitur.

      ```
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
      ```

      code diatas digunakan untuk melakukan proses perankingan seluruh fitur menggunakan metode *Random Forest* dengan menggunakan 50 tree decision. Tujuan perankingan sendiri adalah untuk melihat seluruh fitur yang memiliki nilai lebih / fitur yang paling berpengaruh.

      ```
          scores = sorted(scores, reverse=True)
          print ("Random Forest>>>>>>>")
          print("The 5 best features selected by this method are :")
          for i in range(5):
              print(scores[i][1])
      ```

      code diatas digunakan untuk menampilkan 5 fitur ranking teratas 

   

- tribunnews_kmean(1100fitur) >> melakukan clustering dengan total corpus (total data) asli sebanyak 1099 fitur untuk mencari silhoute terbaik.

   ```
   banyak_cluster = list(range(2, 150))
   for n_cluster in banyak_cluster:
       clusterer = KMeans(n_clusters=n_cluster)
       preds = clusterer.fit_predict((df))centers = clusterer.cluster_centers_
   score = silhouette_score(df, preds, metric='euclidean')
   temp.append(score)
   temp_pred.append(preds)
   
   # print ("Untuk kluster={},silhoute score :{} ".format(n_cluster, repr(score)))
   # print(preds)
   print ("kluster terbaik")
   print ("kluster ke > " + str(temp.index(max(temp)) + 2) + " >silhout> " + str(max(temp)))
   ```

   code diatas digunakan untuk melakukan proses clustering menggunakan metode *K-mean clustering*  menggunakan *euclidean* serta menghitung nilai *silhoutte* pada setiap cluster dengan menggunakan total corpus asli sebanyak kurang lebih 2000, untuk selanjutnya menampilkan nilai *silhoutte* terbaik

   pada cluster tertentu.

- tribunnews_kmeanwithAllPCA >> mencari berapa nilai jumlah PCA yang memiliki nilai  silhoute terbaik dalam melakukan clustering dengan total corpus (total data) asli sebanyak 1099 fitur.

   ```
   banyak_pca = list(range(3, 150))
   dict_temp={}
   temp_kluster=[]
   temp_silhout=[]
   for n_pca in banyak_pca:
   ```

   code diatas digunakan untuk melakukan proses looping banyaknya PCA yang akan digunakan yang di mulai dari 3 sampai 149.

   ```
   dataframe = pd.read_csv('baru_tfidv.csv', encoding='utf-8', skiprows=0, index_col=0, sep=',')
   df = dataframe.copy(deep=True)
   pca = PCA(n_components=n_pca)
   principalcomponent = pca.fit_transform(df)
   kolom=[]
   for i in range(n_pca):
       kolom.append("PCA"+str(i+1))
   principaldf = pd.DataFrame(data=principalcomponent, columns=kolom)
   new_csv = principaldf.to_csv('baru_withpca.csv')
   dataframe = pd.read_csv('baru_withpca.csv', encoding='utf-8', skiprows=0, index_col=0, sep=',')
   
   df = dataframe.copy(deep=True)
   ```

   code diatas digunakan untuk melakukan perhitungan setiap looping (banyak) PCA diatas tadi.

   ```
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
   temp_kluster.append(dict_temp[n_pca]["kluster"])
   temp_silhout.append((dict_temp[n_pca]["silhout"]))
   ```

   code diatas digunakan untuk melakukan proses clustering menggunakan metode *K-mean clustering*  menggunakan *euclidean* dengan menggunakan jumlah fitur sebanyak looping PCA diatas tadi, serta menghitung dan mencari setiap nilai silhoutte terbaiknya pada setiap cluster.

   ```
   baru=pd.DataFrame(columns=['n_PCA','kluster','silhout'])
   baru['n_PCA']=banyak_pca
   baru['kluster']=temp_kluster
   baru['silhout']=temp_silhout
   print (baru.head())
   
   baru.to_csv('klustering_allPCA.csv')
   ```

   code diatas digunakan untuk melakukan proses  penyimpanan nilai PCA, silhoutte, dan cluster ke format file (.csv) untuk mempermudah melakukan analisis data.

   

   <u>*Kesimpulan Project :*</u>

- nilai silhoute terbaik saat menggunkan 1099 fitur adalah < 0.1,
- nilai silhoute terbaik saat dilakukan seleksi fitur mengunakan Random Forest dengan n_estimator 5 mencapai  < 0.3,
- nilai silhoute terbaik saat dilakukan seleksi fitur mengunakan Random Forest dengan n_estimator 50 mencapai  +-0.6,
- nilai silhoute terbaik saat dilakukan penyusutan fitur menggunkan PCA mencapai  <  0.4 (nilai terbaik dengan menggunakan 6 PCA pada kluster ke 8 / dengan 4 PCA pada kluster ke 6).

