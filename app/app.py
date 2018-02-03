
"""
Simple flask thing
"""

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template


app = Flask(__name__)
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://supindex@localhost/supindex'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

db = SQLAlchemy(app)

from app.models import base

"""
@app.route('/game/')
@app.route('/game/<game_id>')
def hello(game_id=None):
    game = Game.query(Game).filter(Game.game_id == game_id).first()
    return render_template('game.html', game=game)
"""
