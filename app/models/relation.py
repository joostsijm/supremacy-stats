
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
    end_day = db.Column(db.Integer)
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
        """Return description of the relation"""
        status_list = {
            -2: "war",
            -1: "ceasefire",
            0: "peace",
            3: "right-of-way",
            4: "share-map",
            6: "share-info"
        }
        status = self.status
        if status in status_list:
            return status_list[status]
        return "unknown"

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<Relation(%s)>" % (self.id)
