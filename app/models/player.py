
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

    native_relations = db.relationship(
        "Relation",
        foreign_keys="Relation.player_native_id",
        back_populates="player_native",
        lazy="dynamic"
    )

    foreign_relations = db.relationship(
        "Relation",
        foreign_keys="Relation.player_foreign_id",
        back_populates="player_foreign",
        lazy="dynamic"
    )

    #
    # Attributes
    # -------------

    @hybrid_property
    def points(self):
        """Display current points"""
        day = self.today()
        if day is not None:
            return day.points
        return 0

    @hybrid_method
    def today(self):
        """Return last day"""
        return self.days.order_by(Day.day.desc()).first()

    @hybrid_property
    def last_day_percentage(self):
        """Show percentage growth day"""
        day = self.today()
        if day is None:
            return 0

        yesterday = self.days.filter(Day.day == day.day - 1).first()
        if yesterday is None:
            return 0

        percentage = (day.points - yesterday.points) / yesterday.points * 100
        return round(percentage, 2)

    @hybrid_property
    def last_week_percentage(self):
        """Show percentage growth last week"""
        day = self.today()
        if day is None:
            return 0

        last_week = self.days.filter(Day.day == day.day - 7).first()
        if last_week is None:
            return 0

        percentage = (day.points - last_week.points) / last_week.points * 100
        return round(percentage, 2)

    @hybrid_property
    def fullname(self):
        """Returns player full name"""
        return "%s %s" % (self.title, self.name)

    @hybrid_property
    def last_login_formatted(self):
        """Humanize user last login"""
        if self.last_login is None:
            return ""

        return humanize.naturaltime(self.last_login)

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<Player(%s)>" % (self.id)
