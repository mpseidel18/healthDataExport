import os
import pandas as pd
from pandas.io import json
from tcxAnalyse import *
from glob import glob
import csv
from xlsxwriter.workbook import Workbook #Mehrere Imports
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
        df_json.to_excel (str(jsonfile) +'.xlsx' )


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
def getTCXDataToTxt(fname):
    print("Fetching Files...")
    for tcxfile in getFilesRecursive(fname, "tcx"):
        output = printData(tcxfile)
        f = open(str(tcxfile) +'.txt' , "a")
        f.write(output)
        f.close
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
            getTCXDataToTxt(PATH)
        if extension == 'json':
            convertJson2xlsx(PATH)
        if extension == 'csv':
            convertCsv2Xlsx(PATH)

        # points_df = get_dataframes(tcxfile)
        # points_df[['time','latitude','longitude','elevation']].to_csv(str(tcxfile) +'.csv',index=False,header=True)