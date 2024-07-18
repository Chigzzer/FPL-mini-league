from flask import Flask, render_template, request, redirect
import static.data as data
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd 
import random
import static.fpl_functions as fpl
import requests as rq


numbers_chosen = []
lg_id = 16147
bingo_bank = open("static/bingo-bank.txt").read().splitlines()
api = 'https://fantasy.premierleague.com/api/bootstrap-static/#/'

# Creating application
app = Flask(__name__)
app.config['Debug'] = True

# Data for points tracking
dataB = rq.get(api)
database = dataB.json()
mainDF = pd.DataFrame(database['elements'])

# Sliming down the dataframe to the only values I require
slimMainDf = mainDF[['id', 'web_name', 'element_type', 'team', 'now_cost', 'total_points']]
slimMainDf.rename(columns={'element_type' : 'position', 'web_name' : 'name', 'now_cost' : 'price'}, inplace = True)

# Altering certain columns to more readable names
for i in range(len(slimMainDf['position'])):
    slimMainDf['position'][i] = fpl.position(slimMainDf['position'][i])

for j in range(len(slimMainDf['team'])):
    slimMainDf['team'][j] = fpl.findTeam(slimMainDf['team'][j], database)

# Converting cost to correct value
slimMainDf['price'] = slimMainDf.loc[:, ('price')]/10.0

#getting the current gameweek
gw = pd.DataFrame(database['events'])
gws = gw[['id', 'finished']]
for week, ids in gws.iterrows():
    if ids['finished'] != True:
        currentGw = ids['id']
        break
playerList, teams = fpl.getPlayerList(database)


def generate_graph(players_dic):
    col = ['black', 'lightcoral', 'red', 'sandybrown', 'tan', 'olive', 'yellow', 'olivedrab', 'lawngreen', 'green', 'mediumturquoise', 'cyan', 'steelblue', 'royalblue', 'deeppink'] # would need to change depending on number of users.
    col_index = 0
    plt.close()
    plt.margins(0)
    plt.xticks(range(0, len(players_dic[0]['running_points'])))
    plt.yticks(range(0, players_dic[0]['total_points']+50, 25))
    plt.xlabel('Gameweek')
    plt.ylabel('Total Points')
    for player in players_dic:
        if col_index >= len(col):
            col_index = 0
        points = player['running_points']
        plt.plot(points, label = player['name'], color = col[col_index])
        col_index += 1
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.savefig('static\plot.png', bbox_inches='tight')


def populate_page(id):
    global league_name
    global current_league_id
    #league_id = request.form.get('League ID')
    data_results = data.find_league_data(id) # player_dic, top_gws, top_gw_players, top_gw_points, months, league name Superana league 16147
    players_dic = data_results[0]
    top_gws = data_results[1]
    top_gw_players = data_results[2]
    top_gw_points = data_results[3]
    months = data_results[4]
    league_name = data_results[5]
    current_league_id = data_results[6]
    worst_gw_players = data_results[7]
    worst_gw_points = data_results[8]
    worst_gws = data_results[9]
    print(top_gw_players)
    generate_graph(players_dic)
    return render_template("index.html", current_league_id = current_league_id, top_gw_points = top_gw_points, top_gw_players = top_gw_players, top_gws = top_gws, months = months, players = players_dic, league_name = league_name, worst_gw_points = worst_gw_points, worst_gw_players = worst_gw_players, worst_gws = worst_gws)


def get_number(length):
    number = random.randint(0, length-1)
    while number in numbers_chosen:
        number = random.randint(0, length -1)
    numbers_chosen.append(number)
    return number


def generate_card(size):
    bingo_card_data = []
    numbers_chosen.clear()
    for i in range(size*size):
        index = get_number(len(bingo_bank))
        bingo_card_data.append(bingo_bank[index])
    print(bingo_card_data)
    return bingo_card_data


@app.route("/")
def index():
   print("Below:")
   print(lg_id)
   return populate_page(lg_id)


@app.route('/', methods=['POST'])
def index_league():
    global lg_id
    if not request.form.get('League ID'):
        return redirect('/')
    if int(request.form.get('League ID')) < 1:
        return redirect('/')
    lg_id = request.form.get('League ID')
    print(lg_id)
    return populate_page(lg_id)


@app.route("/bingo")
def bingo():
    size = 3
    bingo_data = generate_card(size)
    print('below is data')
    print(bingo_data)
    print(numbers_chosen)
    return render_template("bingo.html", bingo_data = bingo_data, size = size, league_name = league_name, current_league_id = current_league_id)


@app.route("/bingo", methods = ['POST'])
def bingo_size():
    if not request.form.get('bingo-size'):
        return redirect('/bingo')
    if int(request.form.get('bingo-size')) < 1:
        return redirect("/bingo") 
    if (int(request.form.get('bingo-size')) * int(request.form.get('bingo-size')))> len(bingo_bank):
        return redirect('/bingo')
    size = int(request.form.get('bingo-size'))
    bingo_data = generate_card(size)
    print('below is data')
    print(bingo_data)
    print(numbers_chosen)
    return render_template("bingo.html", bingo_data = bingo_data, size = size, league_name = league_name, current_league_id = current_league_id)


@app.route("/change-league")
def league_change():
    return render_template("change-league.html", league_name = league_name, current_league_id = current_league_id)


@app.route("/change-league", methods = ['POST'])
def league_change_post():
    global lg_id
    if not request.form.get('League ID'):
        return redirect('/')
    if int(request.form.get('League ID')) < 1:
        return redirect('/')
    lg_id = request.form.get('League ID')
    print(lg_id)
    return redirect('/')


@app.route("/points-track")
def ptrack():
    plt.close()
    playerId = 10
    gwPoints, totalPoints = fpl.playerWeekPoints(playerId)
    x_axis = [x for x in range(1, len(totalPoints) + 1)]
    totalPoints = [0] * len(gwPoints)
    plt.bar(x_axis, totalPoints)
    plt.ylabel("Total Points")
    plt.xlabel("Gameweek")
    print(totalPoints)
    plt.savefig('/static/points_plot.jpg')
    return render_template("points-track.html", playerList = playerList, teams = teams, league_name = league_name, current_league_id = current_league_id)


@app.route('/points-track', methods=['POST'])
def homeGraph():
    #Obtain user's inputted player
    if not request.form.get('players'):
        return redirect('/')
    playerName = request.form.get('players')
    playerId = fpl.findPlayerId(database, playerName)
    gwPoints, totalPoints = fpl.playerWeekPoints(playerId)
    x_axis = [x for x in range(1, len(totalPoints) + 1)]
    plt.bar(x_axis, gwPoints, width=0.2, label=playerName)
    plt.ylabel("Total Points")
    plt.xlabel("Gameweek")
    plt.legend()
    if request.form.get("addOn") != None:
        plt.plot(x_axis, totalPoints, label=playerName)
        plt.legend()
    plt.savefig('static/points_plot.jpg')    
    return render_template("points-track.html", playerList = playerList, teams = teams, league_name = league_name, current_league_id = current_league_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
