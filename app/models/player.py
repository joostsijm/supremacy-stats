
"""
Player model module
"""

from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.sql.expression import func

from app import db
from app.models.day import Day

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

    native_relations = db.relationship("Relation", foreign_keys="Relation.player_native_id", back_populates="player_native")

    foreign_relations = db.relationship("Relation", foreign_keys="Relation.player_foreign_id", back_populates="player_foreign")

    #
    # Attributes
    # -------------

    @hybrid_method
    def points(self):
        return self.today().points

    @hybrid_method
    def today(self):
        return self.days.query.filter(func.max(Day.day)).first()

    @hybrid_method
    def last_day_percentage(self):
        today = self.today()
        yesterday = self.days.query.filter(Day.day == today.day - 1).first()
        percentage = 100 * (today.points - yesterday.points) / today.points
        return percentage

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<Player(%s)>" % (self.id)
