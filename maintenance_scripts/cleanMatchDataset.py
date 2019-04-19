import pandas as pd

a = pd.read_csv("GordoV154.csv")
for i in range(len(a['ACES'])):
    if a['ACES'][i]==0:
        a=a.drop(i)
a.to_csv('GordoV154.csv',index=False)
