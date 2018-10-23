
"""
All models for module
"""

from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from flask import url_for
from flask_login import UserMixin, current_user
import humanize
from app import db, argon2


class Game(db.Model):
    """Model for game"""
    # Table name
    __tablename__ = "sp_games"

    #
    # Columns
    # -------------

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    game_host = db.Column(db.String)
    start_at = db.Column(db.DateTime)
    fetch_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    end_of_game = db.Column(db.Boolean, default=False)
    day_of_game = db.Column(db.Integer)
    number_of_players = db.Column(db.Integer)
    password = db.Column(db.String)
    scenario = db.Column(db.Integer)
    ranked = db.Column(db.Integer)
    gold_round = db.Column(db.Boolean, default=False)
    ai_level = db.Column(db.Integer)
    country_selection = db.Column(db.Integer)
    time_scale = db.Column(db.DECIMAL(2, 1))
    team_setting = db.Column(db.Integer)
    team_victory_points = db.Column(db.Integer)
    victory_points = db.Column(db.Integer)
    research_days_offset = db.Column(db.Integer)
    research_time_scale = db.Column(db.DECIMAL(2, 1))
    next_day_time = db.Column(db.DateTime())
    last_result_time = db.Column(db.DateTime, default=datetime.utcnow)

    #
    # Relationships
    # -------------

    map_id = db.Column(db.Integer, db.ForeignKey("sp_maps.id"))
    map = db.relationship("Map", backref=db.backref("games"))

    #
    # Attributes
    # -------------

    @hybrid_property
    def day(self):
        delta = datetime.today() - self.start_at
        return delta.days + 1

    @hybrid_property
    def last_day(self):
        day = self.days.order_by(Day.day.desc()).first()
        if day is None:
            return 0
        return day.day

    @hybrid_property
    def url(self):
        return url_for("game_overview", game_id=self.game_id)

    @hybrid_property
    def supremacy_url(self):
        """Return supremacy website url"""
        player = self.players.filter(Player.user_id == current_user.id).first()
        url = "https://www.supremacy1914.nl/play.php?gameID=%s" % str(self.game_id)
        if player is not None:
            return url + "&uid=%s" % str(current_user.site_id)
        return url + "&mode=guest"

    @hybrid_property
    def last_fetch(self):
        """Give natural last fetch date"""
        if self.fetch_at:
            return humanize.naturaltime(datetime.now() - self.fetch_at)
        return "never"

    @hybrid_property
    def start_at_formatted(self):
        """Give natural start date"""
        return humanize.naturaldate(self.start_at)

    @hybrid_property
    def fetch_at_formatted(self):
        """Give natural date"""
        return humanize.naturaltime(self.fetch_at)

    @hybrid_property
    def active_players_count(self):
        """Count active non ai players"""
        return self.players.filter(
            Player.user_id != None
        ).filter(Player.defeated == False).count()

    @hybrid_method
    def active_players(self):
        """Return active non ai players"""
        return self.players.filter(
            Player.user_id != None
        ).filter(Player.defeated == False).all()

    @hybrid_method
    def all_players(self):
        """Return all non ai players"""
        return self.players.filter(
            Player.user_id != None
        ).all()

    @hybrid_property
    def scenario_url(self):
        """Give image url for scenario"""
        return "https://supremacy1914.com/fileadmin/templates/supremacy_1914" + \
            "/images/scenarios/scenario_%s_small.jpg" % self.scenario

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<Game(%s)>" % (self.id)


class User(db.Model, UserMixin):
    # Table name
    __tablename__ = "sp_users"

    #
    # db.Columns
    # -------------

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    site_id = db.Column(db.Integer, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True)
    _password = db.Column("password", db.String(255))
    registration_at = db.Column(db.DateTime, default=datetime.utcnow)
    score_military = db.Column(db.Integer)
    score_economic = db.Column(db.Integer)

    #
    # Relationships
    # -------------

    #
    # Attributes
    # -------------

    def __init__(self, id=None):
        self.id = id

    @hybrid_property
    def url(self):
        """Return url user profile"""
        return url_for("user_overview", site_id=self.site_id)

    @hybrid_property
    def supremacy_url(self):
        """Return url for supremacy user profile"""
        return "https://www.supremacy1914.com/index.php?id=59&tx_supgames_piUserPage[uid]=" + str(self.site_id)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        """Hash password"""
        self._password = argon2.generate_password_hash(password)

    def check_password(self, password):
        """Check if password is correct"""
        return argon2.check_password_hash(self.password, password)

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<User(%s)>" % (self.id)


