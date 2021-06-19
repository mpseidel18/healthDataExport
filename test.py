import os
from glob import glob
from tcxAnalyse import *
FILETYPES = ['.tcx', '.json', '.xlsx','.csv', '.lol']
PATH = "./Google_Fit"
def analyzeHealthData(PATH):
    for extension in FILETYPES:
        result = [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*' + extension ))]
        print(result)
        if not result:
            print("No files match " + extension)
        if extension == '.tcx':
            print("Fetching Files...")
            for tcxfile in result:
                print(type(tcxfile))
                output = printData(tcxfile)
                f = open(str(tcxfile) +'.txt' , "a")
                f.write(output)
                f.close