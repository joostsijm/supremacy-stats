
"""
Game model module
"""

from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_method
from app.app import db


class Game(db.Model):
    """Model for game"""
    # Table name
    __tablename__ = 'sp_games'

    #
    # Columns
    # -------------

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    game_host = db.Column(db.String)
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)

    #
    # Relationships
    # -------------

    map_id = db.Column(db.Integer, db.ForeignKey('sp_maps.id'))
    map = db.relationship("Map", back_populates="games")

    players = db.relationship("Player", back_populates="game", lazy="dynamic")

    days = db.relationship("Day", back_populates="game", lazy="dynamic")

    relations = db.relationship("Relation", back_populates="game", lazy="dynamic")

    coalitions = db.relationship("Coalition", back_populates="game")

    #
    # Attributes
    # -------------

    @hybrid_method
    def day(self):
        delta = datetime.today() - self.start_at
        return delta.days + 1

    @hybrid_method
    def last_day(self):
        day = self.days.order_by(Day.day.desc()).first()
        if day is None:
            return 0
        return day.day

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<Game(%s)>" % (self.id)
