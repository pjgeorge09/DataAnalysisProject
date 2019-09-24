"""
Created on Thu Sep 12 12:06:51 2019

 Author: Peter George
 Class:  CMSC435 Intro to Data Science
 Asgn:   2
 
"""

import pandas as pd
import math
import time

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

'''A method to get all of the Euclidean Distances, to be calculated only once and stored
   This method ran for about 1.5 hours on each set, 5% missing and 20% missing'''
def calcEuc(aDataframe):
    #Gets the dataframe length in rows, columns respectively
    r,c = aDataframe.shape
    # Instantiate huge matrix. Other data forms proved difficult.
    matrixThing = [[0 for q in range(r)] for w in range(r)]
    
    for x in range (0,r): 
        #print(x) #For tracking
        #select out a row
        tuple1 = aDataframe.iloc[x]
        #We only care for x+1 because we already know x,x and when at (3,1) its same ED as (1,3)
        for y in range(x+1,r):
            if(x != y and x < y):
                #compare and store to every row
                tuple2 = aDataframe.iloc[y]
                #calculate the ED and store it
                theED = ED(tuple1,tuple2)
                theED = round(theED,5)
                #The key,key = thisED    # Could not reverse with other data structs, problems ensued
                matrixThing[x][y] = theED
                matrixThing[y][x] = theED   
        matrixThing[x][x] = 100
    # Turns it into a DF
    DF = pd.DataFrame(matrixThing)    
    return DF

def ED(object1, object2):
    z=0
    theSum = 0
    #iterate for only 8 columns, avoiding Class
    while(z<8):
        a = object1[z]
        b = object2[z]
        if(a != '?' and b!= '?'):
            a = float(a)
            b = float(b)
            theSum = theSum + ((a-b)*(a-b))
        z = z + 1
    #outside while loop, theSum should now have all of the data
    toReturn = ((math.sqrt(theSum))/2) #this should be the euc distance
    return toReturn



'''Use the data set of nearest neighbors to replace all '?' data cells'''
def hotDeck(aDF,nnDF):
    #Get the df into manipulatble object
    theDF = aDF
    r,c = theDF.shape
    for index in range(0,r):
        #The row that may have '?' values
        row = theDF.iloc[index] # First row from theDF
        # This is the row number of the closest neighbor
        cN = nnDF.iat[index,0]
        row2 = theDF.iloc[cN]  # Some other row from theDF
        #take care of the easy ones
        for j in row:
            nm = 0
            if(j=='?'):
                j = row2[nm]
            nm += 1
        # The row from cN now as a compareable row
        z=0
        #don't check class
        while(z<8):
            a = row[z] #value at theDF[index,z]
            if(a=='?'): #if it's a '?'
                c = row2 #STORE THE ROW EVERY TIME
                b = row2[z] #value at theDF[closest,z]
                value1 = cN
                failure = 1 
                while(b=='?' and failure < 8): #cant store another '?'
                    value1 = nnDF.iat[index,failure] #get index of compareRow's NN
                    c = theDF.iloc[value1] #newRow to compare from that inde
                    b = c[z] #b = new, non-'?' hopefully
                    failure = failure+1
                    
                #got to here, so b != '?'
                theDF.iat[index,z] = b
            z = z+1
    return theDF

'''Use the data set of nearest neighbors to replace all '?' data cells'''
def hotDeckCon(aDF,nnDF):
    #Get the df into manipulatble object
    theDF = aDF
    r,c = theDF.shape
    for index in range(0,r):
        #The row that may have '?' values
        row = theDF.iloc[index] # First row from theDF
        # This is the row number of the closest neighbor
        cN = nnDF.iat[index,0]
        row2 = theDF.iloc[cN]  # Some other row from theDF
        # The row from cN now as a compareable row
        for j in row:
            nm = 0
            if(j=='?'):
                j = row2[nm]
            nm += 1
        z=0
        #don't check class
        while(z<8):
            a = row[z] #value at theDF[index,z]
            if(a=='?'): #if it's a '?'
                c = row2 #STORE THE ROW EVERY TIME
                # index of the closest Number
                value1 = cN
                # counter
                failure = 1
                b = c[z] #value at theDF[closest,z]
                if(nnDF.at[index,'Class'] != nnDF.at[value1,'Class']):
                        b='?'  
                # change the row to the next closest, up to 30 times
                while(b=='?' and failure < 29): #cant store another '?'
                    value1 = nnDF.iat[index,failure] #get index of compareRow's NN
                    c = theDF.iloc[value1] #newRow to compare from that index ##BUG FOUND
                    b = c[z] #b = new, non-'?' hopefully
                    failure = failure+1
                    if(nnDF.at[index,'Class'] != nnDF.at[value1,'Class']):
                        b='?'
                    
                    #938 above = yes, below = no
                    
                #got to here, so b != '?'
                theDF.iat[index,z] = b
            z = z+1
    return theDF

