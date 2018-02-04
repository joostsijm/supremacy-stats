from app import db


class Day(db.Model):
    # Table name
    __tablename__ = 'sp_days'

    #
    # Columns
    # -------------

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer)
    points = db.Column(db.Integer)

    #
    # Relationships
    # -------------

    player_id = db.Column(db.Integer, db.ForeignKey('sp_players.id'))
    player = db.relationship("Player", back_populates="days")

    game_id = db.Column(db.Integer, db.ForeignKey('sp_games.id'))
    game = db.relationship("Game", back_populates="days")

    coalition_id = db.Column(db.Integer, db.ForeignKey('sp_coalitions.id'))
    coalition = db.relationship("Coalition", back_populates="days")

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<Day(%s)>" % (self.id)
