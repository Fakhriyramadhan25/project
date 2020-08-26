#Name : NeracaAlokasi.py

#import System Modules
import arcpy
from arcpy import env

#set environment settings
workspace = arcpy.env.workspace
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

#Get Parameter as text
hutan = arcpy.GetParameterAsText(0)
alokasi = arcpy.GetParameterAsText(1)
KampungTua = arcpy.GetParameterAsText(2)
JALAN = arcpy.GetParameterAsText(3)
neracalokasi = arcpy.GetParameterAsText(4)

#Dissolve Hutan
hutanfix = arcpy.Dissolve_management(hutan,"hutanfix", ["Kelas"], "", "MULTI_PART","")

#intersect Hutan x Alokasi
hutal = arcpy.Intersect_analysis((hutanfix,alokasi), "hutal","ALL", "", "INPUT")

#erase Hutan x Alokasi
nhutal = arcpy.Erase_analysis(hutanfix, hutal,"nhutal")

#Merge Hutan x Alokasi
fhutal = arcpy.Merge_management((nhutal, hutal), "fhutal")

#intersect Hutan x Alokasi x Kampung Tua
HutHPLKT = arcpy.Intersect_analysis((fhutal, KampungTua), "HutHPLKT","ALL", "", "INPUT")

#erase Hutan x HPL x Alokasi x Kampung Tua
nHutHPLKT = arcpy.Erase_analysis(fhutal, HutHPLKT,"nHutHPLKT")

#Merge Hutan x HPL x Alokasi x Kampung Tua
fHutHPLKT = arcpy.Merge_management((nHutHPLKT, HutHPLKT), "fHutHPLKT")

#intersect WkxHutanxNonhutan - Jalan
Hjalan = arcpy.Intersect_analysis((fHutHPLKT,JALAN), "Hjalan","ALL", "", "INPUT")

#erase WkxHutanxNonhutan + WkxHutanxNonhutanxJalan
nHjalan = arcpy.Erase_analysis(fHutHPLKT, Hjalan,"nHjalan")

#Merge WkxHutanxNonhutan + Jalan + NonjalanW
fHjalan = arcpy.Merge_management((Hjalan, nHjalan), "fHjalan")

#Dissolve hasil
neracalokasi = arcpy.Dissolve_management(fHjalan,"neracalokasi", ["Ket","kondisi","Kelas","Kampung"], "", "MULTI_PART","")

# klasifikasi untuk hpl
inTable = "neracalokasi"
fieldName = "klasif"
expression = "calc(!Kelas!, !kondisi!, !Kampung!, !Ket!, !klasif!)"

codeblock = """
def calc(a,b,c,d,e):
    if c == 'Kampung' and b == 'Sudah PL' and d == 'Jalan' and a == ' ':
        e = 'Bukan Hutan - Sudah PL - Jalan - Kampung Tua'
    elif c != 'Kampung' and b == 'Sudah PL' and d == 'Jalan' and a == ' ':
        e = 'Bukan Hutan - Sudah PL - Jalan - Bukan Kampung Tua'
    elif c != 'Kampung' and b == 'Sudah PL' and d != 'Jalan' and a == ' ':
        e = 'Bukan Hutan - Sudah PL - Bukan Jalan - Bukan Kampung Tua'
    elif c == 'Kampung' and b == 'Sudah PL' and d != 'Jalan' and a == ' ':
        e = 'Bukan Hutan - Sudah PL - Bukan Jalan - Kampung Tua'
    elif c == 'Kampung' and b != 'Sudah PL' and d == 'Jalan' and a == ' ':
        e = 'Bukan Hutan - Belum PL - Jalan - Kampung Tua'
    elif c != 'Kampung' and b != 'Sudah PL' and d == 'Jalan' and a == ' ':
        e = 'Bukan Hutan - Belum PL - Jalan - Bukan Kampung Tua'
    elif c != 'Kampung' and b != 'Sudah PL' and d != 'Jalan' and a == ' ':
        e = 'Bukan Hutan - Belum PL - Bukan Jalan - Bukan Kampung Tua'
    elif c == 'Kampung' and b != 'Sudah PL' and d != 'Jalan' and a == ' ':
        e = 'Bukan Hutan - Belum PL - Bukan Jalan - Kampung Tua'
    elif c == 'Kampung' and b == 'Sudah PL' and d == 'Jalan' and a != ' ':
        e = 'Hutan - Sudah PL - Jalan - Kampung Tua'
    elif c != 'Kampung' and b == 'Sudah PL' and d == 'Jalan' and a != ' ':
        e = 'Hutan - Sudah PL - Jalan - Bukan Kampung Tua'
    elif c != 'Kampung' and b == 'Sudah PL' and d != 'Jalan' and a != ' ':
        e = 'Hutan - Sudah PL - Bukan Jalan - Bukan Kampung Tua'
    elif c == 'Kampung' and b == 'Sudah PL' and d != 'Jalan' and a != ' ':
        e = 'Hutan - Sudah PL - Bukan Jalan - Kampung Tua'
    elif c == 'Kampung' and b != 'Sudah PL' and d == 'Jalan' and a != ' ':
        e = 'Hutan - Belum PL - Jalan - Kampung Tua'
    elif c != 'Kampung' and b != 'Sudah PL' and d == 'Jalan' and a != ' ':
        e = 'Hutan - Belum PL - Jalan - Bukan Kampung Tua'
    elif c != 'Kampung' and b != 'Sudah PL' and d != 'Jalan' and a != ' ':
        e = 'Hutan - Belum PL - Bukan Jalan - Bukan Kampung Tua'
    elif c == 'Kampung' and b != 'Sudah PL' and d != 'Jalan' and a != ' ':
        e = 'Hutan - Belum PL - Bukan Jalan - Kampung Tua'
    return e
"""

