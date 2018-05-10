
"""
Website for Supremacy-stats
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from github_webhook import Webhook
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://supindex@localhost/supindex'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config.update(SECRET_KEY='iliasmitchelrobintimjoost')

db = SQLAlchemy(app)
webhook = Webhook(app)
migrate = Migrate(app, db)

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"