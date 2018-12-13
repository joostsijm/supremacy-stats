
"""
Test script
"""

import sys
from sqlalchemy.sql.expression import false
from app.util import sync
from app.models import Game

# random game
GAME_ID = 2527307
if len(sys.argv) > 1:
    GAME = Game.query.filter(Game.game_id == sys.argv[1]).first()
else:
    GAMES = Game.query.filter(Game.end_of_game == false()).all()
    GAME = GAMES[0]

sync.update_market(GAME)

print("\ndone!")
