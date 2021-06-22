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
import sqlite3
import numpy as np
from pathlib import Path
from pandas.io.excel import ExcelWriter
import json
#Mehrere Imports

pd.options.mode.chained_assignment = None 
#Unterdrückung eines Warnings von pandas
def getFilesRecursive(fname, filetype):
    return [y for x in os.walk(fname) for y in glob(os.path.join(x[0], '*.' + str(filetype) ))]
    #Gibt eine Liste mit allen vollständigen Dateipfaden für einen filetype zurück

def convertJson2xlsx(fname):
    print("Searching for Files...")
    for jsonfile in getFilesRecursive(fname, "json"):  
        #Für jede gefundene -json Datei:
        jsonName = os.path.splitext(os.path.basename(jsonfile))[0]
        #Sichern des Dateinamens
        Path("ExportedData/"+ 'fromCsv/'+ jsonName + "/").mkdir(parents=True, exist_ok=True)
        #Erstellen des Pfades, falls er nicht existiert
        df_json = pd.read_json(jsonfile, orient='index')   
        #Laden des .json Files in einen Dataframe, orientierung für json Dateien angepasst
        df_json.transpose()
        #Dataframe wird "umgedreht"
        df_json.to_excel("ExportedData/" + 'fromCsv/'+ jsonName + "/" + str(jsonName) +'.xlsx')
        #Json Datei wird als .xlsx Datei exportiert.
    print("Export finished! The files can be found under ./ExportedData.")

def convertCsv2Xlsx(fname):
    print("Searching for Files...")
    for csvfile in getFilesRecursive(fname, "csv"):
        csvName = os.path.splitext(os.path.basename(csvfile))[0]
        Path("ExportedData/"+ 'fromCsv/'+ csvName + "/").mkdir(parents=True, exist_ok=True)
        workbook = Workbook("ExportedData/" + 'fromCsv/'+ csvName + "/" + str(csvName) +'.xlsx')
        #Neues Workbook
        worksheet = workbook.add_worksheet()   
        #Neues sheet
        with open(csvfile, 'rt', encoding='utf8') as f:
            #.csv File wird geöffnet
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
                    #Daten werden auf das Sheet gesichert
        workbook.close()
        #Schließen des Workbooks
    print("Export finished! The files can be found under ./ExportedData.")

def getTCXDataToCSVGFit(fname):
    #Erneut wird der Pfad erstellt und die Name gesucht und gesichert
    print("Searching for Files...")
    for tcxfile in getFilesRecursive(fname, "tcx"):
        tcxName = os.path.splitext(os.path.basename(tcxfile))[0]

        Path("ExportedData/"+ 'fromTcx/'+ tcxName + "/points/").mkdir(parents=True, exist_ok=True)
        Path("ExportedData/"+ 'fromTcx/'+ tcxName + "/laps/").mkdir(parents=True, exist_ok=True)
        laps_df, points_df = get_dataframes(tcxfile)
        points_df.to_csv("ExportedData/" + 'fromTcx/'+ tcxName + "/points/" + str(tcxName) +'.csv')
        #Konvertierung der gesicherten Dataframes zu .csv Dateien
        laps_df.to_csv("ExportedData/" + 'fromTcx/'+ tcxName + "/laps/" + str(tcxName) +'.csv')
        #Konvertierung der gesicherten Dataframes zu .csv Dateien
    print("Export finished! The files can be found under ./ExportedData.")

def exportWorkoutSessions(PATH):
    #Die Besonderheit hier ist die verschachtelung der Daten. Zunächst werden die Daten aus dem Tree gesucht und in Frames exportiert,
    #Um danach mit den Metadaten zusammengesetzt zu werden
    print("Searching for Files...")
    for jsonfile in getFilesRecursive(PATH, "json"):
        with open(jsonfile) as json_file:
            data = json.load(json_file)
        jsonName = os.path.splitext(os.path.basename(jsonfile))[0]
        Path("ExportedData/"+ 'fromJson/'+ jsonName + "/").mkdir(parents=True, exist_ok=True)
        df_norm = pd.json_normalize(data)
        #Normalisierung der Daten in eine Tabelle
        df_aggregate = pd.DataFrame(df_norm["aggregate"][0])
        #Unter aggregate sind die Json Einträge mit den wichtigen Informationen, somit wird ein neuer Frame aus diesem herausgezogen
        df_meta = df_norm[["fitnessActivity","startTime","endTime","duration"]]
        #Sicherung der Metadaten
        df_final = pd.concat([df_aggregate, df_meta]).to_excel("ExportedData/" + 'fromJson/'+ jsonName + "/" + str(jsonName) +'.xlsx' )
        #Zusammensetzung der beiden Dataframes. Danach wird der finale Frame in eine xlsx Datei Exportiert.
                                             
    print("Export finished! The files can be found under ./ExportedData.")

def getLatLongInCsv(fname):
    #Das gleiche Format wie die anderen Funktionen, hier werden jedoch nur 'time','latitude','longitude','elevation'
    #Aus der TCX Datei gesammelt
    print("Searching for Files...")
    for tcxfile in getFilesRecursive(fname, "tcx"):
        tcxName = os.path.splitext(os.path.basename(fname))[0]
        Path("ExportedData/"+ 'fromTcx/' + tcxName + "/").mkdir(parents=True, exist_ok=True)
        laps_df, points_df = get_dataframes(tcxfile)
        df_no_indicies = points_df[['time','latitude','longitude','elevation']].to_csv("ExportedData/" + 'fromTcx/'+ tcxName + "/" + str(tcxName) +'.csv',index=False,header=True)
    print("Export finished! The files can be found under ./ExportedData.")

