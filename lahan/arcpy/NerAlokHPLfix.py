#Name : NeracaHPL.py

#import System Modules
import arcpy
from arcpy import env


#set environment settings
workspace = arcpy.env.workspace
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

#Get Parameter as text
hpl = arcpy.GetParameterAsText(0)
hutanfix = arcpy.GetParameterAsText(1)
alokasi = arcpy.GetParameterAsText(2)
Kampungtua = arcpy.GetParameterAsText(3)
JALAN = arcpy.GetParameterAsText(4)
neraca = arcpy.GetParameterAsText(5)

#Dissolve HPL
HPL2 = arcpy.Dissolve_management(hpl,"HPL2", ["Status_1"], "", "MULTI_PART","")

#Intersect Hutan x HPL
hutHPL = arcpy.Intersect_analysis((HPL2, hutanfix), "hutHPL","ALL", "", "INPUT")

#erase Hutan x HPL
nhutHPL = arcpy.Erase_analysis(hutanfix,hutHPL,"nhutHPL")

#merge Hutan x HPL
fhutHPL = arcpy.Merge_management((nhutHPL, hutHPL), "fhutHPL")

#Dissolve Alokasi
fALOKASI = arcpy.Dissolve_management(alokasi,"fALOKASI", ["kondisi"], "", "MULTI_PART","")

#intersect Hutan x HPL x Alokasi
HutalHPL = arcpy.Intersect_analysis((fhutHPL, fALOKASI), "HutalHPL","ALL", "", "INPUT")

#erase Hutan x HPL x Alokasi
nHutalHPL = arcpy.Erase_analysis(fhutHPL, HutalHPL,"nHutHPL")

#Merge Hutan x Alokasi
fHutalHPL = arcpy.Merge_management((nHutalHPL, HutalHPL), "fHutalHPL")

#Intersect Hutan - WK - HPL - Kampung Tua
huthplkam = arcpy.Intersect_analysis((fHutalHPL, Kampungtua), "huthplkam","ALL", "", "INPUT")

#erase Hutan - WK - HPL - Kampung Tua
nhuthplkam = arcpy.Erase_analysis(fHutalHPL,huthplkam,"nhuthplkam")

#Merge Final (Hutan - WK - HPL - Kampung Tua)
fhuthplkam = arcpy.Merge_management((nhuthplkam, huthplkam), "fhuthplkam")

#intersect WkxHutanxNonhutan - Jalan
Hjalan = arcpy.Intersect_analysis((fhuthplkam,JALAN), "Hjalan","ALL", "", "INPUT")

#erase WkxHutanxNonhutan + WkxHutanxNonhutanxJalan
nHjalan = arcpy.Erase_analysis(fhuthplkam, Hjalan,"nHjalan")

#Merge WkxHutanxNonhutan + Jalan + NonjalanW
fHjalan = arcpy.Merge_management((Hjalan, nHjalan), "fHjalan")

#Dissolve HPL
neraca = arcpy.Dissolve_management(fHjalan,"neraca", ["Status_1", "Kelas", "Kampung", "kondisi","Ket"], "", "MULTI_PART","")

# klasifikasi untuk hpl
inTable = "neraca"
fieldName = "klasif"
expression = "calc(!Kelas!, !Status_1!, !kondisi!, !Kampung!, !Ket!, !klasif!)"

