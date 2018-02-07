from app import db


class User(db.Model):
    # Table name
    __tablename__ = 'sp_users'

    #
    # db.Columns
    # -------------

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    site_id = db.Column(db.Integer, unique=True, nullable=False)
    score_military = db.Column(db.Integer)
    score_economic = db.Column(db.Integer)

    #
    # Relationships
    # -------------

    players = db.relationship("Player", back_populates="user", lazy="dynamic")

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<User(%s)>" % (self.id)
