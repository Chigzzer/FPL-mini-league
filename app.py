from flask import Flask, render_template, request, redirect, flash
import data
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

#Creating application
app = Flask(__name__)
app.config['Debug'] = True


def generate_graph(players_dic):
    col = ['black', 'lightcoral', 'red', 'sandybrown', 'tan', 'olive', 'yellow', 'olivedrab', 'lawngreen', 'green', 'mediumturquoise', 'cyan', 'steelblue', 'royalblue', 'deeppink']
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
    plt.savefig('static/plot.png', bbox_inches='tight')


@app.route("/")
def index(l_id = 5154):
    data_results = data.find_league_data(l_id) # player_dic, top_gws, top_gw_players, top_gw_points, months, league name Superana league 5154
    players_dic = data_results[0]
    top_gws = data_results[1]
    top_gw_players = data_results[2]
    top_gw_points = data_results[3]
    months = data_results[4]
    league_name = data_results[5]

    generate_graph(players_dic)

    return render_template("index.html", top_gw_points = top_gw_points, top_gw_players = top_gw_players, top_gws = top_gws, months = months, players = players_dic, league_name = league_name)

@app.route('/', methods=['POST'])
def index_league():
    if not request.form.get('League ID'):
        print('worked')
        return redirect('/')
    league_id = request.form.get('League ID')
    data_results = data.find_league_data(league_id) # player_dic, top_gws, top_gw_players, top_gw_points, months, league name Superana league 5154
    players_dic = data_results[0]
    top_gws = data_results[1]
    top_gw_players = data_results[2]
    top_gw_points = data_results[3]
    months = data_results[4]
    league_name = data_results[5]

    generate_graph(players_dic)

    return render_template("index.html", top_gw_points = top_gw_points, top_gw_players = top_gw_players, top_gws = top_gws, months = months, players = players_dic, league_name = league_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