def exportSqlite(PATH):
    #Exportieren der Tabellen einer Datenbank in mehrere xlsx Dateien
    print("Searching for Files...")
    database = sqlite3.connect(PATH)
    #Verbinden mit der ausgewählten Datenbank
    df = pd.read_sql_query("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;", database)
    #Die namen der Tabellen werden aus sqlite_schema
    nparray= df["name"].to_numpy()
    #Aus den Namen wir ein numpy Attay erstellt
    dbname = os.path.splitext(os.path.basename(PATH))[0]
    Path("ExportedData/"+ 'fromSql/'+ dbname + "/").mkdir(parents=True, exist_ok=True)
    for x in nparray:
        exportedTable = pd.read_sql_query("SELECT * from " + x + ";", database)
        #Zunächst die Tabelle auswählen
        exportedTable.to_excel ("ExportedData/" + 'fromSql/'+ dbname + "/" + str(x) +'.xlsx' )
        #Und danach exportieren
    print("Export finished! The files can be found under ./ExportedData.")

def convertJson2Csv(PATH):
    #Das Schema in dieser Funktion ist das gleiche wie das in den voherigen:
    #Dataframe erstellen und diesen exportieren
    print("Searching for Files...")
    for jsonfile in getFilesRecursive(PATH, "json"):
        jsonName = os.path.splitext(os.path.basename(jsonfile))[0]
        Path("ExportedData/"+ jsonName + "/").mkdir(parents=True, exist_ok=True)
        df_json = pd.read_json(jsonfile, orient='index')
        df_json.to_csv(("ExportedData/" + 'fromSql/'+ jsonName + "/" + str(jsonName) +'.csv'), index=False)
    print("Export finished! The files can be found under ./ExportedData.")

def getTimestamps(PATH_TO_JSON):
    #Diese holt sich aus den json Files unter Takeout\Google Fit\Alle Daten die Zeitstempel heraus
    #Diese weren in einen Dataframe geladen und anschließend wird dieser zurückgegeben
    with open (PATH_TO_JSON) as json_file:
        data = json.load(json_file)
        time_df_normalized = pd.json_normalize(data["Data Points"]) 
        df_dates = time_df_normalized[["endTimeNanos","startTimeNanos"]]
        #Aus dem json Dataframe werden die Zeitstempel herausgelesen und in einen neuen gesichert
        df_dates["endTimeNanos"] = pd.to_datetime(df_dates["endTimeNanos"],format="%Y-%m-%d %H:%M:%S")
        #Die Daten werden in lesbare Form gebracht. Altes Format: Linux Epoch
        df_dates["startTimeNanos"] = pd.to_datetime(df_dates["startTimeNanos"],format="%Y-%m-%d %H:%M:%S")
        df_dates.rename(columns={"endTimeNanos":"Date and endtime", "starTimeNanos":"Date and startime"}, inplace=True)
        #Die Spalten werden nun umbenant
        return df_dates

def exportJsonToXlsxGFit(PATH_TO_JSON):
    #Diese Funktion versucht "fitValue" aus verschachtelten .json Dateien aus Takeout\Google Fit\Alle Daten zu holen
    print("Searching for Files...")
    for jsonfile in getFilesRecursive(PATH_TO_JSON, "json"):
        with open (jsonfile) as json_file:
            data = json.load(json_file)
        #Laden der .json Datei
        if data["Data Points"] == []:
            print("Info: " + jsonfile + " has no Data.")
        #Überspringen, falls json keine Daten beinhaltet
        else:
            jsonName = os.path.splitext(os.path.basename(jsonfile))[0]
            df_time = getTimestamps(jsonfile)
            df_normalized = pd.json_normalize(data["Data Points"])
            #Unter Data Points befindet sich eine Liste von .json Dateien
            #Diese wird versucht zu verarbeiten
            index = len(data["Data Points"])
            #Setzen der Indexgröße für den neuen Dataframe
            #Die Indexgröße ist die Anzahl der vorhandenen Daten unter Data Points
            columns = len(df_normalized["fitValue"][0])
            #Setzen Spaltenanzahl. Diest ist die Anzahl der verschiedenen fitVal Einträge
            df_fitVal = pd.DataFrame(index=range(0, index), columns=range(0, columns))
            #Dataframe wird erstellt
            Path("ExportedData/"+ 'fromJson/'+ jsonName + "/").mkdir(parents=True, exist_ok=True)
            for x in range(0,index):
                values_df = df_normalized["fitValue"][x]
                #Neues Dataframe aus dem Dictionary unter fitVal
                tmp = []
                for i in values_df:
                    newdf = pd.DataFrame(i)
                    #Erzeugen eines neuen Dataframes aus voherigem Dict
                    tmp.append(newdf["value"][0])
                    #Anhängen des Values des Dict an eine Liste
                df_fitVal.loc[x]=tmp
                #Schreiben der Liste in den leeren Dataframe
            df_final = pd.concat([df_fitVal, df_time], axis=1, join="inner")
            #Zeit- und Datendataframe werden zusammengeführt
            df_final.to_excel("ExportedData/" + 'fromJson/'+ jsonName + "/" + str(jsonName) +'.xlsx' )
            #Exportierung in xlsx Format
    print("Export finished! The files can be found under ./ExportedData.")
    return "Finished"

def exportGoogleTakout(PATH):
    #Ausführung des verschiedenen zugeschnittenen Exports auf die
    #verschiedenen Takeout Ordner
    getTCXDataToCSVGFit(PATH + "\Google Fit\Aktivitäten")
    exportJsonToXlsxGFit(PATH + "\Google Fit\Alle Daten")
    exportWorkoutSessions(PATH + "\Google Fit\Alle Sitzungen")
    convertCsv2Xlsx(PATH + "\Google Fit\Tägliche Aktivitätswerte")
    print("Google Takout Export finished.")
