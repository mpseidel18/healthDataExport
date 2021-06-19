from modules import *
import argparse
from automaticAnalyzer import analyzeHealthData

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-xt", "--c2txt", help="Exports your .tcx Data in a .txt File.", action="store_true")
group.add_argument("-cl", "--csvgpslist", help="Exports the Lat/Long Data in from your .tcx File into a .csv File.", action="store_true")
group.add_argument("-cx", "--convertc2x", help="Converts .csv to .xlsx files.", action="store_true")
group.add_argument("-jx", "--convertj2x", help="Converts .json to .xlsx files.", action="store_true")
group.add_argument("-a", "--automatic", help="analyzes the full tree recursivly and trys to convert the data in readbale Data.", action="store_true")

parser.add_argument("pathToDir", type=str, help="Path to the target directory.")
args = parser.parse_args()

if args.csvgpslist:
    getLatLongInCsv(args.pathToDir)
elif args.c2txt:
    getTCXDataToTxt(args.pathToDir)
elif args.convertc2x:
    convertCsv2Xlsx(args.pathToDir)
elif args.convertj2x:
    convertJson2xlsx(args.pathToDir)
elif args.automatic:
    analyzeHealthData(args.pathToDir)