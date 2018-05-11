
"""
User model module
"""

from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from flask import url_for
from app import db
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user


class User(db.Model, UserMixin):
    # Table name
    __tablename__ = 'sp_users'

    #
    # db.Columns
    # -------------

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    site_id = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    registration_at = db.Column(db.DateTime, default=datetime.utcnow)
    score_military = db.Column(db.Integer)
    score_economic = db.Column(db.Integer)

    #
    # Relationships
    # -------------

    players = db.relationship("Player", back_populates="user", lazy="dynamic")

    #
    # Attributes
    # -------------

    def __init__(self, id=None):
        self.id = id

    @hybrid_property
    def url(self):
        return url_for('user_overview', site_id=self.site_id)

    @hybrid_property
    def supremacy_url(self):
        return "https://www.supremacy1914.com/index.php?id=59&tx_supgames_piUserPage[uid]=" + str(self.site_id)

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<User(%s)>" % (self.id)
