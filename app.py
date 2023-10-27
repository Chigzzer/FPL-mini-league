from flask import Flask, render_template, request, redirect, flash
import data
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import random
import os

numbers_chosen = []
print(os.getcwd())
bingo_bank = open("static/bingo-bank.txt").read().splitlines()

#Creating application
app = Flask(__name__)
app.config['Debug'] = True

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
    #league_id = request.form.get('League ID')
    data_results = data.find_league_data(id) # player_dic, top_gws, top_gw_players, top_gw_points, months, league name Superana league 5154
    players_dic = data_results[0]
    top_gws = data_results[1]
    top_gw_players = data_results[2]
    top_gw_points = data_results[3]
    months = data_results[4]
    league_name = data_results[5]
    current_league_id = data_results[6]

    print(top_gw_players)
    generate_graph(players_dic)
    return render_template("index.html", current_league_id = current_league_id, top_gw_points = top_gw_points, top_gw_players = top_gw_players, top_gws = top_gws, months = months, players = players_dic, league_name = league_name)

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
def index(l_id = 5154):
   return populate_page(l_id)


@app.route('/', methods=['POST'])
def index_league():
    if not request.form.get('League ID'):
        return redirect('/')
    if int(request.form.get('League ID')) < 1:
        return redirect('/')
    league_id = request.form.get('League ID')
    return populate_page(league_id)


@app.route("/bingo")
def bingo():
    size = 3;
    bingo_data = generate_card(size)
    print('below is data')
    print(bingo_data)
    print(numbers_chosen)
    return render_template("bingo.html", bingo_data = bingo_data, size = size)

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
    return render_template("bingo.html", bingo_data = bingo_data, size = size)






if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
