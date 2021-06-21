from datetime import date
import os
from sqlite3.dbapi2 import paramstyle
from numpy.lib import index_exp
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.io import json
from tcxAnalyse import *
from glob import glob
import csv
from xlsxwriter.workbook import Workbook
import sqlite3 #Mehrere Imports
import numpy as np
from pathlib import Path
from pandas.io.excel import ExcelWriter
import json
FILETYPES = ['tcx', 'json', 'xlsx','csv']

def printData(fname):
    laps_df, points_df = get_dataframes(fname)
    return "LAPS:" + "\n" + str(laps_df) + "\n" + "POINTS:" + "\n" + str(points_df) +"\n"
def getLatLong(fname):
    laps_df, points_df = get_dataframes(fname)
    df_no_indicies = points_df[['latitude','longitude']].to_string(index=False).replace('   ',',')
    return(df_no_indicies)
def getFilesRecursive(fname, filetype):
    return [y for x in os.walk(fname) for y in glob(os.path.join(x[0], '*.' + str(filetype) ))]

def convertJson2xlsx(fname):
    print("Fetching Files...")
    for jsonfile in getFilesRecursive(fname, "json"):
        print(jsonfile)
        df_json = pd.read_json(jsonfile, orient='index')
        df_json.transpose()
        df_json.to_excel(str(jsonfile) +'.xlsx' )


def convertCsv2Xlsx(fname):
    print("Fetching Files...")
    for csvfile in getFilesRecursive(fname, "csv"):
        print(csvfile)
        workbook = Workbook(csvfile[:-4] + '.xlsx')
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
        workbook.close()
def getTCXDataToCSV(fname):
    print("Fetching Files...")
    for tcxfile in getFilesRecursive(fname, "tcx"):
        laps_df, points_df = get_dataframes(tcxfile)
        points_df.to_csv(str(tcxfile) + 'points' + '.csv')
        laps_df.to_csv(str(tcxfile) + 'laps' + '.csv')
    print("Done. Your files are in the folder you've set as args")


def getTCXDataToCSVGFit(fname):
    print("Fetching Files...")
    for tcxfile in getFilesRecursive(fname, "tcx"):
        laps_df, points_df = get_dataframes(tcxfile)
        points_df.to_csv(str(tcxfile) + 'points' + '.csv')
        laps_df.to_csv(str(tcxfile) + 'laps' + '.csv')
    print("Done. Your files are in the folder you've set as args")

def getLatLongInCsv(fname):
    print("Fetching Files...")
    print("Creating .csv file from the files in selected folder. \nImport these files to Google MyMaps to get an overview of the locations")
    for tcxfile in getFilesRecursive(fname, "tcx"):
        print(tcxfile)
        laps_df, points_df = get_dataframes(tcxfile)
        df_no_indicies = points_df[['time','latitude','longitude','elevation']].to_csv(str(tcxfile) +'.csv',index=False,header=True)
        print(df_no_indicies)

def analyzeHealthData(PATH):
    for extension in FILETYPES:
        if extension == 'tcx':
            getTCXDataToCSV(PATH)
        if extension == 'json':
            convertJson2xlsx(PATH)
        if extension == 'csv':
            convertCsv2Xlsx(PATH)

def exportSqlite(PATH):
    database = sqlite3.connect(PATH)
    df = pd.read_sql_query("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;", database)
    nparray= df["name"].to_numpy()
    convertDatabase = sqlite3.connect(PATH)
    dbname = os.path.splitext(os.path.basename(PATH))[0]
    print(dbname)
    Path("DatabaseExports/"+ dbname + "/").mkdir(parents=True, exist_ok=True)
    for x in nparray:
        exportedTable = pd.read_sql_query("SELECT * from " + x + ";", convertDatabase)
        exportedTable.to_excel ("DatabaseExports/" + dbname + "/" + str(x) +'.xlsx' )

def convertJson2Csv(PATH):
    for jsonfile in getFilesRecursive(PATH, "json"):
        print(jsonfile)
        df_json = pd.read_json(jsonfile, orient='index')
        df_json.to_csv((str(jsonfile) +'.csv'), index=False)

def exportJsonToXlsxGFit():
    with open (r"Alle Daten\GoogleFit\Takeout\Google Fit\Alle Daten\derived_com.google.location.sample_com.google.(2).json") as json_file:
        data = json.load(json_file)
    df = pd.json_normalize(data["Data Points"])
    index = len(data["Data Points"])
    # print(index)
    print(df)
    df = df["fitValue"][0]
    columns = len(df)
    # print(columns)
    df_final = pd.DataFrame(index=range(0, index), columns=range(0,columns))
    ################################
    tmp = []
    for i in df:
        newdf = pd.DataFrame(i)
        tmp.append(newdf["value"][0])
    df_final.loc[0]=tmp
    print(df_final)
        # newdf = pd.DataFrame(df)
        # newdf = newdf["value"][0]
        # df_final.loc[2,1] = newdf
        # print(df_final)
    
    # for i in dataPoints:
    #     if isinstance(i, dict):
    #         pairs = i.items()
    #         for key, value in pairs:
    #             if isinstance(value, list):
    #                 for i in value:
    #                     if isinstance(i, dict):
    #                         print(i.values())
    # values = []
    # for result in data["Data Points"]:
    #     values.append(result[u"fitValue"][0])
    # print(values)
    # df = pd.json_normalize(data["Data Points"])
    # newJson=json.dumps(data["Data Points"])
    # df = pd.DataFrame(data["Data Points"])
    # df.to_excel("newDF.xlsx", index = False)
    # return newJson
    # print(df)
exportJsonToXlsxGFit()