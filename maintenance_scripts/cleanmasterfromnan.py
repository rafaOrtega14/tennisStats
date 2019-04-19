import pandas as pd
import numpy as np

df=pd.read_csv('TENNIS154.csv',low_memory=False)
for i in range(len(df['ID1'])):
    print(i)
    if df['ACES_1'][i]=='N' or df['ACES_2'][i]=='N' or df['BPOF_1'][i]=='N' or df['BPOF_2'][i]=='N' or df['BP_1'][i]=='N' or df['BP_2'][i]=='N' or df['DF_1'][i]=='N' or df['DF_2'][i]=='N' or df['FSOF_1'][i]=='N' or df['FSOF_2'][i]=='N' or df['FS_1'][i]=='N' or df['FS_2'][i]=='N' or df['RPWOF_1'][i]=='N' or df['RPWOF_2'][i]=='N' or df['RPW_1'][i]=='N' or df['RPW_2'][i]=='N' or df['TPW_1'][i]=='N' or df['TPW_2'][i]=='N' or df['W1SOF_1'][i]=='N' or df['W1SOF_2'][i]=='N' or df['W1S_1'][i]=='N' or df['W1S_2'][i]=='N' or df['WIS_1'][i]=='N' or df['WIS_2'][i]=='N':
        df=df.drop(i)

df.to_csv('TENNIS154.csv',index=False)