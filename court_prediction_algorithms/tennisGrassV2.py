from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
from difflib import SequenceMatcher
import pickle
import unidecode
from sklearn import model_selection
from sklearn.preprocessing import PolynomialFeatures

TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXX
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
page = requests.get("http://sports.williamhill.es/bet_esp/es/betting/y/17/mh/Tenis.html")
soup = BeautifulSoup(page.content, 'html.parser')
df=pd.read_csv("GordoGrass.csv")
elo=pd.read_csv("eloCourtV69.csv")
rank=pd.read_csv("ranks.csv")
def getPlayers():
    divTag = soup.find_all(class_="CentrePad")
    players=[]
    for tag in divTag:
        tags = tag.find_all('span')
        for idx,tag in enumerate(tags):
            players.append(tag.text.replace(u'\xa0', u' '))
    return players
def getPlayerRank(player):
    rank=1001
    rankpage = requests.get("https://live-tennis.eu/es/clasificacion-atp-en-vivo")
    ranksoup = BeautifulSoup(rankpage.content, 'html.parser')
    ranks = ranksoup.findAll("td", {'width':20,'height':30})
    players = ranksoup.findAll("td", {'width':150})
    for idx,playername in enumerate(players):
        if similar(unidecode.unidecode(playername.text),player)>0.75:
            rank=ranks[idx].text
    return rank
def weigthaverage(rank_proba,model_proba):
    return round(((rank_proba*1)+(model_proba*1))/2,3)
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content
def getPlayerStats(pos):
    stats=[]
    stats.append(df['FS'][pos])
    stats.append(df['FSOF'][pos])
    stats.append(df['ACES'][pos])
    stats.append(df['DF'][pos])
    stats.append(df['W1S'][pos])
    stats.append(df['W1SOF'][pos])
    stats.append(df['WIS'][pos])
    stats.append(df['BP'][pos])
    stats.append(df['BPOF'][pos])
    stats.append(df['TPW'][pos])
    stats.append(df['RPW'][pos])
    stats.append(df['RPWOF'][pos])
    stats.append(df['ID_P'][pos])
    return stats
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
def getposicionPlayer(player):
    playerpos=-1
    for i in range(len(df['NAME_P'])):
        if similar(df['NAME_P'][i],player)>0.75:
            playerpos=i
    return playerpos
def getratio(A,B):
    return A/(A+B)
def rankclassifier(player1,player2):
    rankp1=0
    rankp2=0
    result=0
    Player1_rank=int(getPlayerRank(player1))
    Player2_rank=int(getPlayerRank(player2))
    for i in range(len(rank['puntos'])):
        if Player1_rank==rank['rank'][i]:
            rankp1=rank['puntos'][i]
        
        if Player2_rank==rank['rank'][i]:
            rankp2=rank['puntos'][i]
    
    return getratio(rankp1,rankp2)
def getElo(ID1,ID2):
    elop1=0
    elop2=0
    for i in range(len(elo['grass'])):
        if ID1==elo['ID_player'][i]:
            elop1=elo['grass'][i]
        
        if ID2==elo['ID_player'][i]:
            elop2=elo['grass'][i]
    return {'elop1':elop1,'elop2':elop2}

def stack_proba(Proba_win):
    proba=Proba_win*100
    return round((9*((proba - 65)/35)+1),1)
def getprediction(datax,datay,player1,player2):
    prediction=""
    Player1_rank=getPlayerRank(player1)
    Player2_rank=getPlayerRank(player2)
    elos=getElo(datax[12],datay[12])
    model = pickle.load(open('Octopus_Grass_2.sav', 'rb'))
    players = [{'ACES_1':datax[2],'ACES_2':datay[2],'BPOF_1':datax[8],'BPOF_2':datay[8],'BP_1':datax[7],
    'BP_2':datay[7],'DF_1':datax[3],'DF_2':datay[3],'FSOF_1':datax[1],'FSOF_2':datay[1],'FS_1':datax[0],
    'FS_2':datay[0],'RPWOF_1':datax[11],'RPWOF_2':datay[11],'RPW_1':datax[10],'RPW_2':datay[10],
    'TPW_1':datax[9],'TPW_2':datay[9],'W1SOF_1':datax[5],'W1SOF_2':datay[5],'W1S_1':datax[4],'W1S_2':datay[4],
    'WIS_1':datax[6],'WIS_2':datay[6],'eloLoser':elos['elop2'],'eloWinner':elos['elop1']}]
    data = pd.DataFrame.from_dict(players)
    poly = PolynomialFeatures(degree = 2, interaction_only = True, include_bias=True)
    p = poly.fit_transform(data)
    proba=model.predict_proba(p)
    if proba[0][1]>0.5:
        prediction='<b>'+'Probability: '+str(proba[0][1]*100)+'/100'+' W'+str(Player1_rank)+" "+player1+'</b>'+" - "+str(Player2_rank)+" "+player2+' L'+"\n"
    else:
        prediction='<b>'+'Probability: '+str((1-proba[0][1])*100)+'/100'+"</b> "+str(Player1_rank)+" "+player1+' L'+' - '+'<b>'+'W '+str(Player2_rank)+" "+player2+'</b>'+"\n"
    return prediction
def getStatsAndRun():
    players=getPlayers()
    message=""
    elomessage=""
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=html".format("--------INICIO DE LA PREDICCION--------",'-1001126223985')
    get_url(url)
    for j in players:
        player1=""
        player2=""
        player1=j.split('-')[0]
        player2=j.split('-')[1]
        pos1=getposicionPlayer(player1)
        pos2=getposicionPlayer(player2)
        if (pos1>-1 and pos2>-1):
            message=getprediction(getPlayerStats(pos1),getPlayerStats(pos2),player1,player2)
            url = URL + "sendMessage?text={}&chat_id={}&parse_mode=html".format(message,'-1001126223985')
            get_url(url)
    


def main():
    getStatsAndRun()
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=html".format("--------FIN DE LA PREDICCION--------",'-1001126223985')
    get_url(url)


if __name__ == '__main__':
    main()
