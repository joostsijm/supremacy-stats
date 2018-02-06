
"""
Simple flask thing
"""

from flask import render_template, jsonify
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb
from flask_menu import Menu, register_menu
from app import app
from app.models.game import Game

Menu(app=app)
Breadcrumbs(app=app)


@app.route('/')
@register_breadcrumb(app, '.', 'Home')
@register_menu(app, '.', 'Home')
def index():
    """Show homepage"""

    games = Game.query.all()
    return render_template('site/index.html', games=games)


@app.route('/games')
@register_menu(app, 'games', 'Games')
@register_breadcrumb(app, 'games', 'Games')
def game_index():
    """Return game index"""

    games = Game.query.all()
    return render_template('game/index.html', games=games)


@app.route('/game/<game_id>')
#@register_breadcrumb(app, 'game.id', '', dynamic_list_constructor=game_index)
def game_overview(game_id):
    """Show game overview"""

    try:
        game_id = int(game_id)
    except ValueError:
        game_id = None

    game = Game.query.filter(Game.game_id == game_id).first()
    return render_template('game/overview.html', game=game)


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
