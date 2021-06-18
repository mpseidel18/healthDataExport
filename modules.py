import os
import pandas as pd
from pandas.io import json
from tcxAnalyse import *
import glob
import csv
from xlsxwriter.workbook import Workbook

#MISC
def printData(fname):
    laps_df, points_df = get_dataframes(fname)
    return "LAPS:" + "\n" + str(laps_df) + "\n" + "POINTS:" + "\n" + str(points_df) +"\n"
def getLatLong(fname):
    laps_df, points_df = get_dataframes(fname)
    df_no_indicies = points_df[['latitude','longitude']].to_string(index=False).replace('   ',',')
    return(df_no_indicies)

#JSON
def convertJson2xlsx(fname):
    for jsonfile in glob.glob(os.path.join(fname, '*.json')):
        df_json = pd.read_json(jsonfile, orient='index')
        df_json.transpose()
        df_json.to_excel (str(jsonfile) +'.xlsx' )

# CSV
def convertCsv2Xlsx(fname):
    for csvfile in glob.glob(os.path.join(fname, '*.csv')):
        print(csv)
        workbook = Workbook(csvfile[:-4] + '.xlsx')
        worksheet = workbook.add_worksheet()
        with open(csvfile, 'rt', encoding='utf8') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    worksheet.write(r, c, col)
        workbook.close()
#TCX
#analyszeTakout --tcx --txtdata [path_to_dir] 
def getTCXDataToTxt(fname):
    print("Starting to read the Path...")
    for tcxfile in glob.glob(os.path.join(fname, '*.tcx')):
        output = printData(tcxfile)
        f = open(str(tcxfile) +'.txt' , "a")
        f.write(output)
        f.close
    print("Done. Your files are in the folder you've set as args")
# def getTcxGpsList(fname):
#     for tcxfile in glob.glob(os.path.join(fname, '*.tcx')):
#         output = getLatLong(tcxfile)
#         f = open(str(tcxfile) + '-gps-' + '.txt' , "a")
#         f.write(output)
#         f.close
#analyszeTakout --tcx --csvgpslist [path_to_dir] 
def getLatLongInCsv(fname):
    print("Creating .csv file from the files in selected folder. \nImport these files to Google MyMaps to get an overview of the locations")
    laps_df, points_df = get_dataframes(fname)
    df_no_indicies = points_df[['time','latitude','longitude','elevation']].to_csv(r'.\Exports\out.csv',index=False,header=True)
    print("Done.")
# getLatLongInCsv("Google_Fit/Aktivitäten/2021-06-10T09_23_50+02_00_PT14M30.303S_Gehen.tcx")

#TO-DO: TCX TO CSV
# convertJson2xlsx("Google_Fit/Alle Sitzungen/")
# convertJson2xlsx("Google_Fit/Alle Daten")
# convertCsv2Xlsx(r"Google_Fit\Tägliche Aktivitätswerte")
# getTCXDataToTxt("Google_Fit\Aktivitäten")
# getTcxGpsList("Google_Fit/Aktivitäten")
# getLatLongInCsv(r"Google_Fit\Aktivitäten\2021-06-10T09_23_50+02_00_PT14M30.303S_Gehen.tcx")