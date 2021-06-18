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

def convertJson2xlsx(importPath):
        count = 1
        array = getPathofTargetDir(importPath)
        print(len(array))
        # if not os.path.exists('autoExport'):
        #     os.makedirs('autoExport')
        for i in array:
            print("Nr. " + str(count) + ":" + "\n" + i)
            df_json = pd.read_json(i, orient='index')
            df_json.transpose()
            df_json.to_excel (str(i) +'.xlsx' )
            count += 1

def convertCsv2Xlsx(importPath):
        count = 1
        array = getPathofTargetDir(importPath)
        if not os.path.exists('autoExport'):
            os.makedirs('autoExport')
        for i in array:
            print("Nr. " + str(count) + ":" + "\n" + i)
            df_csv = pd.read_csv(i)
            df_csv.to_excel (str(i) +'.xlsx' )
            count += 1

def getTCXDataToTxt(path, pathToFile):
    array = getPathofTargetDir(path)
    for i in array:
        output = printData(i)
        f = open(pathToFile, "a")
        f.write(output)
        f.close
convertJson2xlsx("Google_Fit/Alle Sitzungen/")
convertJson2xlsx("Google_Fit/Alle Daten")
convertCsv2Xlsx("Google_Fit/Tägliche Aktivitätswerte")
getTCXDataToTxt("Google_Fit\Aktivitäten","Google_Fit/Aktivitäten/Data.txt")