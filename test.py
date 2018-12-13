
"""
Test script
"""

import sys
from datetime import datetime
from sqlalchemy.sql.expression import false
from supremacy1914_wrapper import GameDoesNotExistError
from app import db
from app.util import sync
from app.models import Game

# random game
GAME_ID = 2527307
if sys.argv[1]:
    GAME = Game.query.filter(Game.game_id == sys.argv[1]).first()
else:
    GAMES = Game.query.filter(Game.end_of_game == false()).all()
    GAME = GAMES[0]
try:
    sync.update_market(GAME)
except GameDoesNotExistError:
    GAME.end_of_game = True
    GAME.end_at = datetime.now()
    db.session.commit()

#    for GAME in GAMES:
#        try:
#            update_game_results(GAME.game_id)
#        except GameDoesNotExistError as error:
#            print()

# get_game(GAME_ID)
print("\ndone!")
