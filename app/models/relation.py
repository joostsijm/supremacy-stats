
"""
Representation of a relation
"""

from sqlalchemy.ext.hybrid import hybrid_property

from app import db


class Relation(db.Model):
    # Table name
    __tablename__ = 'sp_relations'

    #
    # db.Columns
    # -------------

    id = db.Column(db.Integer, primary_key=True)
    start_day = db.Column(db.Integer)
    status = db.Column(db.Integer)

    #
    # Relationships
    # -------------

    game_id = db.Column(db.Integer, db.ForeignKey('sp_games.id'))
    game = db.relationship("Game", back_populates="relations")

    player_native_id = db.Column(db.Integer, db.ForeignKey('sp_players.id'))
    player_native = db.relationship("Player", foreign_keys="Relation.player_native_id", back_populates="native_relations")

    player_foreign_id = db.Column(db.Integer, db.ForeignKey('sp_players.id'))
    player_foreign = db.relationship("Player", foreign_keys="Relation.player_foreign_id", back_populates="foreign_relations")

    #
    # Attributes
    # -------------

    @hybrid_property
    def status_formatted(self):
        if self.status == -2:
            return "war"
        if self.status == -1:
            return "ceasefire"
        elif self.status == 0:
            return "peace"
        elif self.status == 3:
            return "right-of-way"
        elif self.status == 4:
            return "share-map"
        elif self.status == 6:
            return "share-information"
    #
    # Representation
    # -------------

    def __repr__(self):
        return "<Relation(%s)>" % (self.id)
