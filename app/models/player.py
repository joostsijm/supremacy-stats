from app.app import db

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
    # Representation
    # -------------

    def __repr__(self):
        return "<Player(%s)>" % (self.id)
