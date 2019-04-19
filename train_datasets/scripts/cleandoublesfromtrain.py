from joblib import Parallel, delayed
import pandas as pd
import numpy as np
import multiprocessing
players=pd.read_csv('players_wta.csv')
df=pd.read_csv('trainsetWTA.csv')
def isdouble(name):
    if name.find('/')!=-1:
        return True
    else:
        return False
def getname(ID):
    for j in range(len(players['ID_P'])):
        if players['ID_P'][j]==ID:
            return players['NAME_P'][j]
for i in range(len(df['ID1'])):
    print(str(z)+"de :33452")
    if isdouble(getname(df['ID1'][z])):
        df=df.drop(z)
        df.to_csv('trainsetWTAV2.csv',index=False)

