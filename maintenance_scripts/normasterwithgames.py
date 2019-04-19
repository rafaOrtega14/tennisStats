from joblib import Parallel, delayed
import pandas as pd
import numpy as np
import multiprocessing

df=pd.read_csv('TENNIS154.csv',low_memory=False)
avg=df['RESULT_G'].mean()
print(avg)
def foo(i):
    print(i)
    juegos=df['RESULT_G'][i]
    players = {'FS_1':(df['FS_1'][i]/juegos)*avg,'FSOF_1':(df['FSOF_1'][i]/juegos)*avg,
        'ACES_1':(df['ACES_1'][i]/juegos)*avg,'DF_1':(df['DF_1'][i]/juegos)*avg,
        'W1S_1':(df['W1S_1'][i]/juegos)*avg,'W1SOF_1':(df['W1SOF_1'][i]/juegos)*avg,
        'WIS_1':(df['WIS_1'][i]/juegos)*avg,'BP_1':(df['BP_1'][i]/juegos)*avg,
        'BPOF_1':(df['BPOF_1'][i]/juegos)*avg,'TPW_1':(df['TPW_1'][i]/juegos)*avg,
        'RPW_1':(df['RPW_1'][i]/juegos)*avg,'RPWOF_1':(df['RPWOF_1'][i]/juegos)*avg,
        'ID1':df['ID1'][i],'FS_2':(df['FS_2'][i]/juegos)*avg,
        'FSOF_2':(df['FSOF_2'][i]/juegos)*avg,'ACES_2':(df['ACES_2'][i]/juegos)*avg,
        'DF_2':(df['DF_2'][i]/juegos)*avg,'W1S_2':(df['W1S_2'][i]/juegos)*avg,
        'RPW_2':(df['RPW_2'][i]/juegos)*avg,'RPWOF_2':(df['RPWOF_2'][i]/juegos)*avg,
        'W1SOF_2':(df['W1SOF_2'][i]/juegos)*avg,'WIS_2':(df['WIS_2'][i]/juegos)*avg,
        'BP_2':(df['BP_2'][i]/juegos)*avg,'BPOF_2':(df['BPOF_2'][i]/juegos)*avg,
        'TPW_2':(df['TPW_2'][i]/juegos)*avg,'ID2':df['ID2'][i],'RESULT_G':juegos,'COURT':df['NAME_C'][i]}
    return players

players=Parallel(n_jobs=multiprocessing.cpu_count())(delayed(foo)(z) for z in range(len(df['ID1'])))
df3 = pd.DataFrame.from_dict(players)
df3.to_csv('TENNIS154.csv',index=False)