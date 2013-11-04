import arcpy as ARCPY
import os as OS
import DBFUtitlities as DBF

def createPolyNeiTable(inputFC, outputTable, field):
    ARCPY.env.overwriteOutput = True
    ARCPY.PolygonNeighbors_analysis(inputFC, outputTable, field)

def reformatPolyNei(outputTable):
    refTable = open(outputTable, 'rb')
    db = list(DBF.dbfreader(refTable))
    refTable.close()
    fieldNames, fieldSpecs, records = db[0], db[1], db[2:]

    del fieldNames[2:4]
    del fieldSpecs[2:4]
    records = [rec[0:2] for rec in records]

    fieldNames[0] = 'FID'
    fieldNames[1] = 'NID'

    newTable = open(outputTable, 'w')
    DBF.dbfwriter(newTable, fieldNames, fieldSpecs, records)
    newTable.close()

def reformatWeight(outputSWM):
    refTable = open(outputSWM, 'rb')
    db = list(DBF.dbfreader(refTable))
    refTable.close()
    fieldNames, fieldSpecs, records = db[0], db[1], db[2:]

    del fieldNames[0]
    del fieldNames[2]
    del fieldSpecs[0]
    del fieldSpecs[2]
    records = [rec[1:3] for rec in records]

    fieldNames[0] = 'FID'
    fieldNames[1] = 'NID'

    newTable = open(outputSWM, 'w')
    DBF.dbfwriter(newTable, fieldNames, fieldSpecs, records)
    newTable.close()

if __name__ == '__main__':
    inputPath = "C:/Data/SWM/data/"
    outputPath = "C:/Data/SWM/result/"

    fileList = ['polygon','tracts','UScounties']
    fieldList = ['FIPS', 'geocompID', 'OBJECTID']

    for i in xrange(3):
        inputFC = inputPath + fileList[i] + ".shp"
        outputTable = outputPath + "PolyNei" + str(i+1) + ".dbf"
        field = fieldList[i]

        createPolyNeiTable(inputFC, outputTable, field)
        reformatPolyNei(outputTable)

        outputSWM = outputPath + "swm" + str(i+1) + ".dbf"
        reformatWeight(outputSWM)

    print "Done"











