**Scraping website https://www.otomart.id**

**Tujuan** **:** Memperoleh data mobil, seperti (merk mobil, model mobil, tipe mobil, harga mobil, dll )

 yang di jual pada website tersebut.

**Tools :**

1. Pycharm include Python 2.7.
2. Library Python seperti Beautiful Soup / bs4, sqlite3, urllib.
3. Terminal linux ubuntu 18.04.

**Langkah-langkah:**

1. Menentukan website yang akan di scraping, misal **(www.otomart.id)**

2. Menentukan **top level url web** yang akan di scrapping untuk mendapatkan source code html, misal **(https://www.otomart.id/cari-mobil/?limit=500).**

3. Menginstall library urllib pada terminal ubuntu, source code **(*pip install urllib*)**

4. Menginstall library Beautiful Soup  pada terminal ubuntu dan pastikan terkoneksi internet, source code **(*apt-get install python-bs4*,*pip install beatifulsoup4*).**

5. Membuat file python **beutiful_url.py.**

6. **Inisialisasi ulrllib**, tambahkan source code pada file python beutiful_url.py.

   ```
   import urllib as link
   html = link.urlopen("https://www.otomart.id/cari-mobil/?limit=500").read()
   ```

   **urllib** adalah library python yang digunakan untuk mengakses web, sedangkan fungsi **urlopen()** dan **read()** digunakan untuk membaca HTML yang dikonversi dalam format **String**.

   **?limit=500** digunakan untuk mengambil 500 data mobil dalam 1 tampilan website.

   *contoh hasil print variabel html index 0-1000*

   <!DOCTYPE html>
   <head>
   	<!-- Google Analytics Content Experiment code -->
   	<style>.async-hide { opacity: 0 !important} </style>
   <script>(function(a,s,y,n,c,h,i,d,e){s.className+=' '+y;h.start=1*new Date;
   h.end=i=function(){s.className=s.className.replace(RegExp(' ?'+y),'')};
   (a[n]=a[n]||[]).hide=h;setTimeout(function(){i();h.end=null},c);h.timeout=c;
   })(window,document.documentElement,'async-hide','dataLayer',4000,
   {'GTM-K2H3W87':true});</script>	<!-- End of Google Analytics Content Experiment code -->
   	<script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
     (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
     m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
     })(window,document,'script','//www.google-analytics.com/analytics.js','ga');  
     ga('create', 'UA-59607984-1', 'auto');
     ga('require', 'GTM-K2H3W87');
     ga('send', 'pageview'); 
   </script>  	<meta charset="utf-8">
   <meta http-equiv="X-UA-

7. Buat file python **beutiful_kedb.py.**

8. **Inisialisasi BeautifulSoup**, tambahkan source code pada file python beutiful_kedb.py.

   ```
   import beutiful_url
   import pandas as pd
   from bs4 import BeautifulSoup
   soup=BeautifulSoup(beutiful_url.html,"lxml")
   ```

   **beautifulsoup** digunakan untuk membantu proses scrapping dengan cara mengimport librarynya, lalu string html diubah menjadi objek beautifulsoup menggunakan parser **lxml.**

9. **Inisialisasi sqlite3**, tambahkan source code pada file python beutiful_kedb.py.

   ```
   import sqlite3
   conn = sqlite3.connect('otomart.db')
   c = conn.cursor()
   ```

   **sqlite3** digunakan untuk memanipulasi database menggunakan python, **otomart.db** adalah nama database yang akan dimanipulasi.

