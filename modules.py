import os
import pandas as pd
from pandas.io import json
from tcxAnalyse import *

def getPathofTargetDir(path):
    d = path
    arr = []
    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        if os.path.isfile(full_path):
            arr.append(full_path)
    return arr

def convertJson2xlsx(importPath, exportPath):
    array = getPathofTargetDir("Google_Fit\Alle Sitzungen")
    df_json = pd.read_json('Google_Fit\Alle Sitzungen\\2021-06-09T13_36_25+02_00_WALKING.json')
    print(df_json)
    df_json.to_excel('Exports/data2.xlsx')

def convertCsv2Xlsx(importPath):
        count = 1
        array = getPathofTargetDir(importPath)
        print(array)
        if not os.path.exists('autoExport'):
            os.makedirs('autoExport')
        for i in array:
            read_file = pd.read_csv (i)
            read_file.to_excel ('.\\autoExport' + '\\1' + '.xlsx' )
            count += 1

def getTCXDataToTxt(path, pathToFile):
    array = getPathofTargetDir(path)
    for i in array:
        output = printData(i)
        f = open(pathToFile, "a")
        f.write(output)
        f.close
# getTCXDataToTxt("Google_Fit\Aktivitäten","tcxDaten.txt")
convertCsv2Xlsx("Google_Fit/Aktivitäten/")