#!/usr/bin/env python

"""
Supremacy1914 ranking index retriever
"""

import time
import json
from datetime import datetime
import requests

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

from app.models.base import Game
from app.models.base import Map
from app.models.base import Player
from app.models.base import User
from app.models.base import Day
from app.models.base import Relation


HEADERS = {
    "Host": "xgs15.c.bytro.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:56.0) Firefox/56.0",
    "Accept": "text/plain, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Content-Length": "387",
    "Origin": "https://www.supremacy1914.com",
    "DNT": "1",
    "Connection": "keep-alive",
    }

PAYLOAD_SAMPLE = {
    "@c": "ultshared.action.UltUpdateGameStateAction",
    "playerID": 0,
    "userAuth": "787925a25d0c072c3eaff5c1eff52829475fd506",
    "tstamp": int(time.time())
    }

# temp place for variables
URL = 'https://xgs3.c.bytro.com/'
ENGINE = create_engine("postgresql://supindex@localhost/supindex")
SESSION = sessionmaker(bind=ENGINE, autoflush=False)
SESSION = SESSION()

# to check database we will execute query
try:
    SESSION.execute('SELECT 1')
except Exception:
    print("Database not working")
    exit()


def print_json(json_text):
    """Print data to console"""
    print(json.dumps(json_text, sort_keys=True, indent=4))


def get_day(game, game_id):
    """Return single day"""
    payload = PAYLOAD_SAMPLE
    payload["gameID"] = game_id
    payload["stateType"] = 12

    request = requests.post(game.game_host, headers=HEADERS, json=payload)

    text = json.loads(request.text)
    print_json(text)
    if not check_response(game_id, text):
        return get_day(game, game_id)

    response = json.loads(request.text)
    result = response["result"]
    return result["dayOfGame"]


def get_score(game, day):
    """get score from players on a day"""
    payload = PAYLOAD_SAMPLE
    payload["gameID"] = game.id
    payload["stateType"] = 2
    payload["option"] = day

    request = requests.post(game.game_host, headers=HEADERS, json=payload)

    text = json.loads(request.text)
    if not check_response(game.id, text):
        return get_score(game, day)

    return text["result"]["ranking"]["ranking"]


def get_results(game_id):
    """Return result from game"""
    game = SESSION.query(Game).filter(Game.game_id == game_id).first()
    if game is None:
        game = get_game(game_id)

    for day_index in range(0, get_day(game, game_id)):
        day_index += 1

        print("day: " + str(day_index))
        result = get_score(game, day_index)
        result.pop(0)

        player_id = 1
        for score in result:
            player = game.players.filter(Player.player_id == player_id).first()
            day = player.days.filter(Day.day == day_index).first()

            if day is None:
                day = Day()
                day.day = day_index
                day.points = score
                day.game_id = game.id
                day.player_id = player.id
                SESSION.add(day)

            player_id += 1

        SESSION.commit()


def get_game(game_id):
    """Ger results from game"""
    payload = PAYLOAD_SAMPLE
    payload["gameID"] = game_id
    payload["stateType"] = 12

    game = SESSION.query(Game).filter(Game.game_id == game_id).first()
    if game is None:
        game = Game()
        game.game_id = game_id
        game.game_host = URL

        SESSION.add(game)
        SESSION.commit()

    request = requests.post(game.game_host, headers=HEADERS, json=payload)

    text = json.loads(request.text)
    if not check_response(game_id, text):
        return get_game(game_id)

    result = text["result"]

    game.start_at = datetime.fromtimestamp(result["startOfGame"])

    game_map = SESSION.query(Map).filter(Map.map_id == result["mapID"]).first()
    if game_map is None:
        game_map = Map()
        game_map.map_id = result["mapID"]
        game_map.slots = result["openSlots"] + result["numberOfPlayers"]
        SESSION.add(game_map)
        SESSION.commit()

    game.map_id = game_map.id
    SESSION.commit()

    return game


