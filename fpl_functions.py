import requests as rq
import pandas as pd

def findPlayerCode(database, name):
    for i in database['elements']:
        if i['web_name'] == name:
            code = i['code']
    return code

def findPlayerId(database, name):
    for i in database['elements']:
        if i['web_name'] == name:
            return i['id']
    return 0


def findPlayerName(database, code):
    for i in database['elements']:
        print(code)
        if i['code'] == code:
            name= i['web_name']
    return name


def position(number):
    if number == 1:
        pos = "GK"
    elif number == 2:
        pos = "DEF"
    elif number == 3:
        pos = "MID"
    else:
        pos = "FWD"
    return pos

def findTeam(code, database):
    for i in database['teams']:
        if i['id'] ==  code:
            name = i['name']
            return str(name)

# Obtain points
def playerWeekPoints(playerId):
   
    pointsApi = 'https://fantasy.premierleague.com/api/element-summary/' + str(playerId) + '/'
    pointsData = rq.get(pointsApi)
    pointsDb = pointsData.json()
    pointsDf = pd.DataFrame(pointsDb['history'])
    pointsDfPoints = pointsDf['total_points'] #gets player id
    playerGwPoints=[]
    playerTotalPoints = []
    for point in pointsDfPoints:
        playerGwPoints.append(point)
    for i in range(len(playerGwPoints)):
        if i == 0:
            playerTotalPoints.append(playerGwPoints[i])
        else:
            playerTotalPoints.append(playerGwPoints[i] + playerTotalPoints[i-1])

    return playerGwPoints, playerTotalPoints


def getPlayerList(db):
    playerList = []
    teams = []
    for player in db['elements']:
        team = findTeam(player['team'], db)
        if team not in teams:
            teams.append(team)
        pl = [player['web_name'], team]
        playerList.append(pl)
    return playerList, teams

def getTeamPlayers(teamDatabase, db):
    playerList = []
    for player in teamDatabase['picks']:
        playerID = player['element']
        for i in db['elements']:
            if i['id'] == playerID:
                playerList.append(i['web_name'])
    return playerList

    
