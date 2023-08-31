from flask import Flask, render_template, request, redirect, flash
import data


#Creating application
app = Flask(__name__)
app.config['Debug'] = True


@app.route("/")
def index():
    return render_template("index.html", top_gw_points = data.top_gw_points, top_gw_players = data.top_gw_players, top_gws = data.top_gws, months = data.months, players = data.players_dic)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
