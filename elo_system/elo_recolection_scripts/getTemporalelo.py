import pandas as pd
import numpy as np
import multiprocessing

pd.options.mode.chained_assignment = None

games=pd.read_csv("TrainsetGrass.csv",low_memory=False)
players=pd.read_csv("eloCourt.csv",low_memory=False)

def find_eloplayer(ID):
    hard=[]
    clay=[]
    grass=[]
    pos=934959345
    for j in range(len(players['ID_player'])):
        if ID==players['ID_player'][j]:
            eloh=players['hard'][j]
            eloc=players['clay'][j]
            elog=players['grass'][j]
            pos=j
            break
    if pos==934959345:
        hard=1500
        clay=1500
        grass=1500
        pos=addPlayer(ID)
    else:
        hard=eloh
        clay=eloc
        grass=elog
    master={
        'hard': hard,
        'clay': clay,
        'grass': grass,
        'pos': pos
    }
    return master

def addPlayer(ID):
    players.loc[-1]=[ID+5,ID,1500,1500,1500,1500]
    players.index = players.index + 1
    return len(players['ID_player'])
def expected(A, B):
    return 1 / (1 + 10 ** ((B - A) / 400))
 
def elo(old, exp, score, k=32):
    return old + k * (score - exp)

if __name__ == "__main__":
    for z in range(len(games['ID1'])):
        print(str(z)+" de : "+str(len(games['ID1'])))
        elo_actualwin=find_eloplayer(games['ID1'][z])
        elo_actuallose=find_eloplayer(games['ID2'][z])
        posicionwin=elo_actualwin['pos']
        posicionloser=elo_actuallose['pos']
        if games['COURT'][z]=='Hard' or games['COURT'][z]=='I.hard':
            hardwin=elo(elo_actualwin['hard'],expected(elo_actualwin['hard'],elo_actuallose['hard']), 1, k=32)
            hardlose=elo(elo_actuallose['hard'],expected(elo_actuallose['hard'],elo_actualwin['hard']),0, k=32)
            players.ix[posicionwin,'hard']=hardwin
            players.ix[posicionloser,'hard']=hardlose
            games.ix[z,'eloWinner']=hardwin
            games.ix[z,'eloLoser']=hardlose
        if games['COURT'][z]=='Clay':
            claywin=elo(elo_actualwin['clay'],expected(elo_actualwin['clay'],elo_actuallose['clay']), 1, k=32)
            claylose=elo(elo_actuallose['clay'],expected(elo_actuallose['clay'],elo_actualwin['clay']),0, k=32)
            players.ix[posicionwin,'clay']=claywin
            players.ix[posicionloser,'clay']=claylose
            games.ix[z,'eloWinner']=claywin
            games.ix[z,'eloLoser']=claylose
        if games['COURT'][z]=='Grass':
            grasswin=elo(float(elo_actualwin['grass']),expected(float(elo_actualwin['grass']),float(elo_actuallose['grass'])), 1, k=64)
            grasslose=elo(float(elo_actuallose['grass']),expected(float(elo_actuallose['grass']),float(elo_actualwin['grass'])),0, k=64)
            players.ix[posicionwin,'grass']=grasswin
            players.ix[posicionloser,'grass']=grasslose
            games.ix[z,'eloWinner']=grasswin
            games.ix[z,'eloLoser']=grasslose
    games.to_csv('TrainsetGrassV2.csv',index=False)