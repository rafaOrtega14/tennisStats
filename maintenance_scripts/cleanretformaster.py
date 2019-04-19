import pandas as pd
import numpy as np

df=pd.read_csv('TENNIS154.csv')
for i in range(len(df['ACES_1'])):
    print(i)
    if df['RESULT_G'][i].find('ret')!=-1:
        df=df.drop(i)

df.to_csv('TENNIS154.csv')