''' A method to simply append the 'Class' column to the end of theDF 
    returns theDF with appended column'''
def appendClass(theDF):
    #arbitrary as they are all the same
    tempDF = pd.read_csv('dataset_missing05.csv')
    nnDF = theDF
    nnDF['Class'] = tempDF['Class']
    return nnDF

''' NOTE: My biggest blunder here. If I have/had time I would fix to some better
    method.
    A method to find the index of the closest 30 neighbors to a row
    returns nn, a created dataframe'''
def findCloseNeighbors(bigDF):
    nn = pd.DataFrame(columns=['N1','N2','N3','N4','N5','N6','N7','N8',
                       'N9','N10','N11','N12','N13','N14','N15',
                       'N16','N17','N18','N19','N20','N21','N22',
                       'N23','N24','N25','N26','N27','N28','N29'])
    # fix is to skip the first column, getting error at 0
    fix = 0
    for i in bigDF:
        if(fix != 0):
            # Get the index of the nearest neighbor (minimum of column)                
            minimum = bigDF[i].idxmin()
            bigDF.at[minimum,i] = 2
            min2 = bigDF[i].idxmin()
            bigDF.at[min2,i] = 2
            min3 = bigDF[i].idxmin()
            bigDF.at[min3,i]=2
            min4 = bigDF[i].idxmin()
            bigDF.at[min4,i]=2
            min5 = bigDF[i].idxmin()
            bigDF.at[min5,i]=2
            min6 = bigDF[i].idxmin()
            bigDF.at[min6,i]=2
            min7 = bigDF[i].idxmin()
            bigDF.at[min7,i]=2
            min8 = bigDF[i].idxmin()
            bigDF.at[min8,i]=2
            min9 = bigDF[i].idxmin()
            bigDF.at[min9,i] = 2
            min10 = bigDF[i].idxmin()
            bigDF.at[min10,i]=2
            min11 = bigDF[i].idxmin()
            bigDF.at[min11,i]=2
            min12 = bigDF[i].idxmin()
            bigDF.at[min12,i]=2
            min13 = bigDF[i].idxmin()
            bigDF.at[min13,i]=2
            min14 = bigDF[i].idxmin()
            bigDF.at[min14,i]=2
            min15 = bigDF[i].idxmin()
            bigDF.at[min15,i]=2
            min16 = bigDF[i].idxmin()
            bigDF.at[min16,i] = 2
            min17 = bigDF[i].idxmin()
            bigDF.at[min17,i]=2
            min18 = bigDF[i].idxmin()
            bigDF.at[min18,i]=2
            min19 = bigDF[i].idxmin()
            bigDF.at[min19,i]=2
            min20 = bigDF[i].idxmin()
            bigDF.at[min20,i]=2
            min21 = bigDF[i].idxmin()
            bigDF.at[min21,i]=2
            min22 = bigDF[i].idxmin()
            bigDF.at[min22,i]=2
            min23 = bigDF[i].idxmin()
            bigDF.at[min23,i] = 2
            min24 = bigDF[i].idxmin()
            bigDF.at[min24,i]=2
            min25 = bigDF[i].idxmin()
            bigDF.at[min25,i]=2
            min26 = bigDF[i].idxmin()
            bigDF.at[min26,i]=2
            min27 = bigDF[i].idxmin()
            bigDF.at[min27,i]=2
            min28 = bigDF[i].idxmin()
            bigDF.at[min28,i]=2
            min29 = bigDF[i].idxmin()
            bigDF.at[min29,i]=2
            # Set this to it's row value in nn
            nn = nn.append({'N1': minimum, 'N2':min2, 'N3':min3, 'N4':min4,
                            'N5':min5, 'N6':min6, 'N7':min7, 'N8':min8, 'N9':min9,
                            'N10':min5, 'N11':min6, 'N12':min7, 'N13':min8,
                            'N14':min14, 'N15':min15, 'N16':min16,'N17':min17,'N18':min18,
                            'N19':min19,'N20':min20,'N21':min21,'N22':min22,'N23':min23,
                            'N24':min24,'N25':min25,'N26':min26,'N27':min27,'N28':min28,'N29':min29
                            }, ignore_index=True)
        fix = 1
    return nn

