
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


@app.route('/api/game/<game_id>')
def api_game(game_id):
    """Return results for game statics"""

    try:
        game_id = int(game_id)
    except ValueError:
        game_id = None

    game = Game.query.filter(Game.game_id == game_id).first()
    return jsonify(game)
