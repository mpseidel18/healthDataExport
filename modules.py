from datetime import date, time
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
pd.options.mode.chained_assignment = None  # default='warn'
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
        jsonName = os.path.splitext(os.path.basename(jsonfile))[0]
        print(jsonfile)
        Path("DatabaseExports/"+ 'fromCsv/'+ jsonName + "/").mkdir(parents=True, exist_ok=True)
        df_json = pd.read_json(jsonfile, orient='index')
        df_json.transpose()
        df_json.to_excel("DatabaseExports/" + 'fromCsv/'+ jsonName + "/" + str(jsonName) +'.xlsx')

def convertCsv2Xlsx(fname):
    print("Fetching Files...")
    for csvfile in getFilesRecursive(fname, "csv"):
        csvName = os.path.splitext(os.path.basename(csvfile))[0]
        Path("DatabaseExports/"+ 'fromCsv/'+ csvName + "/").mkdir(parents=True, exist_ok=True)
        workbook = Workbook("DatabaseExports/" + 'fromCsv/'+ csvName + "/" + str(csvName) +'.xlsx')
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
        workbook.close()
#ToDO: Alle Sitzungen neu Formatieren
def getTCXDataToCSV(fname):
    print("Fetching Files...")
    for tcxfile in getFilesRecursive(fname, "tcx"):
        tcxName = os.path.splitext(os.path.basename(tcxfile))[0]
        print(tcxName)
        Path("DatabaseExports/"+ 'fromTcx/'+ tcxName + "/").mkdir(parents=True, exist_ok=True)
        laps_df, points_df = get_dataframes(tcxfile)
        points_df.to_csv("DatabaseExports/" + 'fromTcx/'+ tcxName + "/" + str(tcxName) +'.csv')
        laps_df.to_csv("DatabaseExports/" + 'fromTcx/'+ tcxName + "/" + str(tcxName) +'.csv')
    print("Done. Your files are in the folder you've set as args")


def getTCXDataToCSVGFit(fname):
    print("Fetching Files...")
    for tcxfile in getFilesRecursive(fname, "tcx"):
        tcxName = os.path.splitext(os.path.basename(tcxfile))[0]
        print(tcxName)
        Path("DatabaseExports/"+ 'fromTcx/'+ tcxName + "/points/").mkdir(parents=True, exist_ok=True)
        Path("DatabaseExports/"+ 'fromTcx/'+ tcxName + "/laps/").mkdir(parents=True, exist_ok=True)
        laps_df, points_df = get_dataframes(tcxfile)
        points_df.to_csv("DatabaseExports/" + 'fromTcx/'+ tcxName + "/points/" + str(tcxName) +'.csv')
        laps_df.to_csv("DatabaseExports/" + 'fromTcx/'+ tcxName + "/laps/" + str(tcxName) +'.csv')
    print("Done. Your files are in the folder you've set as args")

#TO-DO:EXPORT
def getLatLongInCsv(fname):
    print("Fetching Files...")
    print("Creating .csv file from the files in selected folder. \nImport these files to Google MyMaps to get an overview of the locations")
    for tcxfile in getFilesRecursive(fname, "tcx"):
        tcxName = os.path.splitext(os.path.basename(fname))[0]
        print(tcxName)
        Path("DatabaseExports/"+ 'fromTcx/' + tcxName + "/").mkdir(parents=True, exist_ok=True)
        laps_df, points_df = get_dataframes(tcxfile)
        df_no_indicies = points_df[['time','latitude','longitude','elevation']].to_csv("DatabaseExports/" + 'fromTcx/'+ tcxName + "/" + str(tcxName) +'.csv',index=False,header=True)
        print(df_no_indicies)

def exportGoogleTakout(PATH):
#Alle Daten\GoogleFit\Takeout
    getTCXDataToCSVGFit(PATH + "\Google Fit\Aktivitäten")#\Google Fit\Aktivitäten
    exportJsonToXlsxGFit(PATH + "\Google Fit\Alle Daten")
    convertJson2xlsx(PATH + "\Google Fit\Alle Sitzungen")
    convertCsv2Xlsx(PATH + "\Google Fit\Tägliche Aktivitätswerte")

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
        jsonName = os.path.splitext(os.path.basename(jsonfile))[0]
        Path("DatabaseExports/"+ jsonName + "/").mkdir(parents=True, exist_ok=True)
        print(jsonName)
        df_json = pd.read_json(jsonfile, orient='index')
        df_json.to_csv(("DatabaseExports/" + 'fromSql/'+ jsonName + "/" + str(jsonName) +'.csv'), index=False)

def getTimestamps(PATH_TO_JSON):
    with open (PATH_TO_JSON) as json_file:
        data = json.load(json_file)
        time_df_normalized = pd.json_normalize(data["Data Points"])
        df_dates = time_df_normalized[["endTimeNanos","startTimeNanos"]]
        df_dates["endTimeNanos"] = pd.to_datetime(df_dates["endTimeNanos"],format="%Y-%m-%d %H:%M:%S")
        df_dates["startTimeNanos"] = pd.to_datetime(df_dates["startTimeNanos"],format="%Y-%m-%d %H:%M:%S")
        df_dates.rename(columns={"endTimeNanos":"Date and endtime", "starTimeNanos":"Date and startime"}, inplace=True)
        return df_dates
        # time_df_normalized["endTimeNanos","startTimeNanos"].to_excel("myexcel.xlsx")
    

def exportJsonToXlsxGFit(PATH_TO_JSON):
    for jsonfile in getFilesRecursive(PATH_TO_JSON, "json"):
        with open (jsonfile) as json_file:
            data = json.load(json_file)
        if data["Data Points"] == []:
            print(jsonfile + " has no Data.")
        else:
            jsonName = os.path.splitext(os.path.basename(jsonfile))[0]
            print(jsonName)
            df_time = getTimestamps(jsonfile)
            df_normalized = pd.json_normalize(data["Data Points"])
            index = len(data["Data Points"])
            # print("Rows: " + str(index))
            # print(len(df_normalized))
            columns = len(df_normalized["fitValue"][0])
            # print("Colummns: " + str(columns))
            df_fitVal = pd.DataFrame(index=range(0, index), columns=range(0, columns))
            Path("DatabaseExports/"+ 'fromJson/'+ jsonName + "/").mkdir(parents=True, exist_ok=True)
            for x in range(0,index):
                values_df = df_normalized["fitValue"][x]
                tmp = []
                for i in values_df:
                    newdf = pd.DataFrame(i)
                    tmp.append(newdf["value"][0])
                df_fitVal.loc[x]=tmp
            df_final = pd.concat([df_fitVal, df_time], axis=1, join="inner")
            # print(df_final)
            df_final.to_excel("DatabaseExports/" + 'fromJson/'+ jsonName + "/" + str(jsonName) +'.xlsx' )
    return "Finished"



#exportJsonToXlsxGFit(r"Alle Daten\GoogleFit\Takeout\Google Fit\Alle Daten")
# convertJson2Csv(r"Alle Daten\GoogleFit\Takeout\Google Fit\Alle Daten")
# exportGoogleTakout("Alle Daten\GoogleFit\Takeout")
# getTCXDataToCSVGFit(r"Alle Daten\GoogleFit\Takeout\Google Fit\Aktivitäten")
# exportJsonToXlsxGFit(r"Alle Daten\GoogleFit\Takeout\Google Fit\Alle Daten")