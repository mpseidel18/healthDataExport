# HealthDataInterpret

This tool is use to analyze and export data from various health-data vendors. This tool is only tested with the Google Takeout export.

Usage:
```bash
 analyseTakeout.py [-h] [-xt | -cl | -cx | -jx | -a | -db] pathToDir
 
```

This tool offers various commands to chose from:

```bash
optional arguments:
  -h, --help         show this help message and exit
  -xt, --c2txt       Exports your .tcx Data in a .txt File.
  -cl, --csvgpslist  Exports the Lat/Long Data in from your .tcx File into a .csv File.
  -cx, --convertc2x  Converts .csv to .xlsx files.
  -jx, --convertj2x  Converts .json to .xlsx files.
  -a, --automatic    analyzes the full tree recursivly and trys to convert the data in readbale Data.
  -db, --database    Exports tables from a target Database. The Database must contain sqlite_schema. You need to specify the whole path to the databse!
```
Keep in Mind that this tool search for the given Directory **recursively !**. 

>In the case of Google Takeout, this tool, searches from the `Takeout` folder recursively to the end of the folders.
Feel free to try the converts on other vendors or formats!

## Examples
Lets say. you want to export some data from your `tcx` file:
```
>> PS C:\Users\[YOUR_USER]\> dir C:\Users\[YOUR_USER]\GoogleFit\Takeout\Google Fit\Aktivitäten

Verzeichnis: C:\Users\[YOUR_USER]\GoogleFit\Takeout\Google Fit\Aktivitäten


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        09.06.2021     05:19          21995 2021-06-09T13_36_25+02_00_PT37M54.546S_Gehen.tcx
-a----        09.06.2021     05:56           4622 2021-06-09T14_44_55+02_00_PT11M27.125S_Gehen.tcx                                                                     orm.db"
-a----        10.06.2021     00:45         411231 2021-06-10T09_23_50+02_00_PT14M30.303S_Gehen.tcx

>> PS C:\Users\[YOUR_USER]\> python exportHealth.py -xt C:\Users\[YOUR_USER]\GoogleFit\Takeout\Google Fit\Aktivitäten

>> PS C:\Users\[YOUR_USER]\>> dir C:\Users\[YOUR_USER]\GoogleFit\Takeout\Google Fit\Aktivitäten

Verzeichnis: C:\Users\[YOUR_USER]\GoogleFit\Takeout\Google Fit\Aktivitäten


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        09.06.2021     05:19          21995 2021-06-09T13_36_25+02_00_PT37M54.546S_Gehen.tcx
-a----        20.06.2021     12:34           1784 2021-06-09T13_36_25+02_00_PT37M54.546S_Gehen.tcx.txt
-a----        09.06.2021     05:56           4622 2021-06-09T14_44_55+02_00_PT11M27.125S_Gehen.tcx
-a----        20.06.2021     12:34            435 2021-06-09T14_44_55+02_00_PT11M27.125S_Gehen.tcx.txt
-a----        10.06.2021     00:45         411231 2021-06-10T09_23_50+02_00_PT14M30.303S_Gehen.tcx
-a----        20.06.2021     12:34          48727 2021-06-10T09_23_50+02_00_PT14M30.303S_Gehen.tcx.txt






```
## Known Bugs
- I tried this tool on various other exported vendors, but most of the time the `json`to `xlsx` convert does not work well. It works best on   the `json` Google Takout produces.
- Sometimes the path which is given doesn't get inserted in the functions quite well.

Big thanks to https://github.com/bunburya/fitness_tracker_data_parsing for the tcx parser!
