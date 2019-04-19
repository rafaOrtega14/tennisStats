import pandas as pd
import numpy as np
df=pd.read_csv('trainsetClayV7.csv')

for i in range(len(df['ACES_1'])):
    print(i)
    if df['ACES_1'][i]==0:
        df=df.drop(i)

df.to_csv('trainsetClayV7.csv')