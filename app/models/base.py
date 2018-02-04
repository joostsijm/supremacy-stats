from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

from models.day import Day
from models.player import Player
from models.coalition import Coalition
from models.relation import Relation
from models.map import Map
from models.user import User
