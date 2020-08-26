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
Kampungtua = arcpy.GetParameterAsText(2)
NeracaHPL = arcpy.GetParameterAsText(3)

#Dissolve HPL
HPLdiss = arcpy.Dissolve_management(hpl,"HPLdiss", ["STATUS_1"], "", "MULTI_PART","")

#Intersect Hutan x WK X Nonhutan x HPL
hutanxhpl = arcpy.Intersect_analysis((HPLdiss, hutanfix), "hutanxhpl","ALL", "", "INPUT")

#erase WkxnonHutanxHutan - WKxHutanxnonHutanxHPL
hutanxnonhpl = arcpy.Erase_analysis(hutanfix,hutanxhpl,"hutanxnonhpl")

#merge hutan - wk - hpl
fhuthpl = arcpy.Merge_management((hutanxnonhpl, hutanxhpl), "fhuthpl")

#Intersect Hutan - WK - HPL - Kampung Tua
huthplkam = arcpy.Intersect_analysis((fhuthpl, Kampungtua), "huthplkam","ALL", "", "INPUT")

#erase Hutan - WK - HPL - Kampung Tua
nhuthplkam = arcpy.Erase_analysis(fhuthpl,huthplkam,"nhuthplkam")

#Merge Final (Hutan - WK - HPL - Kampung Tua)
fhuthplkam = arcpy.Merge_management((nhuthplkam, huthplkam), "fhuthplkam")

#Dissolve HPL
NeracaHPL = arcpy.Dissolve_management(fhuthplkam,"NeracaHPL", ["Status_1", "Kelas", "Kampung"], "", "MULTI_PART","")

# klasifikasi untuk hpl
inTable = "NeracaHPL"
fieldName = "klasif"
expression = "calc(!Kelas!,!Status_1!,!Kampung!, !klasif!)"

codeblock = """
def calc(a,b,c,d):
    if a==" " and b == "HPL" and c == "Kampung":
        d = "Bukan Hutan - HPL - Kampung Tua"
    elif a==" " and b == "HPL" and c != "Kampung":
        d = "Bukan Hutan - HPL - Bukan Kampung Tua"
    elif a==" " and b == "PROSES" and c == "Kampung":
        d = "Bukan Hutan - PROSES - Kampung"
    elif a==" " and b == "PROSES" and c != "Kampung":
        d = "Bukan Hutan - PROSES - Bukan Kampung Tua"
    elif a==" " and b != "PROSES" and b != "HPL" and c == "Kampung":
        d = "Bukan Hutan - Belum HPL - Kampung"
    elif a==" " and b != "PROSES" and b != "HPL" and c != "Kampung":
        d = "Bukan Hutan - Belum HPL - Bukan Kampung Tua"
    elif a!=" " and b == "HPL" and c == "Kampung":
        d = "Hutan - HPL - Kampung Tua"
    elif a!=" " and b == "HPL" and c != "Kampung":
        d = "Hutan - HPL - Bukan Kampung Tua"
    elif a!=" " and b == "PROSES" and c == "Kampung":
        d = "Hutan - PROSES - Kampung"
    elif a!=" " and b == "PROSES" and c != "Kampung":
        d = "Hutan - PROSES - Bukan Kampung Tua"
    elif a!=" " and b != "PROSES" and b != "HPL" and c == "Kampung":
        d = "Hutan - Belum HPL - Kampung"
    elif a!=" " and b != "PROSES" and b != "HPL" and c != "Kampung":
        d = "Hutan - Belum HPL - Bukan Kampung Tua"
    return d
"""

# tambah kolom klasif
arcpy.AddField_management(inTable, fieldName, 'TEXT', '','',255,'KLASIFIKASI','NULLABLE','')

# Execute CalculateField
arcpy.CalculateField_management(inTable, fieldName, expression, "PYTHON3", codeblock)

# Set local variables
inTable = "NeracaHPL"
fieldName = "hasil"
expression = "calc(!klasif!, !hasil!)"

codeblock = """
def calc(a,b):
    if a=="Bukan Hutan - Belum HPL - Bukan Kampung Tua":
        b="Potensi HPL"
    elif a=="Bukan Hutan - Belum HPL - Kampung":
        b="Kampung Tua"
    elif a=="Bukan Hutan - HPL - Bukan Kampung Tua":
        b="Sudah HPL"
    elif a=="Bukan Hutan - HPL - Kampung Tua":
        b="Kampung Tua"
    elif a=="Bukan Hutan - PROSES - Bukan Kampung Tua":
        b="Proses HPL"
    elif a=="Bukan Hutan - PROSES - Kampung":
        b="Kampung Tua"
    elif a=="Hutan - Belum HPL - Bukan Kampung Tua":
        b="Hutan"
    elif a=="Hutan - Belum HPL - Kampung":
        b="Kampung Tua di Hutan"
    elif a=="Hutan - HPL - Bukan Kampung Tua":
        b="HPL di Hutan"
    elif a=="Hutan - HPL - Kampung Tua":
        b="Kampung Tua di Hutan"
    elif a=="Hutan - PROSES - Bukan Kampung Tua":
        b="Proses di Hutan"
    elif a=="Hutan - PROSES - Kampung":
        b="Kampung Tua di Hutan"
    return b
"""

# tambah kolom klasif
arcpy.AddField_management(inTable, fieldName, 'TEXT', '','',255,'Klasif neraca','NULLABLE','')

# Execute CalculateField
arcpy.CalculateField_management(inTable, fieldName, expression, "PYTHON3", codeblock)

aprx = arcpy.mp.ArcGISProject("CURRENT")
m = aprx.listMaps()[0]
akhir = arcpy.MakeFeatureLayer_management(NeracaHPL, "NeracaHPL")
neracalokasi = akhir.getOutput(0)
m.addLayer(neracalokasi)
