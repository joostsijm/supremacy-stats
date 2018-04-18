
"""
Player model module
"""

from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property

from app import db
from app.models.day import Day
import humanize


class Player(db.Model):
    # Table name
    __tablename__ = 'sp_players'

    #
    # db.Columns
    # -------------

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer)
    start_day = db.Column(db.Integer)

    title = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=False)
    nation_name = db.Column(db.String, nullable=False)

    primary_color = db.Column(db.String)
    secondary_color = db.Column(db.String)

    defeated = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)

    #
    # Relationships
    # -------------

    user_id = db.Column(db.Integer, db.ForeignKey('sp_users.id'))
    user = db.relationship("User", back_populates="players")

    game_id = db.Column(db.Integer, db.ForeignKey('sp_games.id'))
    game = db.relationship("Game", back_populates="players")

    days = db.relationship("Day", back_populates="player", lazy="dynamic")

    native_relations = db.relationship("Relation", foreign_keys="Relation.player_native_id", back_populates="player_native", lazy="dynamic")

    foreign_relations = db.relationship("Relation", foreign_keys="Relation.player_foreign_id", back_populates="player_foreign", lazy="dynamic")

    #
    # Attributes
    # -------------

    @hybrid_method
    def points(self):
        today = self.today()
        if today is not None:
            return today.points

        return 0

    @hybrid_method
    def today(self):
        return self.days.order_by(Day.day.desc()).first()

    @hybrid_method
    def last_day_percentage(self):
        today = self.today()
        if today is None:
            return 0

        yesterday = self.days.filter(Day.day == today.day - 1).first()
        if yesterday is None:
            return 0

        percentage = (today.points - yesterday.points) / yesterday.points * 100
        return round(percentage, 2)

    @hybrid_method
    def last_week_percentage(self):
        today = self.today()
        if today is None:
            return 0

        last_week = self.days.filter(Day.day == today.day - 7).first()
        if last_week is None:
            return 0

        percentage = (today.points - last_week.points) / last_week.points * 100
        return round(percentage, 2)

    @hybrid_property
    def fullname(self):
        return "%s %s" % (self.title, self.name)

    @hybrid_property
    def last_login_formatted(self):
        if self.last_login is None:
            return ""

        return humanize.naturaltime(self.last_login)

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<Player(%s)>" % (self.id)
