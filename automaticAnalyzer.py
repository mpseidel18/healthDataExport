from modules import *
from pandas.io import json
from tcxAnalyse import *
import csv
from xlsxwriter.workbook import Workbook
import os
from glob import glob
FILETYPES = ['tcx', 'json', 'xlsx','csv']

def analyzeHealthData(PATH):
    for extension in FILETYPES:
        if extension == 'tcx':
            getTCXDataToTxt(PATH, extension)
        if extension == 'json':
            convertJson2xlsx(PATH, extension)
        if extension == 'csv':
            convertCsv2Xlsx(PATH, extension)