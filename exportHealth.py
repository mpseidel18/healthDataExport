from modules import *
import argparse #Importieren einiger Module und der Funktionen von modules.py.

parser = argparse.ArgumentParser() #Neuen Parser erstellen.
group = parser.add_mutually_exclusive_group() #Neue Gruppe für Befehle erstellen. Diese können nicht zusammen genutzt werden.
group.add_argument("-xc", "--c2csv", help="Exports your .tcx Data in a .csv File.", action="store_true") #Hinzufügen von den einzelnen Flags.
group.add_argument("-cl", "--csvgpslist", help="Exports the Lat/Long Data in from your .tcx File into a .csv File.", action="store_true")
group.add_argument("-cx", "--convertc2x", help="Converts .csv to .xlsx files.", action="store_true")
group.add_argument("-jx", "--convertj2x", help="Converts .json to .xlsx files.", action="store_true")
group.add_argument("-a", "--automatic", help="analyzes the full tree recursivly and trys to convert the data in readbale Data.", action="store_true")
group.add_argument("-db", "--database", help="Exports tables from a target Database. The Database must contain sqlite_schema. \n You need to specify the whole path to the databse!", action="store_true")
group.add_argument("-f", "--fitval", help="Gets the fitVal entries from a Google Takeout .json. \n You need to specify the whole path to the databse!", action="store_true")

parser.add_argument("pathToDir", type=str, help="Path to the target directory or a file.") #Argument "pathToDir" hinzufügen.
args = parser.parse_args() 

if args.csvgpslist: #Fallunterscheidungen für die einzelnen Inputs. Falls -cl ausgewählt wird, wird getLatLongInCsv ausgeführt.
    getLatLongInCsv(args.pathToDir)
elif args.c2csv:
    getTCXDataToCSV(args.pathToDir)
elif args.convertc2x:
    convertCsv2Xlsx(args.pathToDir)
elif args.convertj2x:
    convertJson2xlsx(args.pathToDir)
elif args.automatic:
    analyzeHealthData(args.pathToDir)
elif args.database:
    exportSqlite(args.pathToDir)
elif args.fitval:
    exportJsonToXlsxGFit(args.pathToDir)