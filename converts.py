import os
import pandas as pd
from pandas.io import json

def getPathofTargetDir(path):
    d = path
    arr = []
    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        if os.path.isfile(full_path):
            arr.append(full_path)
    return arr

def convertJson2xlsx():
    array = getPathofTargetDir("Google_Fit\Alle Sitzungen")
    df_json = pd.read_json('Google_Fit\Alle Sitzungen\\2021-06-09T13_36_25+02_00_WALKING.json')
    print(df_json)
    df_json.to_excel('Exports/data2.xlsx')

def convertCsv2Xlsx():
    read_file = pd.read_csv (r'Google_Fit\Tägliche Aktivitätswerte\\2021-06-10.csv')
    read_file.to_excel (r'Exports/newCSV2.xlsx', index = None, header=True)

convertCsv2Xlsx()
