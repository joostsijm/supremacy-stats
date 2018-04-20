
"""
Website for Supremacy-stats
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from github_webhook import Webhook


app = Flask(__name__)

app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://supindex@localhost/supindex'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

db = SQLAlchemy(app)
webhook = Webhook(app)