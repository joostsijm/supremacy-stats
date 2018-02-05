
"""
Simple flask thing
"""

from flask import render_template, jsonify
from app import app
from app.models.game import Game


@app.route('/')
def index():
    """Show homepage"""
    return render_template('index.html', Game=Game)


@app.route('/game/<game_id>')
def game(game_id=None):
    """Return index"""

    if game_id is not None:
        try:
            game_id = int(game_id)
        except ValueError:
            game_id = None

    game = Game.query.filter(Game.game_id == game_id).first()
    return render_template('game.html', game=game)


@app.route('/api/game/<game_id>/score')
def api_game_score(game_id):
    """Returns list days with players"""

    try:
        game_id = int(game_id)
    except ValueError:
        game_id = None

    game = Game.query.filter(Game.game_id == game_id).first()

    day_dict = {}

    for day in game.days:
        if day.day not in day_dict:
            day_dict[day.day] = {}
            day_dict[day.day]["day"] = day.day

        day_dict[day.day][day.player.name] = day.points

    day_list = []

    for day in day_dict:
        day_list.append(day_dict[day])

    return jsonify(day_list)
