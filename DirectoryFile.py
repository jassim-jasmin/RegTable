import os
import re
from pathlib import Path
import pandas as pd

#arr = os.listdir()

#print(arr)

#for data in arr:
#    print(data)

#print("hello: " + arr[1])

def csvConvert(filenm):
    pathlist = Path('/root/Desktop/tess').glob('**/*.csv')
    for path in pathlist:
        # because path is object not string
        path_in_str = str(path)
        # print(path_in_str)

    #filedir = '/home/sysadmin/Desktop/' + folder + '/' + filenm
    filedir = os.getcwd()+filenm
    df = pd.read_csv(filedir, delimiter=',')
    # this line creates a new column, which is a Pandas series.
    # we then add the series to the dataframe, which holds our parsed CSV file
    df['NewColumn'] = filenm
    # save the dataframe to CSV
    df.to_csv(filedir, sep=',', index=False)

def folder():
    listName = os.listdir()
    pwd = os.getcwd()

    for eachName in listName:
        if not (re.search(r'\.csv$', eachName)):
            os.chdir(eachName)
            folder()
        else:
            print(eachName)
            csvConvert()
        os.chdir(pwd)
        #print(eachName)

#os.chdir(arr[0])
#print(os.listdir())

folder()