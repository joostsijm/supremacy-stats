#!/usr/bin/env python

"""
Supremacy1914 ranking index retriever
"""

import json
from datetime import datetime
from sqlalchemy.sql import and_

from app import db
from app.models import Game, Map, Player, User, Relation, Day
from app.util.job import Job
from supremacy_api import Supremacy, ServerChangeError, GameDoesNotExistError


def server_change_handler(func):
    """Add catch for exception"""
    def wrapper(game):
        try:
            func(game)
        except ServerChangeError as exception:
            game.game_host = str(exception)
            func(game)
    return wrapper


@server_change_handler
def update_score(game):
    """Update result to current day"""

    supremacy = Supremacy(game.game_id, game.game_host)
    current_day = game.day

    for day_index in range(game.last_day, current_day):
        day_index += 1

        result = supremacy.score(day_index)

        ranking = result["ranking"]["ranking"]
        ranking.pop(0)

        player_id = 0

        for score in ranking:
            player_id += 1
            if score >= 20:
                player = game.players.filter(Player.player_id == player_id).first()
                day = player.days.filter(Day.day == day_index).first()

                if day is None:
                    day = Day()
                    day.day = day_index
                    day.points = score
                    day.game_id = game.id
                    day.player_id = player.id
                    db.session.add(day)

    db.session.commit()


def new_game(game_id):
    """Save new game results to database"""

    game = Game()
    game.game_id = game_id
    game.game_host = 'https://xgs8.c.bytro.com/'

    supremacy = Supremacy(game.game_id, game.game_host)

    while True:
        try:
            result = supremacy.game()
        except ServerChangeError as exception:
            new_server = str(exception)
            game.game_host = new_server
            supremacy.url = new_server
            continue
        break

    _update_game(game, result)
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
        game_map.name = result["mapID"]
        game_map.slots = result["openSlots"] + result["numberOfPlayers"]

        db.session.add(game_map)
        db.session.commit()

    game.map_id = game_map.id

    db.session.add(game)
    db.session.commit()

    return game


@server_change_handler
def update_game(game):
    """Update game to database"""

    supremacy = Supremacy(game.game_id, game.game_host)
    result = supremacy.game()

    _update_game(game, result)

    job = Job(game)
    job.check()

    db.session.commit()

    return game


def _update_game(game, result):
    """Update game stats that change"""

    game.number_of_players = result["numberOfPlayers"] - result["openSlots"]
    game.end_of_game = result["endOfGame"]
    game.day_of_game = result["dayOfGame"]
    game.next_day_time = datetime.fromtimestamp(
        result["nextDayTime"] / 1000
    )

    return game

@server_change_handler
def update_players(game):
    """Update players to database"""

    supremacy = Supremacy(game.game_id, game.game_host)
    result = supremacy.players()
    result = result["players"]

    for player_id in result:
        player_data = result[player_id]
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

                player.flag_image_id = player_data["flagImageID"]
                player.player_image_id = player_data["playerImageID"]

                player.defeated = player_data["defeated"]
                if player_data["lastLogin"] != 0:
                    player.last_login = datetime.fromtimestamp(
                        player_data["lastLogin"] / 1000
                    )

                db.session.add(player)
                db.session.commit()


@server_change_handler
def update_relations(game):
    """Get the relations"""
    print("Get relations")

    supremacy = Supremacy(game.game_id, game.game_host)
    result = supremacy.relations()
    result = result["relations"]["neighborRelations"]

    game.relations.update({Relation.end_day: game.last_day})

    for native_id in result:
        relations = result[native_id]
        for foreign_id in relations:
            if foreign_id != native_id:
                relation_status = relations[foreign_id]

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

    db.session.commit()


@server_change_handler
def update_coalitions(game):
    """Get game coalitions"""
    print("Update coalitions")


@server_change_handler
def update_market(game):
    """Get market prices"""
    print("Update market")


def print_json(json_text):
    """Print data to console"""
    print(json.dumps(json_text, sort_keys=True, indent=4))


if __name__ == "__main__":
    update_score.__module__ = "sync"

    # random game
    GAME_ID = 2527307
    GAME = Game.query.filter(Game.end_of_game == False).first()
    try:
        update_relations(GAME)
    except GameDoesNotExistError:
        print("game does not exist")

#    for GAME in GAMES:
#        try:
#            update_game_results(GAME.game_id)
#        except GameDoesNotExistError as error:
#            print()

    # get_game(GAME_ID)
    print("\ndone!")
