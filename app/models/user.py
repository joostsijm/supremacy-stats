
"""
User model module
"""

from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from flask import url_for
from app import db, argon2
from flask_login import UserMixin


class User(db.Model, UserMixin):
    # Table name
    __tablename__ = "sp_users"

    #
    # db.Columns
    # -------------

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    site_id = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True)
    _password = db.Column("password", db.String(255))
    registration_at = db.Column(db.DateTime, default=datetime.utcnow)
    score_military = db.Column(db.Integer)
    score_economic = db.Column(db.Integer)

    #
    # Relationships
    # -------------

    #
    # Attributes
    # -------------

    def __init__(self, id=None):
        self.id = id

    @hybrid_property
    def url(self):
        """Return url user profile"""
        return url_for("user_overview", site_id=self.site_id)

    @hybrid_property
    def supremacy_url(self):
        """Return url for supremacy user profile"""
        return "https://www.supremacy1914.com/index.php?id=59&tx_supgames_piUserPage[uid]=" + str(self.site_id)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        """Hash password"""
        self._password = argon2.generate_password_hash(password)

    def check_password(self, password):
        """Check if password is correct"""
        return argon2.check_password_hash(self.password, password)


    #
    # Representation
    # -------------

    def __repr__(self):
        return "<User(%s)>" % (self.id)
