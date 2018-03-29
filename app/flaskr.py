
"""
Simple flask thing
"""

from flask import render_template, jsonify, request, redirect
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb
from flask_menu import Menu, register_menu
from app import app
from app.models.game import Game
from app.models.user import User
from app.models.player import Player
import fetch

Menu(app=app)
Breadcrumbs(app=app)


@app.route('/')
@register_menu(app, '.', 'Home')
@register_breadcrumb(app, '.', 'Home')
def index():
    """Show homepage"""

    games = Game.query.count()
    users = User.query.count()
    return render_template('site/index.html', games=games, users=users)


@app.route('/games')
@register_menu(app, 'games', 'Games')
@register_breadcrumb(app, '.games', 'Games')
def game_index():
    """Return game index"""

    games = Game.query.all()
    return render_template('game/index.html', games=games)


def game_overview_dlc(*args, **kwargs):
    """Generate dynamic_list for games"""
    game_id = request.view_args['game_id']
    game = Game.query.filter(Game.game_id == game_id).first()
    return [{'text': game.game_id, 'url': game.url}]


@app.route('/game/<int:game_id>')
@register_breadcrumb(app, '.games.game_id', '',
                     dynamic_list_constructor=game_overview_dlc)
def game_overview(game_id):
    """Show game overview"""

    game_id = int(game_id)
    game = Game.query.filter(Game.game_id == game_id).first()
    return render_template('game/overview.html', game=game)


@app.route('/api/game/<int:game_id>/score/<string:type>')
def api_game_score(game_id, type):
    """Returns list days with players"""

    game_id = int(game_id)
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

    player_list = []

    if type == "players":
        players = game.players.filter(Player.user_id != None).all()
    else:
        players = game.players

    for player in players:
        player_list.append({
            "title": player.nation_name,
            "valueField": player.name,
        })

    score = {
        "days": day_list,
        "players": player_list,
    }

    return jsonify(score)


@app.route('/api/game/fetch', methods=['POST'])
def api_fetch_game():
    """Update game in the database"""

    game_id = request.form.get('game_id')
    game = fetch.get_results(game_id)

    return redirect(game.url, code=302)


@app.route('/api/game/fetch', methods=['POST'])
def api_fetch_game_players():
    """Update game in the database"""

    game_id = request.form.get('game_id')
    game = fetch.get_players(game_id)

    return redirect(game.url, code=302)


@app.route('/users')
@register_menu(app, 'users', 'Users')
@register_breadcrumb(app, '.users', 'Users')
def user_index():
    """Return user index"""

    users = User.query.all()
    return render_template('user/index.html', users=users)


def user_overview_dlc(*args, **kwargs):
    """Generate dynamic_list for user"""
    site_id = request.view_args['site_id']
    user = User.query.filter(User.site_id == site_id).first()
    return [{'text': user.name, 'url': user.url}]


@app.route('/user/<int:site_id>')
@register_breadcrumb(app, '.users.site_id', '',
                     dynamic_list_constructor=user_overview_dlc)
def user_overview(site_id):
    """Show user overview"""

    site_id = int(site_id)
    user = User.query.filter(User.site_id == site_id).first()
    return render_template('user/overview.html', user=user)
