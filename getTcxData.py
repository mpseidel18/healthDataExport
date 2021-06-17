from healthdataInterpret import printData
import sys
import os
d = str(sys.argv[1])
print(sys.argv[1])
for path in os.listdir(d):
    full_path = os.path.join(d, path)
    if os.path.isfile(full_path):
        printData(full_path)