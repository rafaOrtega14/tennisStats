from joblib import Parallel, delayed
import pandas as pd
import numpy as np
import multiprocessing

pd.options.mode.chained_assignment = None
df=pd.read_csv("TrainsetClayV3.csv",low_memory=False)
def weightaverage(x,y,v,grid):
    for s in range(grid.shape[0]):
        for t in range(grid.shape[1]):
            distance = np.sqrt((x-s)**2+(y-t)**2)
            if (distance).min()==0:
                grid[s,t] = v[(distance).argmin()]
            else:
                total = np.sum(1/(distance))
                grid[s,t] = np.sum(v/(distance)/total)
    return np.average(grid[0])

def foo(partido):
    FS1val=[]
    FSOF1val=[]
    ACES1val=[]
    DF1val=[]
    W1S1val=[]
    W1SOF1val=[]
    WIS1val=[]
    BP1val=[]
    BPOF1val=[]
    TPW1val=[]
    RPW1val=[]
    RPWOF1val=[]
    FS2val=[]
    FSOF2val=[]
    ACES2val=[]
    DF2val=[]
    W1S2val=[]
    W1SOF2val=[]
    WIS2val=[]
    BP2val=[]
    BPOF2val=[]
    TPW2val=[]
    RPW2val=[]
    RPWOF2val=[]
    eloIWA=[]
    eloIWA2=[]
    desde1=[]
    hasta1=[]
    desde2=[]
    hasta2=[]
    cont1=0
    cont2=0
    print(str(partido)+" de: "+str(len(df['ID1'])))
    for i in reversed(range(partido-5000,partido+1)):
        if df['ID1'][i]==df['ID1'][partido]:
            if cont1<10:
                FS1val.append(df['FS_1'][i])
                FSOF1val.append(df['FSOF_1'][i])
                ACES1val.append(df['ACES_1'][i])
                DF1val.append(df['DF_1'][i])
                W1S1val.append(df['W1S_1'][i])
                W1SOF1val.append(df['W1SOF_1'][i])
                WIS1val.append(df['WIS_1'][i])
                BP1val.append(df['BP_1'][i]) 
                BPOF1val.append(df['BPOF_1'][i])
                TPW1val.append(df['TPW_1'][i])
                RPW1val.append(df['RPW_1'][i])
                RPWOF1val.append(df['RPWOF_1'][i])
                eloIWA.append(df['eloWinner'][i])
                if cont1==0:
                    hasta1.append(partido+1)
                    desde1.append(partido+1)
                else:
                    desde1.append(hasta1[cont1-1])
                    hasta1.append(i)
                cont1=cont1+1

        if df['ID2'][i]==df['ID2'][partido]:
            if cont2<10:
                FS2val.append(df['FS_2'][i])
                FSOF2val.append(df['FSOF_2'][i])
                ACES2val.append(df['ACES_2'][i])
                DF2val.append(df['DF_2'][i])
                W1S2val.append(df['W1S_2'][i])
                W1SOF2val.append(df['W1SOF_2'][i])
                WIS2val.append(df['WIS_2'][i]) 
                BP2val.append(df['BP_2'][i])
                BPOF2val.append(df['BPOF_2'][i])
                TPW2val.append(df['TPW_2'][i])
                RPW2val.append(df['RPW_2'][i])
                RPWOF2val.append(df['RPWOF_2'][i])
                eloIWA2.append(df['eloLoser'][i])
                if cont2==0:
                    hasta2.append(partido+1)
                    desde2.append(partido+1)
                else:
                    desde2.append(hasta2[cont2-1])
                    hasta2.append(i)
                cont2=cont2+1
            
        if df['ID1'][i]==df['ID2'][partido]:
            if cont2<10:
                FS2val.append(df['FS_1'][i])
                FSOF2val.append(df['FSOF_1'][i])
                ACES2val.append(df['ACES_1'][i])
                DF2val.append(df['DF_1'][i])
                W1S2val.append(df['W1S_1'][i])
                W1SOF2val.append(df['W1SOF_1'][i])
                WIS2val.append(df['WIS_1'][i])
                BP2val.append(df['BP_1'][i])
                BPOF2val.append(df['BPOF_1'][i])
                TPW2val.append(df['TPW_1'][i])
                RPW2val.append(df['RPW_1'][i])
                RPWOF2val.append(df['RPWOF_1'][i])
                eloIWA2.append(df['eloWinner'][i])
                if cont2==0:
                    hasta2.append(partido+1)
                    desde2.append(partido+1)
                else:
                    desde2.append(hasta2[cont2-1])
                    hasta2.append(i)
            
        if df['ID2'][i]==df['ID1'][partido]:
            if cont1<10:
                FS1val.append(df['FS_2'][i])
                FSOF1val.append(df['FSOF_2'][i])
                ACES1val.append(df['ACES_2'][i])
                DF1val.append(df['DF_2'][i])
                W1S1val.append(df['W1S_2'][i])
                W1SOF1val.append(df['W1SOF_2'][i])
                WIS1val.append(df['WIS_2'][i])
                BP1val.append(df['BP_2'][i])
                BPOF1val.append(df['BPOF_2'][i])
                TPW1val.append(df['TPW_2'][i])
                RPW1val.append(df['RPW_2'][i])
                RPWOF1val.append(df['RPWOF_2'][i])
                eloIWA.append(df['eloLoser'][i])
                if cont1==0:
                    hasta1.append(partido+1)
                    desde1.append(partido+1)
                else:
                    desde1.append(hasta1[cont1-1])
                    hasta1.append(i)
                cont1=cont1+1
    if cont1==10 and cont2==10:
        desde1=np.array(desde1)
        hasta1=np.array(hasta1)
        desde2=np.array(desde2)
        hasta2=np.array(hasta2)
        grid1 = np.zeros((cont1,cont1),dtype='float32')
        grid2 = np.zeros((cont2,cont2),dtype='float32')
        players = {'FS_1':weightaverage(desde1,hasta1,FS1val,grid1),'FSOF_1': weightaverage(desde1,hasta1,FSOF1val,grid1),
        'ACES_1': weightaverage(desde1,hasta1,ACES1val,grid1),'DF_1': weightaverage(desde1,hasta1,DF1val,grid1),
        'W1S_1':weightaverage(desde1,hasta1,W1S1val,grid1),'W1SOF_1':weightaverage(desde1,hasta1,W1SOF1val,grid1),
        'WIS_1':weightaverage(desde1,hasta1,WIS1val,grid1),'BP_1':weightaverage(desde1,hasta1,BP1val,grid1),
        'BPOF_1':weightaverage(desde1,hasta1,BPOF1val,grid1),'TPW_1':weightaverage(desde1,hasta1,TPW1val,grid1),
        'RPW_1':weightaverage(desde1,hasta1,RPW1val,grid1),'RPWOF_1':weightaverage(desde1,hasta1,RPWOF1val,grid1),
        'ID1':df['ID1'][partido],'FS_2':weightaverage(desde2,hasta2,FS2val,grid2),
        'FSOF_2': weightaverage(desde2,hasta2,FSOF2val,grid2),'ACES_2': weightaverage(desde2,hasta2,ACES2val,grid2),
        'DF_2': weightaverage(desde2,hasta2,DF2val,grid2),'W1S_2':weightaverage(desde2,hasta2,W1S2val,grid2),
        'RPW_2':weightaverage(desde2,hasta2,RPW2val,grid2),'RPWOF_2':weightaverage(desde2,hasta2,RPWOF2val,grid2),
        'W1SOF_2':weightaverage(desde2,hasta2,W1SOF2val,grid2),'WIS_2':weightaverage(desde2,hasta2,WIS2val,grid2),
        'BP_2':weightaverage(desde2,hasta2,BP2val,grid2),'BPOF_2':weightaverage(desde2,hasta2,BPOF2val,grid2),
        'TPW_2':weightaverage(desde2,hasta2,TPW2val,grid2),'ID2':df['ID2'][partido],
        'RESULT_G':df['RESULT_G'][partido],'eloWinner':df['eloWinner'][partido],'eloLoser':df['eloLoser'][partido],
        'eloIWA':weightaverage(desde1,hasta1,eloIWA,grid1),'eloIWA_2':weightaverage(desde2,hasta2,eloIWA2,grid2)}

    else:
        players = {'FS_1':0,'FSOF_1': 0,'ACES_1': 0,'DF_1': 0, 'W1S_1':0,
        'W1SOF_1':0,'WIS_1':0,'BP_1':0,'BPOF_1':0,'TPW_1':0,'RPW_1':0,
        'RPWOF_1':0,'ID1':df['ID1'][partido],'FS_2':0,'FSOF_2': 0,'ACES_2': 0,'DF_2': 0,
        'W1S_2':0,'RPW_2':0,'RPWOF_2':0,'W1SOF_2':0,'WIS_2':0,'BP_2':0,
        'BPOF_2':0,'TPW_2':0,'ID2':df['ID2'][partido],'RESULT_G':0,'eloWinner':df['eloWinner'][partido],
        'eloLoser':df['eloLoser'][partido]}
    return players
players=Parallel(n_jobs=multiprocessing.cpu_count())(delayed(foo)(z) for z in range(5001,len(df['ID1'])))
df3 = pd.DataFrame.from_dict(players)
df3.to_csv('trainsetClayV6.csv',index=False)
