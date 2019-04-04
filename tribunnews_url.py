import xlsxwriter

workbook = xlsxwriter.Workbook('tribunnews_daftarlinkberita.xlsx')
worksheet1 = workbook.add_worksheet()
kumpulan_link=[]

def cari_link(page):
    import urllib as link
    from bs4 import BeautifulSoup
    import re
    print (page)
    html_page = link.urlopen("http://surabaya.tribunnews.com/topic/berita-gresik?&page="+str(page)).read()
    soup = BeautifulSoup(html_page, "lxml")

    for a in soup.findAll('h3', 'f20 ln24 fbo'):
        for link in a.findAll('a', attrs={'href': re.compile("^http://")}):
            #print link.get('href')
            kumpulan_link.append(link.get('href'))

for i in range(1,6):
    cari_link(str(i))
print len(kumpulan_link)

for baris in range(len(kumpulan_link)):
    print (baris)
    print (kumpulan_link[baris])
    worksheet1.write(baris,1, str(kumpulan_link[baris]))
workbook.close()
