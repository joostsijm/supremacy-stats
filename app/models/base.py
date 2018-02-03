from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

from app.models.day import Day
from app.models.player import Player
from app.models.coalition import Coalition
from app.models.relation import Relation
from app.models.map import Map
from app.models.user import User