class Player(db.Model):
    # Table name
    __tablename__ = "sp_players"

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

    flag_image_id = db.Column(db.Integer)
    player_image_id = db.Column(db.Integer)

    #
    # Relationships
    # -------------

    user_id = db.Column(db.Integer, db.ForeignKey("sp_users.id"))
    user = db.relationship("User", backref=db.backref("players", lazy="dynamic"))

    game_id = db.Column(db.Integer, db.ForeignKey("sp_games.id"))
    game = db.relationship("Game", backref=db.backref("players", lazy="dynamic"))

    #
    # Attributes
    # -------------

    @hybrid_property
    def points(self):
        today = self.today()
        if today is not None:
            return today.points

        return 0

    @hybrid_method
    def today(self):
        return self.days.order_by(Day.day.desc()).first()

    @hybrid_property
    def last_day_percentage(self):
        today = self.today()
        if today is None:
            return 0

        yesterday = self.days.filter(Day.day == today.day - 1).first()
        if yesterday is None:
            return 0

        percentage = (today.points - yesterday.points) / yesterday.points * 100
        return round(percentage, 2)

    @hybrid_property
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

    @hybrid_property
    def player_image_url(self):
        """Return url for player image"""
        return "https://static1.bytro.com/games/sup/%s/%s/%s.png" % (
            str(self.game.game_id)[:4],
            str(self.game.game_id)[-3:],
            self.player_image_id
        )

    @hybrid_property
    def flag_image_url(self):
        """Return url for flag image"""
        return "https://static1.bytro.com/games/sup/%s/%s/%s.png" % (
            str(self.game.game_id)[:4],
            str(self.game.game_id)[-3:],
            self.flag_image_id
        )

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<Player(%s)>" % (self.id)


class Relation(db.Model):
    # Table name
    __tablename__ = "sp_relations"

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

    game_id = db.Column(db.Integer, db.ForeignKey("sp_games.id"))
    game = db.relationship("Game", backref=db.backref("relations", lazy="dynamic"))

    player_native_id = db.Column(db.Integer, db.ForeignKey("sp_players.id"))
    player_native = db.relationship("Player", foreign_keys="Relation.player_native_id", backref=db.backref("native_relations", lazy="dynamic"))

    player_foreign_id = db.Column(db.Integer, db.ForeignKey("sp_players.id"))
    player_foreign = db.relationship("Player", foreign_keys="Relation.player_foreign_id", backref=db.backref("foreign_relations", lazy="dynamic"))

    #
    # Attributes
    # -------------

    @hybrid_property
    def status_formatted(self):
        """Return description of the relation"""
        status_list = {
            -2: "war",
            -1: "ceasefire",
            0: "trade-embargo",
            1: "peace",
            3: "right-of-way",
            4: "share-map",
            6: "share-info",
            7: "army-commmand"
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


class Day(db.Model):
    # Table name
    __tablename__ = "sp_days"

    #
    # Columns
    # -------------

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer)
    points = db.Column(db.Integer)

    #
    # Relationships
    # -------------

    player_id = db.Column(db.Integer, db.ForeignKey("sp_players.id"))
    player = db.relationship("Player", backref=db.backref("days", lazy="dynamic"))

    game_id = db.Column(db.Integer, db.ForeignKey("sp_games.id"))
    game = db.relationship("Game", backref=db.backref("days", lazy="dynamic"))

    coalition_id = db.Column(db.Integer, db.ForeignKey("sp_coalitions.id"))
    coalition = db.relationship("Coalition", backref=db.backref("days"))

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<Day(%s)>" % (self.id)


class Map(db.Model):
    """Model for a map"""

    # Table name
    __tablename__ = "sp_maps"

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

    #
    # Representation
    # -------------

    def __repr__(self):
        return "<Map(%s)>" % (self.id)


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
    start_day = db.Column(db.Integer)
    end_day = db.Column(db.Integer)

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
