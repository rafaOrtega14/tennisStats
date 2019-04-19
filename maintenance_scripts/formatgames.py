from joblib import Parallel, delayed
import pandas as pd
import numpy as np
import multiprocessing

df=pd.read_csv('TENNIS154.csv')

def sum_digits(noformatext):
    formatext=removetiebreaks(noformatext)
    return sum(int(x) for x in formatext if x.isdigit())

def removetiebreaks(text):
    start = text.find( '(' )
    end = text.find( ')' )
    if start != -1 and end != -1:
        return text.replace(text[start+1:end],'')
    else:
        return text

for z in range(len(df['ID1'])):
    print(z)
    df.ix[z,'RESULT_G']=sum_digits(df['RESULT_G'][z])

df.to_csv('TENNIS154.csv',index=False)