codeblock = """
def calc(a,b,c,d,e,f):
    if a==" " and b == "HPL" and c == "Sudah PL" and d == "Kampung" and e == "Jalan":
        f = "Bukan Hutan - Sudah HPL - Sudah PL - Kampung Tua - Jalan"
    elif a==" " and b == "HPL" and c == "Sudah PL" and d != "Kampung" and e == "Jalan":
        f = "Bukan Hutan - Sudah HPL - Sudah PL - Bukan Kampung Tua - Jalan"
    elif a==" " and b == "HPL" and c != "Sudah PL" and d == "Kampung" and e == "Jalan":
        f = "Bukan Hutan - Sudah HPL - Belum PL - Kampung Tua - Jalan"
    elif a==" " and b == "HPL" and c != "Sudah PL" and d != "Kampung" and e == "Jalan":
        f = "Bukan Hutan - Sudah HPL - Belum PL - Bukan Kampung Tua - Jalan"
    elif a==" " and b == "PROSES" and c == "Sudah PL" and d == "Kampung" and e == "Jalan":
        f = "Bukan Hutan - PROSES - Sudah PL - Kampung Tua - Jalan"
    elif a==" " and b == "PROSES" and c == "Sudah PL" and d != "Kampung" and e == "Jalan":
        f = "Bukan Hutan - PROSES - Sudah PL - Bukan Kampung Tua - Jalan"
    elif a==" " and b == "PROSES" and c != "Sudah PL" and d == "Kampung" and e == "Jalan":
        f = "Bukan Hutan - PROSES - Belum PL - Kampung Tua - Jalan"
    elif a==" " and b == "PROSES" and c != "Sudah PL" and d != "Kampung" and e == "Jalan":
        f = "Bukan Hutan - PROSES - Belum PL - Bukan Kampung Tua - Jalan"
    elif a==" " and b != "PROSES" and b != "HPL" and c == "Sudah PL" and d == "Kampung" and e == "Jalan":
        f = "Bukan Hutan - Belum HPL - Sudah PL - Kampung Tua - Jalan"
    elif a==" " and b != "PROSES" and b != "HPL" and c == "Sudah PL" and d != "Kampung" and e == "Jalan":
        f = "Bukan Hutan - Belum HPL - Sudah PL - Bukan Kampung Tua - Jalan"
    elif a==" " and b != "PROSES" and b != "HPL" and c != "Sudah PL" and d == "Kampung" and e == "Jalan":
        f = "Bukan Hutan - Belum HPL - Belum PL - Kampung Tua - Jalan"
    elif a==" " and b != "PROSES" and b != "HPL" and c != "Sudah PL" and d != "Kampung" and e == "Jalan":
        f = "Bukan Hutan - Belum HPL - Belum PL - Bukan Kampung Tua - Jalan"
    elif a!=" " and b == "HPL" and c == "Sudah PL" and d == "Kampung" and e == "Jalan":
        f = "Hutan - Sudah HPL - Sudah PL - Kampung Tua - Jalan"
    elif a!=" " and b == "HPL" and c == "Sudah PL" and d != "Kampung" and e == "Jalan":
        f = "Hutan - Sudah HPL - Sudah PL - Bukan Kampung Tua - Jalan"
    elif a!=" " and b == "HPL" and c != "Sudah PL" and d == "Kampung" and e == "Jalan":
        f = "Hutan - Sudah HPL - Belum PL - Kampung Tua - Jalan"
    elif a!=" " and b == "HPL" and c != "Sudah PL" and d != "Kampung" and e == "Jalan":
        f = "Hutan - Sudah HPL - Belum PL - Bukan Kampung Tua - Jalan"
    elif a!=" " and b == "PROSES" and c == "Sudah PL" and d == "Kampung" and e == "Jalan":
        f = "Hutan - PROSES - Sudah PL - Kampung Tua - Jalan"
    elif a!=" " and b == "PROSES" and c == "Sudah PL" and d != "Kampung" and e == "Jalan":
        f = "Hutan - PROSES - Sudah PL - Bukan Kampung Tua - Jalan"
    elif a!=" " and b == "PROSES" and c != "Sudah PL" and d == "Kampung" and e == "Jalan":
        f = "Hutan - PROSES - Belum PL - Kampung Tua - Jalan"
    elif a!=" " and b == "PROSES" and c != "Sudah PL" and d != "Kampung" and e == "Jalan":
        f = "Hutan - PROSES - Belum PL - Bukan Kampung Tua - Jalan"
    elif a!=" " and b != "PROSES" and b != "HPL" and c == "Sudah PL" and d == "Kampung" and e == "Jalan":
        f = "Hutan - Belum HPL - Sudah PL - Kampung Tua - Jalan"
    elif a!=" " and b != "PROSES" and b != "HPL" and c == "Sudah PL" and d != "Kampung" and e == "Jalan":
        f = "Hutan - Belum HPL - Sudah PL - Bukan Kampung Tua - Jalan"
    elif a!=" " and b != "PROSES" and b != "HPL" and c != "Sudah PL" and d == "Kampung" and e == "Jalan":
        f = "Hutan - Belum HPL - Belum PL - Kampung Tua - Jalan"
    elif a!=" " and b != "PROSES" and b != "HPL" and c != "Sudah PL" and d != "Kampung" and e == "Jalan":
        f = "Hutan - Belum HPL - Belum PL - Bukan Kampung Tua - Jalan"
    elif a==" " and b == "HPL" and c == "Sudah PL" and d == "Kampung" and e != "Jalan":
        f = "Bukan Hutan - Sudah HPL - Sudah PL - Kampung Tua - Non Jalan"
    elif a==" " and b == "HPL" and c == "Sudah PL" and d != "Kampung" and e != "Jalan":
        f = "Bukan Hutan - Sudah HPL - Sudah PL - Bukan Kampung Tua - Non Jalan"
    elif a==" " and b == "HPL" and c != "Sudah PL" and d == "Kampung" and e != "Jalan":
        f = "Bukan Hutan - Sudah HPL - Belum PL - Kampung Tua - Non Jalan"
    elif a==" " and b == "HPL" and c != "Sudah PL" and d != "Kampung" and e != "Jalan":
        f = "Bukan Hutan - Sudah HPL - Belum PL - Bukan Kampung Tua - Non Jalan"
    elif a==" " and b == "PROSES" and c == "Sudah PL" and d == "Kampung" and e != "Jalan":
        f = "Bukan Hutan - PROSES - Sudah PL - Kampung Tua - Non Jalan"
    elif a==" " and b == "PROSES" and c == "Sudah PL" and d != "Kampung" and e != "Jalan":
        f = "Bukan Hutan - PROSES - Sudah PL - Bukan Kampung Tua - Non Jalan"
    elif a==" " and b == "PROSES" and c != "Sudah PL" and d == "Kampung" and e != "Jalan":
        f = "Bukan Hutan - PROSES - Belum PL - Kampung Tua - Non Jalan"
    elif a==" " and b == "PROSES" and c != "Sudah PL" and d != "Kampung" and e != "Jalan":
        f = "Bukan Hutan - PROSES - Belum PL - Bukan Kampung Tua - Non Jalan"
    elif a==" " and b != "PROSES" and b != "HPL" and c == "Sudah PL" and d == "Kampung" and e != "Jalan":
        f = "Bukan Hutan - Belum HPL - Sudah PL - Kampung Tua - Non Jalan"
    elif a==" " and b != "PROSES" and b != "HPL" and c == "Sudah PL" and d != "Kampung" and e != "Jalan":
        f = "Bukan Hutan - Belum HPL - Sudah PL - Bukan Kampung Tua - Non Jalan"
    elif a==" " and b != "PROSES" and b != "HPL" and c != "Sudah PL" and d == "Kampung" and e != "Jalan":
        f = "Bukan Hutan - Belum HPL - Belum PL - Kampung Tua - Non Jalan"
    elif a==" " and b != "PROSES" and b != "HPL" and c != "Sudah PL" and d != "Kampung" and e != "Jalan":
        f = "Bukan Hutan - Belum HPL - Belum PL - Bukan Kampung Tua - Non Jalan"
    elif a!=" " and b == "HPL" and c == "Sudah PL" and d == "Kampung" and e != "Jalan":
        f = "Hutan - Sudah HPL - Sudah PL - Kampung Tua - Non Jalan"
    elif a!=" " and b == "HPL" and c == "Sudah PL" and d != "Kampung" and e != "Jalan":
        f = "Hutan - Sudah HPL - Sudah PL - Bukan Kampung Tua - Non Jalan"
    elif a!=" " and b == "HPL" and c != "Sudah PL" and d == "Kampung" and e != "Jalan":
        f = "Hutan - Sudah HPL - Belum PL - Kampung Tua - Non Jalan"
    elif a!=" " and b == "HPL" and c != "Sudah PL" and d != "Kampung" and e != "Jalan":
        f = "Hutan - Sudah HPL - Belum PL - Bukan Kampung Tua - Non Jalan"
    elif a!=" " and b == "PROSES" and c == "Sudah PL" and d == "Kampung" and e != "Jalan":
        f = "Hutan - PROSES - Sudah PL - Kampung Tua - Non Jalan"
    elif a!=" " and b == "PROSES" and c == "Sudah PL" and d != "Kampung" and e != "Jalan":
        f = "Hutan - PROSES - Sudah PL - Bukan Kampung Tua - Non Jalan"
    elif a!=" " and b == "PROSES" and c != "Sudah PL" and d == "Kampung" and e != "Jalan":
        f = "Hutan - PROSES - Belum PL - Kampung Tua - Non Jalan"
    elif a!=" " and b == "PROSES" and c != "Sudah PL" and d != "Kampung" and e != "Jalan":
        f = "Hutan - PROSES - Belum PL - Bukan Kampung Tua - Non Jalan"
    elif a!=" " and b != "PROSES" and b != "HPL" and c == "Sudah PL" and d == "Kampung" and e != "Jalan":
        f = "Hutan - Belum HPL - Sudah PL - Kampung Tua - Non Jalan"
    elif a!=" " and b != "PROSES" and b != "HPL" and c == "Sudah PL" and d != "Kampung" and e != "Jalan":
        f = "Hutan - Belum HPL - Sudah PL - Bukan Kampung Tua - Non Jalan"
    elif a!=" " and b != "PROSES" and b != "HPL" and c != "Sudah PL" and d == "Kampung" and e != "Jalan":
        f = "Hutan - Belum HPL - Belum PL - Kampung Tua - Non Jalan"
    elif a!=" " and b != "PROSES" and b != "HPL" and c != "Sudah PL" and d != "Kampung" and e != "Jalan":
        f = "Hutan - Belum HPL - Belum PL - Bukan Kampung Tua - Non Jalan"
    return f

"""

