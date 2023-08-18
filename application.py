import requests
import pandas as pd

# Setting values
league_id =  5154
top_gw_points = 0
top_gws = []
top_gw_players = []
players = []
players_ids = []

# API Link
league_api = 'https://fantasy.premierleague.com/api/leagues-classic/' + str(league_id) + '/standings'


# Obtaining league data
league_data = requests.get(league_api)
json_league = league_data.json()['standings']['results']

# Obtaining all the player's and their ids of each player in the league
for item in json_league:
    players.append(item['player_name'])
    players_ids.append(item['entry'])
    
# Looping through multiple playrs to look at each player     
for i in range(len(players_ids)):
    team_api = 'https://fantasy.premierleague.com/api/entry/' + str(players_ids[i]) + '/history/'
    player_data = requests.get(team_api)
    player_data_json = player_data.json()['current']
    
    # Looping through each of the player's gameweek
    for week in player_data_json:
        # Comparing that gw points with the current maximum
        if week['points'] == top_gw_points: # if points value is identical to the current highest, append the winner to the list
            top_gw_players.append(players[i])
            top_gws.append(week['event'])

        elif week['points'] > top_gw_points: # if the total points is higher than the value, remove the current winners and update the list
            top_gw_points = week['points']
            top_gws.clear()
            top_gw_players.clear()
            top_gw_players.append(players[i])
            top_gws.append(week['event'])


print('The top gameweek scored: ' + str(top_gw_points))
print('The following players scored the maximum points at each of the following gameweeks')
for winner in range(len(top_gws)):
    print(str(top_gw_players[winner]) + ': ' + str(top_gws[winner]))
