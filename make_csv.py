import subprocess
import os
import time
import csv
import pandas as pd
from datetime import datetime
import sys

parentdir = str(sys.argv[1])

def getFileList():
    os.chdir(parentdir)
    files = os.listdir()
    return files  

files = getFileList()

def getDurationData():
    data = {}
    for f in files:
        p1 = subprocess.run('ffmpeg -i "' + f + '" 2>&1| grep Duration',capture_output=True,shell=True)
        out = p1.stdout.decode("utf-8")[12:20]
        if out != '':
            data[f] = out
    return data

data = getDurationData()

def createCsvFile():
    global data
    csvData = []
    csvColumnName = ['FileName','Start','End']
    for i in data:
        col = {}
        col['FileName'] = i
        col['Start'] = '00:00:00'
        col['End'] = data[i]
        csvData.append(col)
    with open('trimdata.csv','w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvColumnName)
        writer.writeheader()
        for data in csvData:
                writer.writerow(data)

createCsvFile()

