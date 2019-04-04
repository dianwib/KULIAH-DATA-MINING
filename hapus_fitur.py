import xlsxwriter
import xlrd
excel = xlrd.open_workbook("tribunnews_daftarsteaming.xlsx")
sheetdata = excel.sheet_by_index(0)
'''
data.name = nama sheet
data.nrows = jumah baris
data.ncols = jumlah kolom
'''

workbook = xlsxwriter.Workbook('tribunnews_daftarsteaming_palingseringmuncul.xlsx')
worksheet1 = workbook.add_worksheet()


def cek(baris):
    value = sheetdata.cell_value(rowx=baris, colx=2)
    kalimat=value.split(" ")
    banyak={}
    temp_kata=""

    for kata in kalimat:
        for kata_lawan in kalimat:
            #print (kata)
            kata=str(kata)
            #print (kata_lawan)
            if str(kata)==str(kata_lawan):
                if kata not in banyak:
                    banyak[kata]=1
                else:
                    temp=banyak[kata]
                    banyak[kata] = temp + 1
            else:
                continue
        if banyak[kata]<4:
            del banyak[kata]

    for kata in banyak.keys():
        temp_kata+=kata+" "
            #print (banyak[kata])


    print (banyak)
    return temp_kata


for i in range(1,sheetdata.nrows-130):

    worksheet1.write(i,2,cek(i))
workbook.close()


