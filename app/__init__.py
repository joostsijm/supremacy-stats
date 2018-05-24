
"""
Website for Supremacy-stats
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from github_webhook import Webhook
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_compress import Compress
from flask_argon2 import Argon2


app = Flask(__name__)

app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config.update(
    TESTING=True,
    SQLALCHEMY_DATABASE_URI='postgresql://supindex@localhost/supindex',
    SECRET_KEY='g6DGM5y2bVhb0mxdCRELI5m7fnzzoJ2y',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SEND_FILE_MAX_AGE_DEFAULT=1296000,
)
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500
Compress(app)

db = SQLAlchemy(app)
webhook = Webhook(app)
migrate = Migrate(app, db)
argon2 = Argon2(app)

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"
