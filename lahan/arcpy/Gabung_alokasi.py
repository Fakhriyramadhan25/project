#Name : Gabung alokasi.py
#import System Modules
import arcpy
from arcpy import env

#set environment settings
workspace = arcpy.env.workspace
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

#Get Parameter as text
induk = arcpy.GetParameterAsText(0)
KSB = arcpy.GetParameterAsText(1)
pecahan = arcpy.GetParameterAsText(2)
proses = arcpy.GetParameterAsText(3)
alokasi = arcpy.GetParameterAsText(4)

#erase induk - pecahan
inpec = arcpy.Erase_analysis(pecahan,induk,"inpec")

#merge induk x pecahan
finpec = arcpy.Merge_management((inpec, induk), "finpec")

#erase induk x pecahan - ksb
inksb = arcpy.Erase_analysis(finpec,KSB,"inksb")

#merge induk x pecahan x ksb
finpk = arcpy.Merge_management((finpec, inksb), "finpk")

#erase induk x pecahan x ksb - proses
inpro = arcpy.Erase_analysis(finpk, proses,"inpro")

#merge induk x pecahan x ksb x proses
finpkpro = arcpy.Merge_management((finpk, inpro), "finpkpro")

# indikator penambahan field dan perhitungan field
inTable = "finpkpro"
fieldName = "kondisi"
expression = "calc(!kondisi!)"
codeblock = """
def calc(a):
    a="Sudah PL"
    return a
"""

# penambahan field
arcpy.AddField_management(inTable, fieldName, 'TEXT', '','',255,'kondisi','NULLABLE','')

# perhitungan field
arcpy.CalculateField_management(inTable, fieldName, expression, "PYTHON3", codeblock)

#Dissolve HPL
alokasi = arcpy.Dissolve_management(finpkpro,"alokasi", ["kondisi"], "", "MULTI_PART","")

aprx = arcpy.mp.ArcGISProject("CURRENT")
m = aprx.listMaps()[0]
gabung = arcpy.MakeFeatureLayer_management(alokasi, "Alokasi")
gabungalokasi = gabung.getOutput(0)
m.addLayer(gabungalokasi)
