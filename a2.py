"""
Created on Thu Sep 12 12:06:51 2019

 Author: Peter George
 Class:  CMSC435 Intro to Data Science
 Asgn:   2
 
"""

import pandas as pd
import math
import time

def printHT(toPrint):
    print(toPrint.head(8))
    print(toPrint.tail(8))
    return

'''A method to get the average value of any column, ignoring question mark values'''
def getColAve(object1):
    counter = 0
    runningSum = 0
    # For Each Row Item (i) in the passed column
    for i in object1:
        # that is not equal to '?'
        if (i != '?'):
            # Make the value a float
            i = float(i)
            # Increment counter 
            counter += 1
            #Add to sum
            runningSum = runningSum + i
    toReturn = (runningSum / counter)
    toReturn = round(toReturn,5)
    return toReturn

'''Replace all '?' with the calculated average
   Fully functioning right now!'''
def replaceWithAverage(theDF):
    aDF = theDF
    ave = 0
    # For Each Column in the Dataframe Object    do stuff
    for i in aDF:
        # For Each Column that is not 'Class'    do stuff
        if (i != 'Class'):
            ave = getColAve(aDF[i])
            aDF[i] = aDF[i].replace('?', value = str(ave), inplace=False)            
    return aDF

    
'''Replace with average of matching data for similarity'''
def replaceWithConditionalAverage(theDF):
    #Split the data files into two DF objects with Yes and No respectively
    yesDF  = theDF[theDF.Class == 'Yes']
    noDF  = theDF[theDF.Class == 'No']
    #Replace the missing values with the average of their isolated data columns
    yesDF = replaceWithAverage(yesDF)
    noDF = replaceWithAverage(noDF)
    #https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
    #Join the two dataframe objects back together
    frames = [yesDF, noDF]
    toReturn = pd.concat(frames)
    return toReturn

def calcEuc(aDataframe):
    dfC = aDataframe
    dfC["ED"] = ""
    r,c = aDataframe.shape
    bigMat = [[0 for x in range(r)] for y in range(r)]
    dfA = aDataframe
    dfA = dfA.drop(columns='Class')
    dfB = aDataframe
    dfB = dfB.drop(columns='Class')
    for x in range (0,r):
        minimum = 1000
        for y in range (x+1,r):
            '''gross row calculations'''
            z=0
            theSum = 0
            while (z < 8):
                a = dfA.iat[x,z]
                if(a == '?'):
                    a = float(0)
                a = float(a)
                b = dfB.iat[y,z]
                if(b == '?' or a == '?'):
                    b = a
                b = float(b)
                theSum += ((a-b)*(a-b))
                z += 1
            theNext = ((math.sqrt(theSum))/2)
            theNext = round(theNext,5)
            if (theNext < minimum):
                minimum = theNext
                dfC.at[x, "ED"] = y
            bigMat[x][y] = theNext
            bigMat[y][x] = theNext
            bigMat[x][x] = 0            
            #print("We are at " + str(x) + " , " + str(y))
            
    print("Holy fucking shit it finished")
    return

''''''
def hotDeck(theDF):
    # https://stackoverflow.com/questions/15943769/how-do-i-get-the-row-count-of-a-pandas-dataframe
    r,c = theDF.shape  #r = number of rows #c = numb of columns
    p = 0
    toReturnDF = theDF
    return toReturnDF
start_time = time.time()
'''Read the files into python'''
df = pd.read_csv('dataset_complete.csv')
df05 = pd.read_csv('dataset_missing05.csv')
df20 = pd.read_csv('dataset_missing20.csv')
dfmock05 = pd.read_csv('dataset_missing05.csv')


'''dataset with 5% missing computed with mean here''' 
'''TODO: Calculate on the 20% missing data '''
#allCol is new list object of the dfmock05 dataset
'''TODO : Why did I stop using this'''
allCol = list(dfmock05) 
printHT(dfmock05) #Print for pre-test
#Parse each column, calculate the average in that column, replace all '?', iterate
dfmock05 = replaceWithAverage(dfmock05) 
printHT(dfmock05) #Print for post-test
#use export to set this temporary dfmock05 dataset, adjusted, to filename below
export = dfmock05.to_csv('V00396834_missing05_imputed_mean.csv', index= None, header=True)


print("\n------------Conditional Mean Imputation Start-------------\n")
'''Setting up for algorithm 2 Conditional Mean Imputation on 5% missing'''
'''TODO: Calculate on the 20% missing data '''
#Reset dfmock05 to the origial dataset from 'dataset_missing05.csv'
dfmock05 = pd.read_csv('dataset_missing05.csv')
allCol = list(dfmock05) #set allCol to list form of dfmock05
printHT(dfmock05) #Print for pre-test
dfmock05 = replaceWithConditionalAverage(dfmock05)
printHT(dfmock05) #Print for post-test
export = dfmock05.to_csv('V00396834_missing05_imputed_mean_conditional.csv', index=None, header=True)


print("\n------------Hot Deck Imputation-------------\n")
'''Setting up for algorithm 3 Hot Deck Imputation on 5% missing'''
'''TODO: Calculate on the 20% missing data '''
#Reset dfmock05 to the origial dataset from 'dataset_missing05.csv'
dfmock05 = pd.read_csv('dataset_missing05.csv')
##printHT(dfmock05) #Print for pre-test
EucDistance05 = calcEuc(dfmock05)

dfmock05 = hotDeck(dfmock05)
##printHT(dfmock05) #Print for post-test
print("--- %s seconds ---" % (time.time() - start_time))