10. Tambahkan source code di bawah ini secara berurutan pada file beutiful_kedb.py.

    **sqlite3** digunakan untuk memanipulasi database menggunakan python, **otomart.db** adalah nama database yang akan dimanipulasi.

    ```
    c.execute('DROP TABLE IF EXISTS mobil_bekas')
    c.execute('''CREATE TABLE IF NOT EXISTS mobil_bekas
                 (merk VARCHAR, model VARCHAR, tipe VARCHAR, harga INTEGER, kota VARCHAR, provinsi VARCHAR, showroom VARCHAR, transmisi VARCHAR, warna VARCHAR, deskripsi VARCHAR)''')
    conn.commit()
    ```

    code diatas digunakan untuk membuat tabel **mobil_bekas** dengan attribut yang telah di tentukan pada database **otomart.db**.

    ```
    produk = soup.find_all("div","box-car clearfix")
    ```

    digunakan untuk memfilter setiap class ***"box-car clearfix"*** pada tag <div> html pada website , karena pada frame tersebut berisi beberapa elemen yang dapat kita ambil datanya, misalnya (merk, harga lokasi mobil dll).**

    *nb : untuk menemukan **tag dan class html yang akan di filter maka sebelumnya lakukanlah inspect element / mode view tag html pada web browser** hal tersebut tergantung pada posisi letak setiap objek pada tag html setiap website hal tersebut dilakukan secara looping secara otomatis sebanyak program menemukan frame tersebut untuk melakukan scrapping data website.*

    ```
    for p in produk:
        temp_merk = p.find('h3', 'car-name-blue').get_text()
        merk = temp_merk[:temp_merk.index(' ')] 
    ```

    digunakan untuk memfilter merk mobil pada setiap class ***"car-name-blue"*** pada tag <h3> html, namun diambil satu kata yang paling depan  yang di identifikasi sebagai merk mobil.

    ```
    if '.' not in temp_merk:
        model = temp_merk[temp_merk.index(' ') + 1:]
        tipe = 'Lainnya'
    else:
        model = temp_merk[temp_merk.index(' ') + 1:temp_merk.index('.') - 2]  # model
    ```

    digunakan untuk memfilter model mobil pada setiap class ***"car-name-blue"*** pada tag <h3> html, kali ini diambil kata kedua (tengah)  yang di identifikasi sebagai model mobil.

    ```
    tipe = temp_merk[temp_merk.index('.') - 1:-1]  # tipe
    ```

    digunakan untuk memfilter tipe mobil pada setiap class ***"car-name-blue"*** pada tag <h3> html, namun diambil kata ketiga (terakhir)  yang di identifikasi sebagai tipe mobil.

    ```
    harga = p.find('span', 'yellow').get_text().replace('Rp', '').replace('.', '').replace(' ', '')  # harga
    ```

    digunakan untuk memfilter harga mobil pada setiap class ***"yellow"*** pada tag <span> html.

    ```
    temp_lokasi = p.find('h4', 'dealername').get_text()[1:]  # lokasi
    kota = temp_lokasi[:temp_lokasi.index(',')]  # kota
    ```

    digunakan untuk memfilter lokasi (kota) penjual mobil pada setiap class ***"dealername"*** pada tag <h4> html, namun diambil kata pertama (sebelum tanda koma) yang diidentifikasi sebagai kota penjual mobil.

    ```
    provinsi = temp_lokasi[temp_lokasi.index(',') + 2:]  # provinsi
    ```

    digunakan untuk memfilter lokasi (provinsi) penjual mobil pada setiap class ***"dealername"*** pada tag <h4> html, kali ini diambil kata terakhir (setelah tanda koma) yang diidentifikasi sebagai provinsi penjual mobil.

    ```
    showroom = p.find('h3', 'dealername txt-algn hidden-xs').get_text().replace('\n', '').replace('-', '').replace('.',
                                                                                                                   '')[
               16:]  # nama dealer
    showroom = showroom.strip()
    ```

    digunakan untuk memfilter nama showroom mobil pada setiap class ***"dealername txt-algn hidden-xs"*** pada tag <h3> html.

    ```
    temp_detil = (
        p.find("ul", "list-inline descrip").get_text().replace(' ', '').replace('\n', ' ').replace('\t', '').replace(
            'Bandingkan', ''))  # tahun    #print(p.find('li', '').get_text())  # warna
    tahun = temp_detil[2:6]  # tahun
    ```

    digunakan untuk memfilter tahun mobil dibuat pada setiap class ***"list-inline descrip"*** pada tag <ul> html, namun hanya diambil 4 karakter string mulai dari index karakter ke 2 sampai 6 yang diidentifikasi sebagai tahun modil dibuat.

    ```
    warna = temp_detil[9:16]  # warna
    warna = warna.strip()
    ```

    digunakan untuk memfilter warna mobil pada setiap class ***"list-inline descrip"*** pada tag <ul> html, namun hanya diambil index karakter string mulai dari index ke 9 sampai 16 yang diidentifikasi sebagai warna mobil.

    ```
    transmisi = temp_detil[17:]  # transmisi
    transmisi = transmisi.strip()
    ```

    digunakan untuk memfilter tipe transmisi mobil pada setiap class ***"list-inline descrip"*** pada tag <ul> html, kali ini hanya diambil index karakter string mulai dari index ke 17 sampai indeks yang diidentifikasi sebagai tipe transmisi mobil.

    ```
    deskripsi = (p.find("p", "des-carlist").get_text().replace('\n', '').replace('\r', ''))  # abstract
    deskripsi = deskripsi.strip()
    ```

    digunakan untuk memfilter deksripsi penujal pada setiap class ***"list-inline descrip"*** pada tag <p> html.

    ```
    c.execute("INSERT INTO mobil_bekas (merk, model, tipe, harga, kota, provinsi, showroom, transmisi, warna, deskripsi) values (?, ?,?, ?, ?,?,?, ?, ?,?)", (merk, model, tipe, harga, kota, provinsi, showroom, transmisi, warna, deskripsi))
    conn.commit()
    ```

    digunakan untuk memasukkan atau insert data kedalam tabel **mobil_bekas** yang telah diinisialisasi sebelumnya setiap 1x looping atau setiap menemukan frame **(produk = soup.find_all("div","box-car clearfix")** diatas tadi.

    *nb : hal tersebut terjadi atau dilakukan sebanyak program menemukan frame tersebut pada script website.*