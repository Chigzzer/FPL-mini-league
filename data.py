import requests
import pandas as pd

# Setting values
league_id =  5154
top_gw_points = 0
months = []
top_gws = []
top_gw_players = []
players_dic = []
current_gw = 0


# API Link
league_api = 'https://fantasy.premierleague.com/api/leagues-classic/' + str(league_id) + '/standings'
general_api = 'https://fantasy.premierleague.com/api/bootstrap-static/'


# Obtaining league data
league_data = requests.get(league_api)
json_league = league_data.json()['standings']['results']
general_data = requests.get(general_api).json()
month_data = general_data['phases']

# Organising gameweek to months
for event in month_data:
    if event['id'] == 1:
        continue
    months.append({'month_name':event['name'], 'gw_start':event['start_event'], 'gw_end':event['stop_event']})

print(months)
# Obtaining all the player's and their ids of each player in the league
for item in json_league:
    player_dic = {'name': item['player_name'], 'player_id': item['entry']}
    players_dic.append(player_dic)
    
# Looping through each player in league to get their data 
for player in players_dic:
    player_points = []
    team_api = 'https://fantasy.premierleague.com/api/entry/' + str(player['player_id']) + '/history/'
    player_data = requests.get(team_api)
    player_data_json = player_data.json()
    player_current_data = player_data_json['current']
    current_gw = len(player_current_data)
    player_chip_used = player_data_json['chips']
    # Looping through each of the player's gameweek
    for week in player_current_data:
        player_points.append(week['points']) # Adding that gameweek points to that player's points list
        # adding points to relevent month
        gw = week['event']
        for month in months:
            if gw <= month['gw_end'] and gw >= month['gw_start']:
                if month['month_name'] not in player.keys():
                    player[month['month_name']] = 0 
                player[month['month_name']] += week['points']
        # Comparing that gw points with the current maximum
        if week['points'] == top_gw_points: # if points value is identical to the current highest, append the winner to the list
            top_gw_players.append(player['name'])
            top_gws.append(week['event'])
        elif week['points'] > top_gw_points: # if the total points is higher than the value, remove the current winners and update the list
            top_gw_points = week['points']
            top_gws.clear()
            top_gw_players.clear()
            top_gw_players.append(player['name'])
            top_gws.append(week['event'])
    player["points"] = player_points # Adding player's points list to their dictionary

    # looking through the players chips to check if they have been used and what gameweek
    if player_chip_used:
        chips_used = {}
        print(player_chip_used)
        for chips in player_chip_used:
            if chips['name'] == 'bboost':
                chips_used["bench_boost"] = chips['event']
            elif chips['name'] == 'freehit':
                chips_used["free_hit"] = chips['event']
            elif chips['name'] == 'wildcard':
                chips_used["wildcard1"] = chips['event']
            elif chips['name'] == 'wcard2': # Need to confirm name after january
                chips_used["wildcard2"] = chips['event']
            elif chips['name'] == '3xc':
                chips_used["triple_captain"] = chips['event']
        player['chips'] = chips_used


#Checking who is the highest scoring in the month
for month in months:
    for player in players_dic:
        if month['month_name'] not in player.keys():
            continue 
        if 'top_scorer' not in month.keys():
            month['top_scorer'] = []
            month['top_points'] = 0
        if player[month['month_name']] >=  month['top_points']:
            month['top_scorer'].clear()
            month['top_points'] = player[month['month_name']]
            month['top_scorer'].append(player['name'])


# Printing out the current top scorer of the league


print('The top gameweek scored: ' + str(top_gw_points))
print('The following players scored the maximum points at each of the following gameweeks')
for winner in range(len(top_gws)):
    print(str(top_gw_players[winner]) + ': ' + str(top_gws[winner]))


print('The top scorers for each month are below:')
for month in months:
    if 'top_scorer' not in month.keys():
        continue
    print(month['month_name'] + 'Top Scorers who scored: ' + str(month['top_points']) + ' are:')
    for player in month['top_scorer']:
        print(player)