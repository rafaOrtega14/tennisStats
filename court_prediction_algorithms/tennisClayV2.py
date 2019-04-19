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

TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXX"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
page = requests.get("http://sports.williamhill.es/bet_esp/es/betting/y/17/mh/Tenis.html")
soup = BeautifulSoup(page.content, 'html.parser')
df=pd.read_csv("GordoClay.csv")
elo=pd.read_csv("eloCourtV81.csv")
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
    stats={'FS':df['FS'][pos],'FSOF':df['FSOF'][pos],'ACES':df['ACES'][pos],'DF':df['DF'][pos],
    'W1S':df['W1S'][pos],'W1SOF':df['W1SOF'][pos],'WIS':df['WIS'][pos],'BP':df['BP'][pos],'BPOF':df['BPOF'][pos],
    'TPW':df['TPW'][pos],'RPW':df['RPW'][pos],'RPWOF':df['RPWOF'][pos],'FSRival':df['FSRival'][pos],'FSOFRival':df['FSOFRival'][pos],
    'ACESRival':df['ACESRival'][pos],'DFRival':df['DFrival'][pos],'W1SRival':df['W1SRival'][pos],'W1SOFRival':df['W1SOFRival'][pos],'WISRival':df['WISRival'][pos],
    'BPRival':df['BPRival'][pos],'BPOFRival':df['BPOFRival'][pos],'TPWRival':df['TPWRival'][pos],'RPWRival':df['RPWRival'][pos],'RPWOFRival':df['RPWOFRival'][pos],
    'ID_P':df['ID_P'][pos]}
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
    for i in range(len(elo['clay'])):
        if ID1==elo['ID_player'][i]:
            elop1=elo['clay'][i]
        
        if ID2==elo['ID_player'][i]:
            elop2=elo['clay'][i]
    return {'elop1':elop1,'elop2':elop2}

def stack_proba(Proba_win):
    proba=Proba_win*100
    return round((9*((proba - 65)/35)+1),1)
def getprediction(datax,datay,player1,player2):
    prediction=""
    Player1_rank=getPlayerRank(player1)
    Player2_rank=getPlayerRank(player2)
    elos=getElo(datax["ID_P"],datay["ID_P"])
    model = pickle.load(open('RangerRed_V2.sav', 'rb'))
    players = [{'ACESRival_1':datax['ACESRival'],'ACESRival_2':datay['ACESRival'],'BPOFRival_1':datax['BPOFRival'],'BPOFRival_2':datay['BPOFRival'],
    'BPRival_1':datax['BPRival'],'BPRival_2':datay['BPRival'],'DFRival_1':datax['DFRival'],'DFRival_2':datay['DFRival'],'FSOFRival_1':datax['FSOFRival'],
    'FSOFRival_2':datay['FSOFRival'],'FSRival_1':datax['FSRival'],'FSRival_2':datay['FSRival'],'RPWOFRival_1':datax['RPWOFRival'],'RPWOFRival_2':datay['RPWOFRival'],
    'RPWRival_1':datax['RPWRival'],'RPWRival_2':datay['RPWRival'],'TPWRival_1':datax['TPWRival'],'TPWRival_2':datay['TPWRival'],'W1SOFRival_1':datax['W1SOFRival'],
    'W1SOFRival_2':datay['W1SOFRival'],'W1SRival_1':datax['W1SRival'],'W1SRival_2':datay['W1SRival'],'WISRival_1':datax['WISRival'],'WISRival_2':datay['WISRival'],
    'ACES_1':datax['ACES'],'ACES_2':datay['ACES'],'BPOF_1':datax['BPOF'],'BPOF_2':datay['BPOF'],'BP_1':datax['BP'],'BP_2':datay['BP'],'DF_1':datax['DF'],
    'DF_2':datay['DF'],'FSOF_1':datax['FSOF'],'FSOF_2':datay['FSOF'],'FS_1':datax['FS'],'FS_2':datay['FS'],'RPWOF_1':datax['RPWOF'],'RPWOF_2':datay['RPWOF'],
    'RPW_1':datax['RPW'],'RPW_2':datay['RPW'],'TPW_1':datax['TPW'],'TPW_2':datay['TPW'],'W1SOF_1':datax['W1SOF'],'W1SOF_2':datay['W1SOF'],'W1S_1':datax['W1S'],
    'W1S_2':datay['W1S'],'WIS_1':datax['WIS'],'WIS_2':datay['WIS'],'eloLoser':elos['elop2'],'eloWinner':elos['elop1']}]
    data = pd.DataFrame.from_dict(players)
    data.to_csv('prueba_Rafi.csv')
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
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=html".format("--------INICIO DE LA PREDICCION--------",'-1001225248748')
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
            print(message)
            #url = URL + "sendMessage?text={}&chat_id={}&parse_mode=html".format(message,'-1001225248748')
            #get_url(url)
    


def main():
    getStatsAndRun()
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=html".format("--------FIN DE LA PREDICCION--------",'-1001225248748')
    get_url(url)


if __name__ == '__main__':
    main()