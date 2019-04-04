import urllib as link
import xlrd,xlsxwriter
'''
data.name = nama sheet
data.nrows = jumah baris
data.ncols = jumlah kolom
'''
excel = xlrd.open_workbook("tribunnews_daftarlinkberita.xlsx")
data = excel.sheet_by_index(0)

workbook = xlsxwriter.Workbook('tribunnews_daftarjuduldanisiberita.xlsx')
worksheet1 = workbook.add_worksheet()


import sqlite3

conn = sqlite3.connect('tribunnews.db')
c = conn.cursor()

    # Create table
c.execute('DROP TABLE IF EXISTS berita_gresik')
c.execute('''CREATE TABLE IF NOT EXISTS berita_gresik
                 (judul VARCHAR,isi VARCHAR)''')
conn.commit()
print(data.nrows)
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

    print(isi)
    c.execute("INSERT INTO berita_gresik (judul,isi) values ( ?,?)",(berita, isi))
    conn.commit()
    worksheet1.write(baris, 1, berita)
    worksheet1.write(baris, 2, isi)

workbook.close()
conn.close()