
"""
model module
"""

from app import db


class Map(db.Model):
    """Model for a map"""

    # Table name
    __tablename__ = 'sp_maps'

    #
    # Columns
    # -------------

    id = db.Column(db.Integer, primary_key=True)
    map_id = db.Column(db.Integer)
    name = db.Column(db.String)
    image = db.Column(db.String)
    slots = db.Column(db.Integer)

    #
    # Relationships
    # -------------

    games = db.relationship("Game", back_populates="map")

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<Map(%s)>" % (self.id)
