160411100044 _ Dian Wibowo

KULIAH WEB MINING 2019tribunnews_kedb

python2.7(csv,BeautifulSoup4,xlsxwriter,xlrd,pandas,numpy,sklearn,sastrawi,sqlite3),database kamus bhs indo, tambahan stopword

Crawling web "http://surabaya.tribunnews.com/topic/berita-gresik?&page=?" sebanyak 5 page dengan rincian 1 page menampung 30 berita, jadi total dokumen /berita yang di crawling sekitar 150 dokumen

Tujuan :

Melakukan Clustering atau pengelompokan berita berdasarkan single ngram (satu kata /fitur yang terdapat pada berita)

Proses:

1. Crawling merupakan proses pengambilan data (text) dari sebuah website

   menggunakan library (urllib,Beautifulsoup)

   File:

   1. tribunnews_url >> mengambil setiap link berita pada setiap page url header, lalu disimpan pada file excel

   2. tribunnews_kedb >> melakukan crawling text (judul dan isi) berita pada setiap link yang ada di file excel, lalu menyimpannya pada database

      

2. Prepocessing  merupakan proses seleksi kata / data yang akan di proses

   Tahapan:

   1. Tokenizing >> pemretelan setiap kata / string pembuangan tanda baca dll
   2. Stemming >> pengambilan kata baku serta penghapusan imbuhan kata
   3. Filtering >> pengambilan kata hasil tokenisasi yang bukan termasuk kata hubung

   menggunakan library (sastrawi)

   File:

   1. tribunnews_sastrawi >> melakukan semua proses prepocessing termasuk pengecekan setiap kata pada database bahasa indonesia serta penambahan fitur stopword (penambahan untuk mengecek kata hubung) 

      

3. Prepocessing  merupakan proses seleksi kata / data yang akan di proses

   Tahapan:

   1. Tokenizing >> pemretelan setiap kata / string pembuangan tanda baca dll
   2. Stemming >> pengambilan kata baku serta penghapusan imbuhan kata
   3. Filtering >> pengambilan kata hasil tokenisasi yang bukan termasuk kata hubung

   menggunakan library (sastrawi)

   File:

   1. tribunnews_sastrawi >> melakukan semua proses prepocessing termasuk pengecekan setiap kata pada database bahasa indonesia serta penambahan fitur stopword (penambahan untuk mengecek kata hubung) 

      

4. Penjabaran matrik VSM merupakan proses perhitungan / frekuensi kemunculan semua kata yang terdapat pada setiap dokumen ke dalam bentuk matrik

   File:

   1. tribunnews_ambilfitur >> mengambil seluruh term atau seluruh kata pada semua dokumen
   2. tribunnews_sastrawi_pilihfrekuaensiseringmuncul >> menghitung frekuensi kemunculan setiap kata dalam bentuk matrik lalu menyimpan ke dalam excel (konvert ke.csv)

   

5. Perhitungan TF_IDV merupakan proses menghitung pembobotan kata dalam suatu dokumen dan menjadikan ke bentuk terstruktur

   File:

   1. tribunnews_tfidf >> melakukan proses perhitungan TF-IDF dan menjadikan ke bentuk matrik 

6. Perhitungan TF_IDV merupakan proses menghitung pembobotan kata dalam suatu dokumen dan menjadikan ke bentuk terstruktur

   File:

   1. tribunnews_tfidf >> melakukan proses perhitungan TF-IDF dan menjadikan ke bentuk matrik 

7. Seleksi Fitur merupakan proses penghapusan beberapa fitur yang dianggap tidak terlalu berpengaruh pada model, tujuan dari seleksi fitur adalah: 

   1. pertama kita akan membuat model yang akan kita buat menjadi lebih simple untuk di tafsirkan karena hanya menggunkan fitur yang dianggap penting saja serta tidak perlu menggunakan keseluruhan fitur jika itu berjumlah ribuan ataupun jutaan

   2. kedua mengurangi proses komputasi

       

   Metode:

   model RandomForest banyak digunakan karena dianggap memiliki peringkat terbaik dalam hal menentukan pemilihan fitur terbaik / paling berpengaruh pada suatu model berdasar information gain

   PCA (Principal Component Analysis) merupakan metode penyusutan / penyederhanaan fitur dari total keseluruhan fitur

   >>>  Model Based Ranking:
   >>>                   Kita dapat menyesuaikan classfier untuk setiap fitur dan memberi peringkat kekuatan prediksi.
   >>>                   Metode ini memilih fitur yang paling kuat secara individual tetapi diabaikan
   >>>                   kekuatan prediksi ketika fitur digabungkan. Metode Random Forest digunakan dalam 
   >>>                   kasus ini karena kuat, nonlinier, dan tidak memerlukan penskalaan.

   ```
                UFS (Univariate Feature Selection):
                Digunakan untuk memilih fitur terbaik dengan menjalankan statistik univariate
                tes seperti uji chi-squared, uji F-1, dan mutual information.
                
                RFE (Rekursif Feature Extraction):
                Metode ini berjalan secara rekursif memilih subset penting dari fitur berdasarkan 
                pada atribut bawaan seperti koefisien atau kepentingan fitur dari estimator yang diberikan.
                
                Kesimpulan :
                Untuk Feature Selection, diperlukan penggabungan beberapa teknik ini dalam kombinasi dan cross validation
                harus memberikan hasil yang bagus. Untuk Ranking Feature, penting untuk berhati-hati dalam memilih setiap metode.
   ```


   ​             

8. Clustering merupakan proses pengelompokan data berdasarkan kemiripan fitur tertentu

   Metode:

   1. Kmean Clustering

   

   File :

   1. tribunnews_KmeanSeleksiFitur(RFE,UFS,BasedRanking) 

      1. melakukan clustering dengan total corpus (total data) asli sebanyak 1099 fitur
      2. melakukan pilihan 4 metode seleksi fitur (RFE model Linier Regresion ,RFE model random Forest, UFS model chi square, UFS mutual information), serta menginputkan berapa jumlah fitur yang di ingikan untuk dilakukan clustering 
      3. Model Based Ranking model RandomForest melakukan proses perhitungan gain setiap fitur, lalu melakukan perankingan berdasarkan nilai gain seluruh fitur

      

   2. tribunnews_kmean(1100fitur) >> melakukan clustering dengan total corpus (total data) asli sebanyak 1099 fitur untuk mencari silhoute terbaik

   3. tribunnews_kmeanwithAllPCA >> mencari berapa nilai jumlah PCA yang memiliki nilai  silhoute terbaik dalam melakukan clustering dengan total corpus (total data) asli sebanyak 1099 fitur

   4. tribunnews_kmeanwithPCA >>  melakukan clustering dengan total corpus (total data) asli sebanyak 1099 fitur untuk mencari silhoute terbaik dengan menggunakan total 6 PCA

Kesimpulan Project

nilai silhoute terbaik saat menggunkan 1099 fitur adalah < 0.1

nilai silhoute terbaik saat dilakukan seleksi fitur mencapai  +-0.7

nilai silhoute terbaik saat dilakukan penyusutan fitur menggunkan PCA mencapai  <  0.4





