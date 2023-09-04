from flask import Flask, render_template, request, redirect, flash
import data
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

#Creating application
app = Flask(__name__)
app.config['Debug'] = True


@app.route("/")
def index():

    col = ['black', 'lightcoral', 'red', 'sandybrown', 'tan', 'olive', 'yellow', 'olivedrab', 'lawngreen', 'green', 'mediumturquoise', 'cyan', 'steelblue', 'royalblue', 'deeppink']
    col_index = 0
    plt.close()
    plt.margins(0)
    plt.xticks(range(0, len(data.players_dic[0]['running_points'])))
    plt.yticks(range(0, data.players_dic[0]['total_points']+50, 25))
    plt.xlabel('Gameweek')
    plt.ylabel('Total Points')
    for player in data.players_dic:
        if col_index >= len(col):
            col_index = 0
        points = player['running_points']
        plt.plot(points, label = player['name'], color = col[col_index])
        col_index += 1

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.savefig('static/plot.png', bbox_inches='tight')

    return render_template("index.html", top_gw_points = data.top_gw_points, top_gw_players = data.top_gw_players, top_gws = data.top_gws, months = data.months, players = data.players_dic)

"""@app.route("/race")
def race():
    col = ['black', 'lightcoral', 'red', 'sandybrown', 'tan', 'olive', 'yellow', 'olivedrab', 'lawngreen', 'green', 'mediumturquoise', 'cyan', 'steelblue', 'royalblue', 'deeppink']
    col_index = 0
    plt.close()
    plt.margins(0)
    plt.xticks(range(0, len(data.players_dic[0]['running_points'])))
    plt.yticks(range(0, data.players_dic[0]['total_points']+50, 25))
    plt.xlabel('Gameweek')
    plt.ylabel('Total Points')
    for player in data.players_dic:
        print(col_index)
        print(col[col_index])
        if col_index >= len(col):
            col_index = 0
        points = player['running_points']
        plt.plot(points, label = player['name'], color = col[col_index])
        col_index += 1

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    plt.savefig('static/plot.png', bbox_inches='tight')
    return render_template("race.html", players = data.players_dic)"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
