"""
Created on Thu Sep 12 12:06:51 2019

 Author: Peter George
 Class:  CMSC435 Intro to Data Science
 Asgn:   2
 
"""

import pandas as pd

df = pd.read_csv('dataset_complete.csv')
df05 = pd.read_csv('dataset_missing05.csv')
df20 = pd.read_csv('dataset_missing20.csv')
print(df)