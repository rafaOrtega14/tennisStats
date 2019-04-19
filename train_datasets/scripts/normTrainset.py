import pandas as pd


df=pd.read_csv('TENNISClay.csv')    
avg=df['RESULT_G'].mean()  
df['FS_1']=df['FS_1']*avg
df['FS_2']=df['FS_2']*avg
df['FSOF_1']=df['FSOF_1']*avg
df['FSOF_2']=df['FSOF_2']*avg
df['ACES_1']=df['ACES_1']*avg
df['ACES_2']=df['ACES_2']*avg
df['DF_1']=df['DF_1']*avg
df['DF_2']=df['DF_2']*avg
df['W1S_1']=df['W1S_1']*avg
df['W1S_2']=df['W1S_2']*avg
df['W1SOF_1']=df['W1SOF_1']*avg
df['W1SOF_2']=df['W1SOF_2']*avg
df['WIS_1']=df['WIS_1']*avg
df['WIS_2']=df['WIS_2']*avg
df['BP_1']=df['BP_1']*avg
df['BP_2']=df['BP_2']*avg
df['BPOF_1']=df['BPOF_1']*avg
df['BPOF_2']=df['BPOF_2']*avg
df['TPW_1']=df['TPW_1']*avg
df['TPW_2']=df['TPW_2']*avg
df['RPW_1']=df['RPW_1']*avg
df['RPW_2']=df['RPW_2']*avg
df['RPWOF_1']=df['RPWOF_1']*avg
df['RPWOF_2']=df['RPWOF_2']*avg

df.to_csv('TENNISClay.csv',index=False)
        