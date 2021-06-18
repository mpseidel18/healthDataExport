from modules import *
import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-xt", "--c2txt", help="Exports your .tcx Data in a .txt File.", action="store_true")
group.add_argument("-cl", "--csvgpslist", help="Exports the Lat/Long Data in from your .tcx File into a .csv File.", action="store_true")
group.add_argument("-cx", "--convertc2x", help="Converts .csv to .xlsx files", action="store_true")
group.add_argument("-jx", "--convertj2x", help="Converts .json to .xlsx files", action="store_true")


parser.add_argument("pathToDir", type=str, help="Path to the target directory. The tool always tries to fetch all files of given type.")
args = parser.parse_args()
# answer = args.x**args.y

# if args.quiet:
#     print(answer)
# elif args.verbose:
#     print("{} to the power {} equals {}".format(args.x, args.y, answer))
# else:
#     print("{}^{} == {}".format(args.x, args.y, answer))
if args.csvgpslist:
    getLatLongInCsv(args.pathToDir)
elif args.c2txt:
    getTCXDataToTxt(args.pathToDir)
elif args.convertc2x:
    convertCsv2Xlsx(args.pathToDir)
elif args.convertj2x:
    convertJson2xlsx(args.pathToDir)