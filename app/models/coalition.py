from app import db


class Coalition(db.Model):
    # Table name
    __tablename__ = "sp_coalitions"

    #
    # db.Columns
    # -------------

    id = db.Column(db.Integer, primary_key=True)
    coaliton_id = db.Column(db.Integer)
    name = db.Column(db.String)
    description = db.Column(db.String)

    #
    # Relationships
    # -------------

    game_id = db.Column(db.Integer, db.ForeignKey("sp_games.id"))
    game = db.relationship("Game", backref=db.backref("coalitions"))

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<Coalition(%s)>" % (self.id)
