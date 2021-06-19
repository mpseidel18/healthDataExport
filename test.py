from tcxAnalyse import *
import os
from glob import glob
FILETYPES = ['.tcx', '.json', '.xlsx','.csv', '.lol']

def analyzeHealthData():
    for extension in FILETYPES:
        PATH = r"C:\Users\Marius\progammiern\healthdatatInterpret\Google_Fit"
        result = [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*' + extension ))]
        if not result:
            print("No files match " + extension)
        if extension == '.tcx':
            print("Fetching Files...")
            for tcxfile in result:
                output = printData(tcxfile)
                f = open(str(tcxfile) +'.txt' , "a")
                f.write(output)
                f.close
                points_df = get_dataframes(tcxfile)
                points_df[['time','latitude','longitude','elevation']].to_csv(r'.\Exports\out.csv',index=False,header=True)
            print("Done.")
        if extension == '.json':
            pass
        if extension == '.csv':
            pass