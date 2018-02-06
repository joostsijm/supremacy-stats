#!/usr/bin/env python

"""
Supremacy1914 ranking index retriever
"""

import time
import json
from datetime import datetime
import requests
from sqlalchemy.sql import and_

from app import db
from app.models.day import Day
from app.models.coalition import Coalition
from app.models.game import Game
from app.models.map import Map
from app.models.player import Player
from app.models.user import User
from app.models.relation import Relation


HEADERS = {
    "Host": "xgs8.c.bytro.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Accept": "text/plain, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://www.supremacy1914.nl",
    "DNT": "1",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
    }

PAYLOAD_SAMPLE = {
    "@c": "ultshared.action.UltUpdateGameStateAction",
    "playerID": 0,
    "userAuth": "787925a25d0c072c3eaff5c1eff52829475fd506",
    "tstamp": int(time.time())
    }

# temp place for variables
URL = 'https://xgs8.c.bytro.com/'


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
    if not check_response(game_id, text):
        return get_day(game, game_id)

    response = json.loads(request.text)
    result = response["result"]
    return result["dayOfGame"]


def get_score(game, day):
    """get score from players on a day"""
    payload = PAYLOAD_SAMPLE
    payload["gameID"] = game.game_id
    payload["stateType"] = 2
    payload["option"] = day

    request = requests.post(game.game_host, headers=HEADERS, json=payload)

    text = json.loads(request.text)
    if not check_response(game.id, text):
        return get_score(game, day)

    return text["result"]["ranking"]["ranking"]


def get_results(game_id):
    """Return result from game"""
    game = Game.query.filter(Game.game_id == game_id).first()
    if game is None:
        game = get_game(game_id)

    for day_index in range(game.last_day(), get_day(game, game_id)):
        day_index += 1

        print("day: " + str(day_index))
        result = get_score(game, day_index)
        result.pop(0)

        player_id = 1
        if game.players.first() is None:
            get_players(game_id)
            return get_results(game_id)

        for score in result:
            player = game.players.filter(Player.player_id == player_id).first()

            day = player.days.filter(Day.day == day_index).first()

            if day is None:
                day = Day()
                day.day = day_index
                day.points = score
                day.game_id = game.id
                day.player_id = player.id
                db.session.add(day)

            player_id += 1

        db.session.commit()

    return None


def get_game(game_id):
    """Get results from game"""
    payload = PAYLOAD_SAMPLE
    payload["gameID"] = game_id
    payload["stateType"] = 12

    game = Game.query.filter(Game.game_id == game_id).first()
    if game is None:
        game = Game()
        game.game_id = game_id
        game.game_host = URL

        db.session.add(game)
        db.session.commit()

    request = requests.post(game.game_host, headers=HEADERS, json=payload)

    text = json.loads(request.text)
    if not check_response(game_id, text):
        return get_game(game_id)

    result = text["result"]

    game.start_at = datetime.fromtimestamp(result["startOfGame"])

    game_map = Map.query.filter(Map.map_id == result["mapID"]).first()
    if game_map is None:
        game_map = Map()
        game_map.map_id = result["mapID"]
        game_map.slots = result["openSlots"] + result["numberOfPlayers"]
        db.session.add(game_map)
        db.session.commit()

    game.map_id = game_map.id
    db.session.commit()

    return game


def get_players(game_id):
    """Get a player"""
    payload = PAYLOAD_SAMPLE
    payload["gameID"] = game_id
    payload["stateType"] = 1

    game = Game.query.filter(Game.game_id == game_id).first()
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

            player = Player.query.filter(and_(
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
                    user = User.query.filter(
                        User.name == player_data["userName"]
                    ).first()

                    if user is None:
                        user = User()

                        user.site_id = player_data["siteUserID"]
                        user.name = player_data["userName"]

                        db.session.add(user)
                        db.session.commit()

                    player.user_id = user.id

                db.session.add(player)

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

            db.session.commit()


def get_relations(game_id):
    """Get the relation"""
    payload = PAYLOAD_SAMPLE
    payload["gameID"] = game_id
    payload["stateType"] = 5

    game = Game.query.filter(Game.game_id == game_id).first()
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
                    db.session.add(save_foreign_relation(
                        game,
                        player_relations,
                        player,
                        foreign_id
                    ))

        db.session.commit()


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

            db.session.add(relation)


def check_response(game_id, response):
    """Check for correct response"""
    if response["result"]["@c"] == "ultshared.rpc.UltSwitchServerException":
        game = Game.query.filter(Game.game_id == game_id).first()
        game.game_host = "http://" + response["result"]["newHostName"]

        # not needed for debug
        if "newHostName" in response["result"]:
            game.game_host = "http://" + response["result"]["newHostName"]
            db.session.commit()
        else:
            print("Problem checking response:")
            print_json(response["result"])
            exit()
        return False
    return True


if __name__ == "__main__":

    # internal game
    # GAME_ID = 2100245
    # domination
    # GAME_ID = 2117045

    # random game
    GAME_ID = 2190957

    get_results(GAME_ID)
    print("\ndone!")