# tambah kolom klasif
arcpy.AddField_management(inTable, fieldName, 'TEXT', '','',255,'neracalokasi','NULLABLE','')

# Execute CalculateField
arcpy.CalculateField_management(inTable, fieldName, expression, "PYTHON3", codeblock)

# Set local variables
inTable = "neracalokasi"
fieldName = "hasil"
expression = "calc(!klasif!, !hasil!)"

codeblock = """
def calc(a,b):
    if a=="Bukan Hutan - Belum PL - Bukan Jalan - Bukan Kampung Tua":
        b="Potensi Alokasi"
    elif a=="Bukan Hutan - Belum PL - Bukan Jalan - Kampung Tua":
        b="Kampung Tua"
    elif a=="Bukan Hutan - Belum PL - Jalan - Bukan Kampung Tua":
        b="Jalan"
    elif a=="Bukan Hutan - Belum PL - Jalan - Kampung Tua":
        b="Jalan"
    elif a=="Bukan Hutan - Sudah PL - Bukan Jalan - Bukan Kampung Tua":
        b="Sudah Alokasi"
    elif a=="Bukan Hutan - Sudah PL - Bukan Jalan - Kampung Tua":
        b="Teralokasi di Kampung Tua"
    elif a=="Bukan Hutan - Sudah PL - Jalan - Bukan Kampung Tua":
        b="Teralokasi di Jalan"
    elif a=="Bukan Hutan - Sudah PL - Jalan - Kampung Tua":
        b="Teralokasi di Jalan"
    elif a=="Hutan - Belum PL - Bukan Jalan - Bukan Kampung Tua":
        b="Hutan"
    elif a=="Hutan - Belum PL - Bukan Jalan - Kampung Tua":
        b="Hutan di Kampung Tua"
    elif a=="Hutan - Belum PL - Jalan - Bukan Kampung Tua":
        b="Jalan"
    elif a=="Hutan - Belum PL - Jalan - Kampung Tua":
        b="Jalan"
    elif a=="Hutan - Sudah PL - Bukan Jalan - Bukan Kampung Tua":
        b="Teralokasi di Hutan"
    elif a=="Hutan - Sudah PL - Bukan Jalan - Kampung Tua":
        b="Teralokasi dan Hutan di Kampung Tua"
    elif a=="Hutan - Sudah PL - Jalan - Bukan Kampung Tua":
        b="Teralokasi di Jalan"
    elif a=="Hutan - Sudah PL - Jalan - Kampung Tua":
        b="Teralokasi di Jalan"
    return b
"""

# tambah kolom klasif
arcpy.AddField_management(inTable, fieldName, 'TEXT', '','',255,'Klasif neraca','NULLABLE','')

# Execute CalculateField
arcpy.CalculateField_management(inTable, fieldName, expression, "PYTHON3", codeblock)

#State and activate the layer
aprx = arcpy.mp.ArcGISProject("CURRENT")
m = aprx.listMaps()[0]
akhir = arcpy.MakeFeatureLayer_management(neracalokasi, "neraca_alokasi")
neracalokasi = akhir.getOutput(0)
m.addLayer(neracalokasi)
