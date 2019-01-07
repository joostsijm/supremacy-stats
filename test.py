
"""
Test script
"""

import sys
import random
from sqlalchemy.sql.expression import false
from app.util import sync
from app.models import Game

if len(sys.argv) > 2:
    # Search game by id
    GAME = Game.query.filter(Game.game_id == sys.argv[2]).first()
else:
    # Get random game
    GAMES = Game.query.filter(Game.end_of_game == false()).all()
    GAME = random.choice(GAMES)

SYNC_FUNCTIONS = {
    "combined": sync.update_combined,
    "game": sync.update_game,
    "players": sync.update_players,
    "score": sync.update_score,
    "relations": sync.update_relations,
    "market": sync.update_market,
    "coalitions": sync.update_coalitions,
}

if len(sys.argv) > 1:
    if sys.argv[1] in SYNC_FUNCTIONS:
        # Run function from argument
        SYNC_FUNCTIONS[sys.argv[1]](GAME)
    else:
        print("%s is not a function" % sys.argv[1])
else:
    # Run random function
    SYNC_FUNCTIONS[random.choice(list(SYNC_FUNCTIONS.keys()))](GAME)
