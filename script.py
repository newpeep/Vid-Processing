# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import subprocess
import os
import time
import csv
import pandas as pd
from datetime import datetime


# %%
class preparedata:

    def __init__(self,pdir = os.getcwd()):
        self.parentdir = pdir
        self.nPac = 10
        self.files = self.getFileList()
        self.data = self.getDurationData()
        self.tsec = self.getTotalDuration()

    def setPackets(self,n):
        self.nPac = n

    def getFileList(self):
        os.chdir(self.parentdir)
        files = os.listdir()
        return files    

    def getDurationData(self):
        data = {}
        for f in self.files:
            p1 = subprocess.run('ffmpeg -i "' + f + '" 2>&1| grep Duration',capture_output=True,shell=True)
            out = p1.stdout.decode("utf-8")[12:20]
            if out != '':
                data[f] = out
        # print(data)
        return data

    def addTime(self,a,b):
        return time.struct_time((0,0,0,a.tm_hour+b.tm_hour,a.tm_min+b.tm_min,a.tm_sec+b.tm_sec,0,0,0))

    def getTotalDuration(self):
        res = time.struct_time((0,0,0,0,0,0,0,0,0))
        for i in self.data:
            res = self.addTime(res,time.strptime(self.data[i],'%H:%M:%S'))
        tsec = res.tm_sec + res.tm_min * 60 + res.tm_hour * 60 * 60
        return tsec

    def moveFiles(self):
        limit = (self.tsec)/(self.nPac)
        test = 0
        filePtr = 0
        fileL = len(self.files) 
        for i in range(1,self.nPac+1):
            ndir = "folder" + str(i)
            path = os.path.join(self.parentdir,ndir)
            os.mkdir(path)
            test = 0
            while test<limit and filePtr<fileL:
                p = subprocess.run('mv "' + self.files[filePtr] + '" "' + path + '"',capture_output=True, shell=True)
                tobj = time.strptime(self.data[self.files[filePtr]],'%H:%M:%S')
                t = tobj.tm_sec + tobj.tm_min * 60 + tobj.tm_hour * 60 * 60
                test = test + t
                filePtr =filePtr + 1
    
    def createCsvFile(self):
        csvData = []
        csvColumnName = ['FileName','Start','End']
        for i in self.data:
            col = {}
            col['FileName'] = i
            col['Start'] = '00:00:00'
            col['End'] = self.data[i]
            csvData.append(col)
        with open('trimdata.csv','w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csvColumnName)
            writer.writeheader()
            for data in csvData:
                    writer.writerow(data)



class trimVideo:
        
    def __init__(self,pdir = os.getcwd()):
        self.parentdir = pdir
    
    def trimVideoFromCSV(self):
        mydict = {}
        os.chdir(self.parentdir)
        df = pd.read_csv('trimdata.csv')
        print(df)
        if os.path.exists('sorted') == False:
            os.mkdir("sorted")
        for i in df.index:
            FMT = '%H:%M:%S'
            print(datetime.strptime(df['Start'][i], FMT))
            print(datetime.strptime(df['End'][i], FMT))
            tdelta = datetime.strptime(df['End'][i], FMT) - datetime.strptime(df['Start'][i], FMT) 
            outpath = os.path.join(os.getcwd(),"sorted/"+df['FileName'][i])
            subprocess.run("ffmpeg -ss " + df['Start'][i] +' -i "' + df['FileName'][i] + '" -c copy' +  " -t " + str(tdelta)+' "' + outpath+'"',capture_output=True, shell=True)
        # with open('trimdata.csv', mode='r') as infile:
        #     reader = csv.reader(infile)
        #     mydict = {rows[0]:rows[1] for rows in reader}
        # print(mydict)


# %%
# !pwd
parentdir = "/home/shivam/Desktop/Vid Processing/2/mrigank bahiya data"
# print(preparedata(parentdir).getTotalDuration())
# folder = os.listdir(parentdir)
# print(folder)
    # print(Sol(path).getTotalDuration())
# preparedata(parentdir).createCsvFile()
trimVideo(parentdir).trimVideoFromCSV()
parentdir = "/home/shivam/Desktop/Vid Processing/2/mrigank bahiya data/sorted"
preparedata(parentdir).tsec

# %%

    




