import beutiful_url
from bs4 import BeautifulSoup

soup=BeautifulSoup(beutiful_url.html,"lxml")

import sqlite3
conn = sqlite3.connect('otomart.db')
c = conn.cursor()

# Create table
c.execute('DROP TABLE IF EXISTS mobil_bekas')
c.execute('''CREATE TABLE IF NOT EXISTS mobil_bekas
             (merk VARCHAR, model VARCHAR, tipe VARCHAR, harga INTEGER, tahun VARCHAR, kota VARCHAR, provinsi VARCHAR, showroom VARCHAR, transmisi VARCHAR, warna VARCHAR, deskripsi VARCHAR)''')
conn.commit()

# Insert a row of data





daftar_merk=[]
daftar_model=[]
daftar_tipe=[]
daftar_harga=[]
daftar_kota=[]
daftar_provinsi=[]
daftar_showroom=[]
daftar_tahunmobil=[]
daftar_warnamobil=[]
daftar_transmisimobil=[]
daftar_deskripsi=[]


produk = soup.find_all("div","box-car clearfix") #class yang kan difilter pada inspect element #div=tag html / box car==classnya

for p in produk:
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # print(p.find('h3','car-name-blue').get_text())#merk

    temp_merk = p.find('h3', 'car-name-blue').get_text()
    print(temp_merk)
    merk = temp_merk[:temp_merk.index(' ')]  # merk
    print(merk)

    if '.' not in temp_merk:
        model = temp_merk[temp_merk.index(' ') + 1:]
        tipe = 'Lainnya'
    else:
        model = temp_merk[temp_merk.index(' ') + 1:temp_merk.index('.') - 2]  # model
        tipe = temp_merk[temp_merk.index('.') - 1:-1]  # tipe

    print(model)
    print(tipe)

    harga = p.find('span', 'yellow').get_text().replace('Rp', '').replace('.', '').replace(' ', '')  # harga
    print(harga)

    # print(p.find('h4','dealername').get_text()[1:])#lokasi
    temp_lokasi = p.find('h4', 'dealername').get_text()[1:]  # lokasi
    kota = temp_lokasi[:temp_lokasi.index(',')]  # kota
    provinsi = temp_lokasi[temp_lokasi.index(',') + 2:]  # provinsi
    print(kota)
    print(provinsi)

    showroom = p.find('h3', 'dealername txt-algn hidden-xs').get_text().replace('\n', '').replace('-', '').replace('.',
                                                                                                                   '')[
               16:]  # nama dealer
    showroom = showroom.strip()
    print(showroom)

    temp_detil = (
        p.find("ul", "list-inline descrip").get_text().replace(' ', '').replace('\n', ' ').replace('\t', '').replace(
            'Bandingkan', ''))  # tahun    #print(p.find('li', '').get_text())  # warna
    tahun = temp_detil[2:6]  # tahun
    print(tahun)
    warna = temp_detil[9:16]  # warna
    warna = warna.strip()
    print(warna)

    transmisi = temp_detil[17:]  # transmisi
    transmisi = transmisi.strip()
    print(transmisi)

    deskripsi = (p.find("p", "des-carlist").get_text().replace('\n', '').replace('\r', ''))  # abstract
    deskripsi = deskripsi.strip()
    print(deskripsi)

    #insert to table
    c.execute("INSERT INTO mobil_bekas (merk, model, tipe, harga,tahun, kota, provinsi, showroom, transmisi, warna, deskripsi) values (?, ?,?, ?,?, ?,?,?, ?, ?,?)", (merk, model, tipe, harga,tahun, kota, provinsi, showroom, transmisi, warna, deskripsi))
    conn.commit()

    daftar_merk.append(str(merk))
    daftar_tipe.append(str(tipe))
    daftar_model.append(str(model))
    daftar_harga.append(int(harga))
    daftar_kota.append(str(kota))
    daftar_provinsi.append(str(provinsi))
    daftar_showroom.append(str(showroom))
    daftar_tahunmobil.append(str(merk))
    daftar_transmisimobil.append(str(transmisi))
    daftar_warnamobil.append(str(warna))
    daftar_deskripsi.append((deskripsi))




# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.

#c.execute('SELECT * FROM mobil_bekas')

#meida = c.fetchone()

#print (meida)


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
conn.close()


product_dict={'merk':daftar_merk,'model':daftar_model,'tipe':daftar_tipe,'harga':daftar_harga,'kota':daftar_kota,'provinsi':daftar_provinsi,'showroom':daftar_showroom,'tahun':daftar_tahunmobil,'warna':daftar_warnamobil,'transmisi':daftar_transmisimobil,'deskripsi':daftar_deskripsi}
#print(product_dict)
#data=pd.DataFrame(product_dict,columns=['merk','model','tipe','harga','kota','provinsi','showroom','tahun','warna','transmisi','deskripsi'])
#data.sort_values('harga',ascending=True)

#data.to_csv("Otomart.csv", sep=',' )