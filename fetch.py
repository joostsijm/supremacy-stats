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
from app.models import Game, Map, Player, User, Relation, Day


HEADERS = {
    "Host": "xgs8.c.bytro.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) " +
                  "Gecko/20100101 Firefox/57.0",
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
    print("day: " + str(day))
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
        game = update_game(game_id)

    game.fetch_at = datetime.now()

    get_players(game_id)
    # get_relations(game_id)

    for day_index in range(game.last_day, get_day(game, game_id)):
        day_index += 1

        result = get_score(game, day_index)
        result.pop(0)

        player_id = 0

        for score in result:
            player_id += 1
            if score >= 20:
                player = game.players.filter(
                    Player.player_id == player_id
                    ).first()
                day = player.days.filter(Day.day == day_index).first()

                if day is None:
                    day = Day()
                    day.day = day_index
                    day.points = score
                    day.game_id = game.id
                    day.player_id = player.id
                    db.session.add(day)

    db.session.commit()

    print("return game")
    return game


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

    return text["result"]


def save_game(game_id, result):
    """Save game results in database"""

    game = Game.query.filter(Game.game_id == game_id).first()
    if game.start_at is None:
        save_new_game(game, result)

    game.number_of_players = result["numberOfPlayers"] - result["openSlots"]
    game.end_of_game = result["endOfGame"]
    game.next_day_time = datetime.fromtimestamp(
        result["nextDayTime"] / 1000
    )

    db.session.commit()

    return game

def save_new_game(game, result):
    """Save new game results to database"""
    game.start_at = datetime.fromtimestamp(result["startOfGame"])
    game.password = result["password"]
    game.scenario = result["scenarioID"]
    game.ranked = result["ranked"]
    game.gold_round = result["goldRound"]
    game.ai_level = result["aiLevel"]
    game.country_selection = result["countrySelection"]
    game.time_scale = result["timeScale"]
    game.team_setting = result["teamSettings"]
    game.victory_points = result["victoryPoints"]
    game.research_days_offset = result["researchDaysOffset"]
    game.research_time_scale = result["researchTimeScale"]
    game.team_victory_points = result["teamVictoryPoints"]

    game_map = Map.query.filter(Map.map_id == result["mapID"]).first()
    if game_map is None:
        game_map = Map()
        game_map.map_id = result["mapID"]
        game_map.slots = result["openSlots"] + result["numberOfPlayers"]

        db.session.add(game_map)
        db.session.commit()

    game.map_id = game_map.id
    db.session.commit()


def update_game(game_id):
    """Get existing game and save to database"""
    result = get_game(game_id)
    game = save_game(game_id, result)
    return game


def update_game_details(game_id):
    """Get game and save all data to database"""
    result = get_game(game_id)
    game = save_game(game_id, result)
    save_new_game(game, result)


def get_players(game_id):
    """Get a player"""
    print("Get players")

    payload = PAYLOAD_SAMPLE
    payload["gameID"] = game_id
    payload["stateType"] = 1

    game = Game.query.filter(Game.game_id == game_id).first()
    if game is None:
        game = update_game(game_id)

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
            player = Player.query.filter(
                and_(
                    Player.game_id == game.id,
                    Player.player_id == player_id
                )
            ).first()

            if player is None:
                player = Player()

                player.start_day = game.last_day
                player.nation_name = player_data["nationName"]
                player.primary_color = player_data["primaryColor"]
                player.secondary_color = player_data["secondaryColor"]

            player.game_id = game.id
            player.player_id = player_id

            if "userName" in player_data and not player.user_id:
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

            player.title = player_data["title"]
            player.name = player_data["name"]

            player.defeated = player_data["defeated"]
            if player_data["lastLogin"] != 0:
                player.last_login = datetime.fromtimestamp(
                    player_data["lastLogin"] / 1000
                )

            db.session.add(player)
            db.session.commit()


def get_relations(game_id):
    """Get the relations"""
    print("Get relations")

    payload = PAYLOAD_SAMPLE
    payload["gameID"] = game_id
    payload["stateType"] = 5

    game = Game.query.filter(Game.game_id == game_id).first()
    if game is None:
        game = update_game(game_id)

    request = requests.post(game.game_host, headers=HEADERS, json=payload)

    text = json.loads(request.text)
    if not check_response(game_id, text):
        get_relations(game_id)
    else:
        result = text["result"]["relations"]["neighborRelations"]

        game.relations.update({Relation.end_day: game.last_day})

        for native_id in result:
            relations = result[native_id]
            for foreign_id in relations:
                if foreign_id != native_id:
                    save_foreign_relation(
                        game,
                        relations,
                        native_id,
                        foreign_id
                    )

        db.session.commit()


def save_foreign_relation(game, player_relations, native_id, foreign_id):
    """Save foreign relation"""
    relation_status = player_relations[foreign_id]

    native_player = game.players.filter(
        Player.player_id == native_id
    ).first()

    foreign_player = game.players.filter(
        Player.player_id == foreign_id
    ).first()

    relation = game.relations.filter(and_(
        Relation.player_native_id == native_player.id,
        Relation.player_foreign_id == foreign_player.id
        )).order_by(Relation.start_day.desc()).first()

    if relation is None:
        relation = Relation()

        relation.game_id = game.id
        relation.player_native_id = native_player.id
        relation.player_foreign_id = foreign_player.id

        relation.start_day = game.day
        relation.status = relation_status

        db.session.add(relation)

    elif relation_status == relation.status:
        relation.end_day = None


def check_response(game_id, response):
    """Check for correct response"""
    if response["result"]["@c"] == "ultshared.rpc.UltSwitchServerException":
        game = Game.query.filter(Game.game_id == game_id).first()

        if "newHostName" in response["result"]:
            print("new host: " + response["result"]["newHostName"])
            game.game_host = "http://" + response["result"]["newHostName"]
            db.session.commit()
        else:
            print("Game does not exist")
            print_json(response["result"])
        return False

    return True


def get_coalitions(game_id):
    """Get game coalitions"""
    print("Get coalitions")

    payload = PAYLOAD_SAMPLE
    payload["gameID"] = game_id
    payload["stateType"] = 5

    game = Game.query.filter(Game.game_id == game_id).first()
    if game is None:
        game = update_game(game_id)

    request = requests.post(game.game_host, headers=HEADERS, json=payload)

    text = json.loads(request.text)
    if not check_response(game_id, text):
        get_relations(game_id)
    else:
        return


if __name__ == "__main__":

    # random game
    GAME_ID = 2467682

    get_game(GAME_ID)
    print("\ndone!")