def get_players(game_id):
    """Get a player"""
    payload = PAYLOAD_SAMPLE
    payload["gameID"] = game_id
    payload["stateType"] = 1

    game = SESSION.query(Game).filter(Game.game_id == game_id).first()
    if game is None:
        get_game(game_id)

    request = requests.post(game.game_host, headers=HEADERS, json=payload)

    text = json.loads(request.text)
    if not check_response(game_id, text):
        get_players(game_id)
    else:
        result = text["result"]["players"]
        for player_id in result:
            save_player(game, result[player_id])


def save_player(game, player_data):
    """Save a player"""
    if "playerID" in player_data:
        player_id = int(player_data["playerID"])

        if player_id > 0:
            print("player_id: " + str(player_id))

            player = SESSION.query(Player).filter(and_(
                Player.game_id == game.id,
                Player.player_id == player_id)
                                                 ).first()

            if player is None:
                player = Player()

                player.game_id = game.id
                player.player_id = player_id

                player.nation_name = player_data["nationName"]

                player.primary_color = player_data["primaryColor"]
                player.secondary_color = player_data["secondaryColor"]

                if "userName" in player_data:
                    user = SESSION.query(User).filter(
                        User.name == player_data["userName"]
                    ).first()

                    if user is None:
                        user = User()

                        user.site_id = player_data["siteUserID"]
                        user.name = player_data["userName"]

                        SESSION.add(user)
                        SESSION.commit()

                    player.user_id = user.id

                SESSION.add(player)

            player.title = player_data["title"]
            player.name = player_data["name"]

            print(player.name)

            player.defeated = player_data["defeated"]
            if player_data["lastLogin"] == 0:
                player.last_login = None
            else:
                player.last_login = datetime.fromtimestamp(
                    player_data["lastLogin"] / 1000
                )

            SESSION.commit()


def get_relations(game_id):
    """Get the relation"""
    payload = PAYLOAD_SAMPLE
    payload["gameID"] = game_id
    payload["stateType"] = 5

    game = SESSION.query(Game).filter(Game.game_id == game_id).first()
    if game is None:
        get_game(game_id)

    request = requests.post(game.game_host, headers=HEADERS, json=payload)

    text = json.loads(request.text)
    if not check_response(game_id, text):
        get_relations(game_id)
    else:
        result = text["result"]["relations"]["neighborRelations"]
        for player_id in result:
            player_relations = result[player_id]
            player = game.players.filter(
                Player.player_id == player_id
            ).first()

            if player is None:
                get_players(game_id)
            else:
                for foreign_id in player_relations:
                    SESSION.add(save_foreign_relation(
                        game,
                        player_relations,
                        player,
                        foreign_id
                    ))

        SESSION.commit()


def save_foreign_relation(game, player_relations, player, foreign_id):
    """Save foreign relation"""
    relation_status = player_relations[foreign_id]
    foreign_player = game.players.filter(
        Player.player_id == foreign_id
    ).first()

    if foreign_player is not None:
        relation = game.relations.filter(and_(
            Relation.player_native_id == player.id,
            Relation.player_foreign_id == foreign_player.id
        )).order_by(Relation.start_day.desc()).first()

        if relation is None or relation_status != relation.status:
            relation = Relation()

            relation.game_id = game.id
            relation.player_native_id = player.id
            relation.player_foreign_id = foreign_player.id

            relation.start_day = game.day()
            relation.status = relation_status

            SESSION.add(relation)


def check_response(game_id, response):
    """Check for correct response"""
    if response["result"]["@c"] == "ultshared.rpc.UltSwitchServerException":
        game = SESSION.query(Game).filter(Game.game_id == game_id).first()
        game.game_host = "http://" + response["result"]["newHostName"]
        SESSION.commit()
        return False
    return True


if __name__ == "__main__":

    # internal game
    # GAME_ID = 2100245
    # domination
    # GAME_ID = 2117045

    # random game
    GAME_ID = 2190957

    get_game(GAME_ID)
    print("\ndone!")
