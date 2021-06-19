# HealthDataInterpret

This tool is use to analyze and export data from various health-data vendors. This tool is only tested with the Google Takeout export.

Usage:
```bash
 analyseTakeout.py [-h] [-xt | -cl | -cx | -jx | -a] pathToDir
 
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
```
Keep in Mind that this tool search for the given Directory **recursively !**.
In the case of Google Takeout, this tool, searches from the `Takeout` folder recursively to the end of the folders.
Feel free to try the converts on other vendors or formats!
## Known Bugs
- I tried this tool on various other exported vendors, but most of the time the `json`to `xlsx` convert does not work well. It works best on   the `json` Google Takout produces.
- Sometimes the path which is given doesn't get inserted in the functions quite well.
