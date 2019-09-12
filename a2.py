"""
Created on Thu Sep 12 12:06:51 2019

 Author: Peter George
 Class:  CMSC435 Intro to Data Science
 Asgn:   2
 
"""

import pandas as pd

'''A method to get the average value of any column, ignoring question mark values'''
def getColAve(object1):
    counter = 0
    runningSum = 0
    for i in object1:
        if (i != '?'):
            i = float(i)
            counter += 1
            runningSum = runningSum + i
    toReturn = (runningSum / counter)
    toReturn = round(toReturn,5)
    return toReturn

'''Replace all '?' with the calculated average
   Fully functioning right now!'''
def replaceWithAverage(theDF):
    aDF = theDF
    ave = 0
    for i in aDF:
        if (i != 'Class'):
            ave = getColAve(aDF[i])
            aDF[i] = aDF[i].replace('?',str(ave))            
    return aDF


'''Read the files into python'''
df = pd.read_csv('dataset_complete.csv')
df05 = pd.read_csv('dataset_missing05.csv')
df20 = pd.read_csv('dataset_missing20.csv')
dfmock05 = pd.read_csv('dataset_missing05.csv')
#print(df)

'''Column means calculated here'''

allCol = list(dfmock05)
dfmock05 = replaceWithAverage(dfmock05)
print(dfmock05)

col_05_F1 = list(df05.F1)
aF1 = getColAve(col_05_F1)


col_05_F2 = list(df05.F2)
aF2 = getColAve(col_05_F2)

col_05_F3 = list(df05.F3)
aF3 = getColAve(col_05_F3)

col_05_F4 = list(df05.F4)
aF4 = getColAve(col_05_F4)

col_05_F5 = list(df05.F5)
aF5 = getColAve(col_05_F5)

col_05_F6 = list(df05.F6)
aF6 = getColAve(col_05_F6)

col_05_F7 = list(df05.F7)
aF7 = getColAve(col_05_F7)

col_05_F8 = list(df05.F8)
aF8 = getColAve(col_05_F8)  

'''propogate mock dataframe, fill in ?'''


'''Testing a write to function'''


        

#print(col05F1)   
#df05['F1'] = df05['F1'].astype(float)























