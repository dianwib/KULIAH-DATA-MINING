import xlsxwriter
import xlrd
excel = xlrd.open_workbook("tribunnews_vsmsatufitur.xlsx")
sheetdata = excel.sheet_by_index(0)
'''
data.name = nama sheet
data.nrows = jumah baris
data.ncols = jumlah kolom
'''


workbook = xlsxwriter.Workbook('tribunnews_vsmsatufitur_cekhapusfitur.xlsx')
worksheet1 = workbook.add_worksheet()


for kolom in range(1,sheetdata.ncols):
    for baris in range(1, sheetdata.nrows):
        value = sheetdata.cell_value(rowx=kolom, colx=baris)

        for baris_lawan in range(baris+1, sheetdata.nrows-1):
            value_pembangding = sheetdata.cell_value(rowx=kolom, colx=baris)

            if value == value_pembangding:
                break
            else:
                