''' A method to calculate the Mean Absolute Error (MAE)
    Takes 3 parameters in, the DF with missing data, the DF imputed, and the true DF
    counter counts total '?' occurances
    toAdd sums the total of {x_i - t_i}
    returns the sum divided by the number of occurances, rounded to 4 dec'''
def MAE(missingDF, imputedDF, completedDF):
    #Define the shape. They should all be the same
    r,c = imputedDF.shape
    #Counter for number of question marks
    counter = 0
    toAdd = 0
    for aCol in missingDF:
        col = missingDF[aCol]
        index = 0
        for i in col:
            if(i=='?'):
                counter +=1
                maeX = imputedDF.at[index,aCol]
                if(maeX == '?'):
                    maeX = 0
                maeT = completedDF.at[index,aCol]
                maeX = float(maeX)
                maeT = float(maeT)
                toAdd = toAdd + abs(maeX - maeT)
            index += 1
    toReturn = toAdd/counter
    toReturn = round(toReturn,4)                   
    return toReturn

'''A method to parse two data files and print the number of "?" before and after'''
def countQuestions(df1,df2):
    count1 = 0
    count2 = 0
    for aCol in df1:
        col = df1[aCol]
        for i in col:
            if (i=='?'):
                count1 += 1
    for bCol in df2:
        colB = df2[bCol]
        for j in colB:
            if(j=='?'):
                count2 += 1
    print("There were " + str(count1) + " question marks")
    print("There are now " + str(count2) + " question marks")
    return
#clock start
start_time = time.time()
print("--- %s seconds ---" % (start_time))

'''Read the files into python'''
df = pd.read_csv('dataset_complete.csv')
df05 = pd.read_csv('dataset_missing05.csv')
df20 = pd.read_csv('dataset_missing20.csv')
dfmock05 = pd.read_csv('dataset_missing05.csv')
dfmock20 = pd.read_csv('dataset_missing20.csv')

print("\n------------------------ Mean Imputation Start-------------------------\n")
#Parse each column, calculate the average in that column, replace all '?', iterate
# 5% missing
dfmock05 = replaceWithAverage(dfmock05) 
dfmock05.to_csv('V00396834_missing05_imputed_mean.csv', index= None, header=True)
#20% missing
dfmock20 = replaceWithAverage(dfmock20)
dfmock20.to_csv('V00396834_missing20_imputed_mean.csv', index = None, header=True)


print("\n------------------------Conditional Mean Imputation Start-------------------------\n")
#Reset dfmock05 to the origial dataset from 'dataset_missing05.csv'
dfmock05 = pd.read_csv('dataset_missing05.csv')
dfmock05 = replaceWithConditionalAverage(dfmock05)
dfmock05.to_csv('V00396834_missing05_imputed_mean_conditional.csv', index=None, header=True)

dfmock20 = pd.read_csv('dataset_missing20.csv')
dfmock20 = replaceWithConditionalAverage(dfmock20)
dfmock20.to_csv('V00396834_missing20_imputed_mean_conditional.csv',index=None,header=True)


print("\n------------------------Hot Deck Imputation-------------------------\n")
#Reset dfmock05 to the origial dataset from 'dataset_missing05.csv'
dfmock05 = pd.read_csv('dataset_missing05.csv')
dfmock20 = pd.read_csv('dataset_missing20.csv')

