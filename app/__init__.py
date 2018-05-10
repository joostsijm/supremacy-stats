
"""
Website for Supremacy-stats
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from github_webhook import Webhook
from flask_migrate import Migrate
from flask_compress import Compress


app = Flask(__name__)

app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://supindex@localhost/supindex'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
# Cache files for 15 days
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1296000
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500
Compress(app)

db = SQLAlchemy(app)
webhook = Webhook(app)
migrate = Migrate(app, db)
