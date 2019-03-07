import xlsxwriter

import re
import tribunnews_ambilfitur


from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

data = []
kumpulan_katadasar = ""
a=0
wworkbook = xlsxwriter.Workbook('tribunnews_sastrawi.xlsx')
wworksheet1 = wworkbook.add_worksheet()

for kalimat in tribunnews_ambilfitur.data:

    a+=1
    print (a,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (kalimat)
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    kalimat = kalimat.encode('utf-8').strip()
    katadasar = stemmer.stem(str(kalimat))
    wworksheet1.write(a, 0, str(kalimat))

    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    stop = stopword.remove(katadasar)

    stop = re.sub(r'\b\w{1,3}\b', '', stop)
    print(stop)
    data.append(stop)
    wworksheet1.write(a, 1, str(stop))
    kumpulan_katadasar = kumpulan_katadasar + stop

temp = {}
kal = kumpulan_katadasar.split(" ")
wworkbook.close()
for i in kal:
    if i not in temp:
        temp[i] = 1
    else:
        hasil_sementara = temp[i]
        temp[i] = hasil_sementara + 1


# print (temp)


def list_fitur():
    t = {}
    semua_kata = ""
    for i in data:
        semua_kata = semua_kata + i + " "

    for j in semua_kata.split(" "):
        t[j] = 0

    del t[""]
    return t


def coba1():
    tt = []

    for kalimat in data:
        list_kata = kalimat.split(" ")

        a = list_fitur()
        for kata in list_kata:
            if kata not in list_fitur():
                a[kata] = 0
            else:
                temp = a[kata]
                a[kata] = temp + 1

        tt.append(a)

        # print (kalimat)

        # print (a)
    return tt


print coba1()
print len(list_fitur())
print list_fitur()
print (str(coba1()[2].values()[1]))

