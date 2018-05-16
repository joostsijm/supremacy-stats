
"""
Game model module
"""

from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from flask import url_for
from app import db
import humanize

from app.models.day import Day
from app.models.map import Map
from app.models.user import User
from app.models.player import Player
from app.models.relation import Relation
from app.models.coalition import Coalition


class Game(db.Model):
    """Model for game"""
    # Table name
    __tablename__ = "sp_games"

    #
    # Columns
    # -------------

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    game_host = db.Column(db.String)
    start_at = db.Column(db.DateTime)
    fetch_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)

    #
    # Relationships
    # -------------

    map_id = db.Column(db.Integer, db.ForeignKey("sp_maps.id"))
    map = db.relationship("Map", backref=db.backref("games"))

    #
    # Attributes
    # -------------

    @hybrid_property
    def day(self):
        delta = datetime.today() - self.start_at
        return delta.days + 1

    @hybrid_property
    def last_day(self):
        day = self.days.order_by(Day.day.desc()).first()
        if day is None:
            return 0
        return day.day

    @hybrid_property
    def url(self):
        return url_for("game_overview", game_id=self.game_id)

    @hybrid_property
    def supremacy_url(self):
        return "https://www.supremacy1914.com/play.php?mode=guest&gameID=" + str(self.game_id)

    @hybrid_property
    def last_fetch(self):
        if self.fetch_at:
            return humanize.naturaltime(datetime.now() - self.fetch_at)
        else:
            return "never"

    @hybrid_property
    def start_at_formatted(self):
        return humanize.naturaldate(self.start_at)

    @hybrid_property
    def fetch_at_formatted(self):
        return humanize.naturaltime(self.fetch_at)

    @hybrid_property
    def active_players(self):
        return self.players.filter_by(Game.user_id >= 8).get()

    @hybrid_property
    def active_players_count(self):
        return self.players.filter(Player.user_id != None).count()

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<Game(%s)>" % (self.id)
