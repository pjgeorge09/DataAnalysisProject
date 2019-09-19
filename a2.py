"""
Created on Thu Sep 12 12:06:51 2019

 Author: Peter George
 Class:  CMSC435 Intro to Data Science
 Asgn:   2
 
"""

import pandas as pd

def printHT(toPrint):
    print(toPrint.head(8))
    print(toPrint.tail(8))
    return

'''A method to get the average value of any column, ignoring question mark values'''
def getColAve(object1):
    counter = 0
    runningSum = 0
    # For Each Column (i) in the Dataframe (object1) do stuff
    for i in object1:
        # For Each Value in Column Above that does not equal '?'   do stuff
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
    for i in aDF:
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

'''Read the files into python'''
df = pd.read_csv('dataset_complete.csv')
df05 = pd.read_csv('dataset_missing05.csv')
df20 = pd.read_csv('dataset_missing20.csv')
dfmock05 = pd.read_csv('dataset_missing05.csv')


'''dataset with 5% missing computed with mean here''' 
'''TODO: Calculate on the 20% missing data '''
#allCol is new list object of the dfmock05 dataset
allCol = list(dfmock05)
##printHT(dfmock05) #Print for pre-test
#Parse each column, calculate the average in that column, replace all '?', iterate
dfmock05 = replaceWithAverage(dfmock05) 
##printHT(dfmock05) #Print for post-test
#use export to set this temporary dfmock05 dataset, adjusted, to filename below
export = dfmock05.to_csv('V00396834_missing05_imputed_mean.csv', index= None, header=True)


print("\n------------Conditional Mean Imputation Start-------------\n")
'''Setting up for algorithm 2 Conditional Mean Imputation on 5% missing'''
'''TODO: Calculate on the 20% missing data '''
#Reset dfmock05 to the origial dataset from 'dataset_missing05.csv'
dfmock05 = pd.read_csv('dataset_missing05.csv')
allCol = list(dfmock05) #set allCol to list form of dfmock05
##printHT(dfmock05) #Print for pre-test
dfmock05 = replaceWithConditionalAverage(dfmock05)
##printHT(dfmock05) #Print for post-test
export = dfmock05.to_csv('V00396834_missing05_imputed_mean_conditional.csv', index=None, header=True)






