# tambah kolom klasif
arcpy.AddField_management(inTable, fieldName, 'TEXT', '','',255,'KLASIFIKASI','NULLABLE','')

# Execute CalculateField
arcpy.CalculateField_management(inTable, fieldName, expression, "PYTHON3", codeblock)

# Set local variables
inTable = "neraca"
fieldName = "hasil"
expression = "calc(!klasif!, !hasil!)"

codeblock = """
def calc(a,b):
    if a=="Bukan Hutan - Belum HPL - Belum PL - Bukan Kampung Tua - Jalan":
        b="Jalan"
    elif a=="Bukan Hutan - Belum HPL - Belum PL - Bukan Kampung Tua - Non Jalan":
        b="Potensi Alokasi"
    elif a=="Bukan Hutan - Belum HPL - Belum PL - Kampung Tua - Jalan":
        b="Jalan"
    elif a=="Bukan Hutan - Belum HPL - Belum PL - Kampung Tua - Non Jalan":
        b="Kampung Tua"
    elif a=="Bukan Hutan - Belum HPL - Sudah PL - Bukan Kampung Tua - Jalan":
        b="Teralokasi di Jalan"
    elif a=="Bukan Hutan - Belum HPL - Sudah PL - Bukan Kampung Tua - Non Jalan":
        b="Teralokasi belum HPL"
    elif a=="Bukan Hutan - Belum HPL - Sudah PL - Kampung Tua - Jalan":
        b="Teralokasi di Jalan"
    elif a=="Bukan Hutan - Belum HPL - Sudah PL - Kampung Tua - Non Jalan":
        b="Kampung Tua"
    elif a=="Bukan Hutan - PROSES - Belum PL - Bukan Kampung Tua - Jalan":
        b="Jalan"
    elif a=="Bukan Hutan - PROSES - Belum PL - Bukan Kampung Tua - Non Jalan":
        b="Potensi Alokasi"
    elif a=="Bukan Hutan - PROSES - Belum PL - Kampung Tua - Jalan":
        b="Jalan"
    elif a=="Bukan Hutan - PROSES - Belum PL - Kampung Tua - Non Jalan":
        b="Kampung Tua"
    elif a=="Bukan Hutan - PROSES - Sudah PL - Bukan Kampung Tua - Jalan":
        b="Teralokasi di Jalan"
    elif a=="Bukan Hutan - PROSES - Sudah PL - Bukan Kampung Tua - Non Jalan":
        b="Teralokasi"
    elif a=="Bukan Hutan - PROSES - Sudah PL - Kampung Tua - Jalan":
        b="Teralokasi di Jalan"
    elif a=="Bukan Hutan - PROSES - Sudah PL - Kampung Tua - Non Jalan":
        b="Kampung Tua"
    elif a=="Bukan Hutan - Sudah HPL - Belum PL - Bukan Kampung Tua - Jalan":
        b="Jalan"
    elif a=="Bukan Hutan - Sudah HPL - Belum PL - Bukan Kampung Tua - Non Jalan":
        b="Potensi Alokasi"
    elif a=="Bukan Hutan - Sudah HPL - Belum PL - Kampung Tua - Jalan":
        b="Jalan"
    elif a=="Bukan Hutan - Sudah HPL - Belum PL - Kampung Tua - Non Jalan":
        b="Kampung Tua"
    elif a=="Bukan Hutan - Sudah HPL - Sudah PL - Bukan Kampung Tua - Jalan":
        b="Teralokasi di Jalan"
    elif a=="Bukan Hutan - Sudah HPL - Sudah PL - Bukan Kampung Tua - Non Jalan":
        b="Teralokasi"
    elif a=="Bukan Hutan - Sudah HPL - Sudah PL - Kampung Tua - Jalan":
        b="Teralokasi di Jalan"
    elif a=="Bukan Hutan - Sudah HPL - Sudah PL - Kampung Tua - Non Jalan":
        b="Kampung Tua"
    elif a=="Hutan - Belum HPL - Belum PL - Bukan Kampung Tua - Jalan":
        b="Jalan"
    elif a=="Hutan - Belum HPL - Belum PL - Bukan Kampung Tua - Non Jalan":
        b="Hutan"
    elif a=="Hutan - Belum HPL - Belum PL - Kampung Tua - Jalan":
        b="Jalan"
    elif a=="Hutan - Belum HPL - Belum PL - Kampung Tua - Non Jalan":
        b="Kampung Tua"
    elif a=="Hutan - Belum HPL - Sudah PL - Bukan Kampung Tua - Jalan":
        b="Teralokasi di Jalan"
    elif a=="Hutan - Belum HPL - Sudah PL - Bukan Kampung Tua - Non Jalan":
        b="Teralokasi di Hutan"
    elif a=="Hutan - Belum HPL - Sudah PL - Kampung Tua - Jalan":
        b="Teralokasi di Jalan"
    elif a=="Hutan - Belum HPL - Sudah PL - Kampung Tua - Non Jalan":
        b="Kampung Tua"
    elif a=="Hutan - PROSES - Belum PL - Bukan Kampung Tua - Jalan":
        b="Jalan"
    elif a=="Hutan - PROSES - Belum PL - Bukan Kampung Tua - Non Jalan":
        b="Proses HPL di Hutan"
    elif a=="Hutan - PROSES - Belum PL - Kampung Tua - Non Jalan":
        b="Kampung Tua"
    elif a=="Hutan - PROSES - Sudah PL - Bukan Kampung Tua - Jalan":
        b="Teralokasi di Jalan"
    elif a=="Hutan - PROSES - Sudah PL - Bukan Kampung Tua - Non Jalan":
        b="Teralokasi di Hutan"
    elif a=="Hutan - PROSES - Sudah PL - Kampung Tua - Non Jalan":
        b="Kampung Tua"
    elif a=="Hutan - Sudah HPL - Belum PL - Bukan Kampung Tua - Jalan":
        b="Jalan"
    elif a=="Hutan - Sudah HPL - Belum PL - Bukan Kampung Tua - Non Jalan":
        b="Sudah HPL di Hutan"
    elif a=="Hutan - Sudah HPL - Belum PL - Kampung Tua - Jalan":
        b="Jalan"
    elif a=="Hutan - Sudah HPL - Belum PL - Kampung Tua - Non Jalan":
        b="Kampung Tua"
    elif a=="Hutan - Sudah HPL - Sudah PL - Bukan Kampung Tua - Jalan":
        b="Teralokasi di Jalan"
    elif a=="Hutan - Sudah HPL - Sudah PL - Bukan Kampung Tua - Non Jalan":
        b="Teralokasi di Hutan"
    elif a=="Hutan - Sudah HPL - Sudah PL - Kampung Tua - Jalan":
        b="Teralokasi di Jalan"
    elif a=="Hutan - Sudah HPL - Sudah PL - Kampung Tua - Non Jalan":
        b="Kampung Tua"
    return b
"""

# tambah kolom klasif
arcpy.AddField_management(inTable, fieldName, 'TEXT', '','',255,'Klasif neraca','NULLABLE','')

# Execute CalculateField
arcpy.CalculateField_management(inTable, fieldName, expression, "PYTHON3", codeblock)

aprx = arcpy.mp.ArcGISProject("CURRENT")
m = aprx.listMaps()[0]
akhirat = arcpy.MakeFeatureLayer_management(neraca, "Neraca_Alokasi_HPL")
neracalokasi5 = akhirat.getOutput(0)
m.addLayer(neracalokasi5)




