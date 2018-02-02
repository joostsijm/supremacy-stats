
"""
Simple flask thing
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import Flask, render_template
from models.base import Game


APP = Flask(__name__)

ENGINE = create_engine("postgresql://supindex@localhost/supindex")
SESSION = sessionmaker(bind=ENGINE, autoflush=False)
SESSION = SESSION()

# to check database we will execute query
try:
    SESSION.execute('SELECT 1')
except Exception:
    print("Database not working")
    exit()


@APP.route('/game/')
@APP.route('/game/<game_id>')
def hello(game_id=None):
    """Return html"""
    game = SESSION.query(Game).filter(Game.game_id == game_id).first()
    return render_template('game.html', game=game)
