import pandas as pd

a = pd.read_csv("GordoV154.csv")
b = pd.read_csv("players_atp.csv")
merged = a.merge(b, on='ID_P')
merged.to_csv('GordoV154.csv',index=False)

pd.options.mode.chained_assignment = None
df=pd.read_csv("GordoV154.csv")
for i in range(len(df['NAME_P'])):
    print(i)
    if df['NAME_P'][i].find('/')!=-1:
        df=df.drop(i)

df.to_csv('GordoV154.csv',index=False)