'''This was done once and stored but left in code to be seen'''
all05 = calcEuc(dfmock05) 
all20 = calcEuc(dfmock20)
all05.to_csv('ED05.csv', index=True, header=True)
all20.to_csv('ED20.csv', index=True, header=True)
time.sleep(8)

#Calculating 40 nearest neighbors, only used once 
finder05 = pd.read_csv('ED05.csv')
n05 = findCloseNeighbors(finder05)
n05 = appendClass(n05) # Literally just appends the 'Class' column to the end
n05.to_csv('nnDF05.csv', index = False, header=True)

finder20 = pd.read_csv('ED20.csv')
n20 = findCloseNeighbors(finder20)
n20 = appendClass(n20) # Literally just appends the 'Class' column to the end
n20.to_csv('nnDF20.csv',index=False,header=True)

'''I now have all the closest neighbors in a dataframe of 1 column for 05 and 20'''
nnDF05 = pd.read_csv('nnDF05.csv')
nnDF20 = pd.read_csv('nnDF20.csv')
dfmock05 = hotDeck(dfmock05,nnDF05)
dfmock20 = hotDeck(dfmock20,nnDF20)
dfmock05.to_csv('V00396834_missing05_imputed_hd.csv', index=False, header=True)
dfmock20.to_csv('V00396834_missing20_imputed_hd.csv', index=False, header=True)


print("\n------------------------Hot Deck Conditional Start-------------------------\n")
dfmock05 = pd.read_csv('dataset_missing05.csv')
dfmock20 = pd.read_csv('dataset_missing20.csv')

dfmock05 = hotDeckCon(dfmock05,nnDF05)
dfmock20 = hotDeckCon(dfmock20,nnDF20)

dfmock05.to_csv('V00396834_missing05_imputed_hd_conditional.csv', index=False, header=True)
dfmock20.to_csv('V00396834_missing20_imputed_hd_conditional.csv', index=False, header=True)


print("\n------------------------MAE values-------------------------\n")
miss05 = pd.read_csv('dataset_missing05.csv')
miss20 = pd.read_csv('dataset_missing20.csv')
complete = pd.read_csv('dataset_complete.csv')

# MAE 05 MEAN
imp05 = pd.read_csv('V00396834_missing05_imputed_mean.csv')
mean05 = MAE(miss05,imp05,complete)
print("MAE_05_mean = " + str(mean05))

# MAE 05 CONDITIONAL
imp05 = pd.read_csv('V00396834_missing05_imputed_mean_conditional.csv')
meanC05 = MAE(miss05,imp05,complete)
print("MAE_05_mean_conditional = " + str(meanC05))

# MAE 05 HOT DECK
imp05 = pd.read_csv('V00396834_missing05_imputed_hd.csv')
hd05 = MAE(miss05,imp05,complete)
print("MAE_05_hd = " + str(hd05))

# MAE 05 HOT DECK CONDITIONAL
imp05 = pd.read_csv('V00396834_missing05_imputed_hd_conditional.csv')
hdc05 = MAE(miss05,imp05,complete)
print("MAE_05_hd_conditional = " + str(hdc05))

# MAE 520MEAN
imp20 = pd.read_csv('V00396834_missing20_imputed_mean.csv')
mean20 = MAE(miss20,imp20,complete)
print("MAE_20_mean = " + str(mean20))

# MAE 05 CONDITIONAL
imp20 = pd.read_csv('V00396834_missing20_imputed_mean_conditional.csv')
meanC20 = MAE(miss20,imp20,complete)
print("MAE_20_mean_conditional = " + str(meanC20))

# MAE 05 HOT DECK
imp20 = pd.read_csv('V00396834_missing20_imputed_hd.csv')
hd20 = MAE(miss20,imp20,complete)
print("MAE_20_hd = " + str(hd20))

# MAE 05 HOT DECK CONDITIONAL
imp20 = pd.read_csv('V00396834_missing20_imputed_hd_conditional.csv')
hdc20 = MAE(miss20,imp20,complete)
print("MAE_20_hd_conditional = " + str(hdc20))


print("--- %s seconds ---" % (time.time() - start_time))















