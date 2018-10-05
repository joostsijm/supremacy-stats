
"""
Website for Supremacy-stats
"""

from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from github_webhook import Webhook
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_compress import Compress
from flask_argon2 import Argon2
from flask_apscheduler import APScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


DATABASE_URI = 'postgresql://supindex@localhost/supindex'

class Config(object):
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url=DATABASE_URI)
    }
    SCHEDULER_API_ENABLED = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SECRET_KEY = 'g6DGM5y2bVhb0mxdCRELI5m7fnzzoJ2y'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEND_FILE_MAX_AGE_DEFAULT = 1296000


app = Flask(__name__)
app.config.from_object(Config())
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

# Compress settings
COMPRESS_MIMETYPES = [
    'text/html',
    'text/css',
    'text/xml',
    'application/json',
    'application/javascript'
]
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500
Compress(app)

db = SQLAlchemy(app)
webhook = Webhook(app)
migrate = Migrate(app, db)
argon2 = Argon2(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"
