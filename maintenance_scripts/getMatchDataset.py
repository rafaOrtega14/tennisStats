from joblib import Parallel, delayed
import pandas as pd
import numpy as np
import multiprocessing

df=pd.read_csv("TENNISHard.csv",low_memory=False)
pd.options.mode.chained_assignment = None
rep2=df['ID2'].value_counts().index.tolist()
rep1=df['ID1'].value_counts().index.tolist()
ID1=[]
ID2=[]
for i in range(len(rep1)):
    if rep1[i]+rep2[i]>10:
        ID1.append(rep1[i])
        ID2.append(rep2[i])
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
def foo(z):
    FSaux=[]
    FSOFaux=[]
    ACESaux=[]
    DFaux=[]
    W1Saux=[]
    W1SOFaux=[]
    WISaux=[]
    BPaux=[]
    BPOFaux=[]
    TPWaux=[]
    RPWaux=[]
    RPWOFaux=[]
    FSrival=[]
    FSOFrival=[]
    ACESrival=[]
    DFrival=[]
    W1Srival=[]
    W1SOFrival=[]
    WISrival=[]
    BPrival=[]
    BPOFrival=[]
    TPWrival=[]
    RPWrival=[]
    RPWOFrival=[]
    desde=[]
    hasta=[]
    cont=0
    print(str(z)+"de :"+str(len(ID1)))
    for j in reversed(range(len(df['FS_1'])-5000,len(df['FS_1']))):
        if df['ID1'][j]==ID2[z] and cont<10:
            FSaux.append(df['FS_1'][j])
            FSOFaux.append(df['FSOF_1'][j])
            ACESaux.append(df['ACES_1'][j])
            DFaux.append(df['DF_1'][j])
            W1Saux.append(df['W1S_1'][j])
            WISaux.append(df['WIS_1'][j])
            W1SOFaux.append(df['W1SOF_1'][j])
            BPaux.append(df['BP_1'][j])
            BPOFaux.append(df['BPOF_1'][j])
            TPWaux.append(df['TPW_1'][j])
            RPWaux.append(df['RPW_1'][j])
            RPWOFaux.append(df['RPWOF_1'][j])
            FSrival.append(df['FS_2'][j])
            FSOFrival.append(df['FSOF_2'][j])
            ACESrival.append(df['ACES_2'][j])
            DFrival.append(df['DF_2'][j])
            W1Srival.append(df['W1S_2'][j])
            WISrival.append(df['WIS_2'][j])
            W1SOFrival.append(df['W1SOF_2'][j])
            BPrival.append(df['BP_2'][j])
            BPOFrival.append(df['BPOF_2'][j])
            TPWrival.append(df['TPW_2'][j])
            RPWrival.append(df['RPW_2'][j])
            RPWOFrival.append(df['RPWOF_2'][j])
            if cont==0:
                hasta.append(z+1)
                desde.append(z+1)
            else:
                desde.append(hasta[cont-1])
                hasta.append(j)
            cont=cont+1
        if df['ID2'][j]==ID2[z] and cont<10:
            FSaux.append(df['FS_2'][j])
            FSOFaux.append(df['FSOF_2'][j])
            ACESaux.append(df['ACES_2'][j])
            DFaux.append(df['DF_2'][j])
            W1Saux.append(df['W1S_2'][j])
            WISaux.append(df['WIS_2'][j])
            W1SOFaux.append(df['W1SOF_2'][j])
            BPaux.append(df['BP_2'][j])
            BPOFaux.append(df['BPOF_2'][j])
            TPWaux.append(df['TPW_2'][j])
            RPWaux.append(df['RPW_2'][j])
            RPWOFaux.append(df['RPWOF_2'][j])
            FSrival.append(df['FS_1'][j])
            FSOFrival.append(df['FSOF_1'][j])
            ACESrival.append(df['ACES_1'][j])
            DFrival.append(df['DF_1'][j])
            W1Srival.append(df['W1S_1'][j])
            WISrival.append(df['WIS_1'][j])
            W1SOFrival.append(df['W1SOF_1'][j])
            BPrival.append(df['BP_1'][j])
            BPOFrival.append(df['BPOF_1'][j])
            TPWrival.append(df['TPW_1'][j])
            RPWrival.append(df['RPW_1'][j])
            RPWOFrival.append(df['RPWOF_1'][j])
            if cont==0:
                hasta.append(z+1)
                desde.append(z+1)
            else:
                desde.append(hasta[cont-1])
                hasta.append(j)
            cont=cont+1
    if cont==10:
        desde=np.array(desde)
        hasta=np.array(hasta)
        grid = np.zeros((10,10),dtype='float32')
        players = {'FS':weightaverage(desde,hasta,FSaux,grid),'FSOF': weightaverage(desde,hasta,FSOFaux,grid),
        'ACES': weightaverage(desde,hasta,ACESaux,grid),'DF': weightaverage(desde,hasta,DFaux,grid),
        'W1S':weightaverage(desde,hasta,W1Saux,grid),'W1SOF':weightaverage(desde,hasta,W1SOFaux,grid),
        'WIS':weightaverage(desde,hasta,WISaux,grid),'BP':weightaverage(desde,hasta,BPaux,grid),
        'BPOF':weightaverage(desde,hasta,BPOFaux,grid),'TPW':weightaverage(desde,hasta,TPWaux,grid),
        'RPW':weightaverage(desde,hasta,RPWaux,grid),'RPWOF':weightaverage(desde,hasta,RPWOFaux,grid),'ID_P':ID2[z],
        'FSRival':weightaverage(desde,hasta,FSrival,grid),'FSOFRival': weightaverage(desde,hasta,FSOFrival,grid),
        'ACESRival': weightaverage(desde,hasta,ACESrival,grid),'DFrival': weightaverage(desde,hasta,DFrival,grid),
        'W1SRival':weightaverage(desde,hasta,W1Srival,grid),'W1SOFRival':weightaverage(desde,hasta,W1SOFrival,grid),
        'WISRival':weightaverage(desde,hasta,WISrival,grid),'BPRival':weightaverage(desde,hasta,BPrival,grid),
        'BPOFRival':weightaverage(desde,hasta,BPOFrival,grid),'TPWRival':weightaverage(desde,hasta,TPWrival,grid),
        'RPWRival':weightaverage(desde,hasta,RPWrival,grid),'RPWOFRival':weightaverage(desde,hasta,RPWOFrival,grid),
        }
    else:
        players = {'FS':0,'FSOF': 0,'ACES': 0,'DF':0,'W1S':0,'W1SOF':0,'WIS':0,'BP':0,
        'BPOF':0,'TPW':0,'RPW':0,'RPWOF':0,'ID_P':ID2[z]}
    return players


players=Parallel(n_jobs=multiprocessing.cpu_count())(delayed(foo)(z) for z in range(len(ID1)))
df2 = pd.DataFrame.from_dict(players)
df2.to_csv('GordoHard.csv',index=False)
