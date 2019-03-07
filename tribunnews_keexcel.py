import xlsxwriter
import tribunnews_sastrawi

workbook = xlsxwriter.Workbook('tribunnews_rabu.xlsx')
worksheet1 = workbook.add_worksheet()



for j in range(tribunnews_sastrawi.a):
    worksheet1.write(j + 1,0,str(j+1))

worksheet1.write(0 ,0, "data ke")
#tulis fitur kata ke excel
for i in range(len(tribunnews_sastrawi.list_fitur())):
    # print i
    fitur = str(tribunnews_sastrawi.list_fitur().keys()[i])
    # print fitur
    worksheet1.write(0, i + 1, str(fitur))

print (len(tribunnews_sastrawi.data))
for baris in range(len(tribunnews_sastrawi.data)):
    for kolom in range(len(tribunnews_sastrawi.list_fitur())):
        fitur = tribunnews_sastrawi.coba1()[baris].values()[kolom]
        print ("data ke > " + str(baris + 1) + " kata " + str(tribunnews_sastrawi.coba1()[baris].keys()[kolom]) + " sebanyak " + str(
            tribunnews_sastrawi.coba1()[baris].values()[kolom]))
        worksheet1.write(baris + 1, kolom + 1, int(fitur))
workbook.close()

