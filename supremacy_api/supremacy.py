"""The Supremacy 1914 class"""

import time
import json
import requests


class Supremacy():
    """The supremacy class allow easy asses to the Supremacy 1914 API"""

    game_id = None
    url = None

    default_params = {
        "@c": "ultshared.action.UltUpdateGameStateAction",
        "playerID": 0,
        "userAuth": "787925a25d0c072c3eaff5c1eff52829475fd506",
        "tstamp": int(time.time())
    }

    headers = {
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

    def __init__(self, game_id, url):
        """Initialize api"""
        self.game_id = game_id
        self.url = url
        self.default_params["gameID"] = game_id

    @classmethod
    def game(cls):
        """Return game information"""
        return True

    @classmethod
    def coalitions(cls):
        """Return coalition list and members"""
        return True

    @classmethod
    def players(cls):
        """Return list of players"""
        return True

    @classmethod
    def market(cls):
        """Return market prices"""
        return True

    @classmethod
    def score(cls, day):
        """Return score of specified day"""
        print(day)
        return True

    @classmethod
    def relation(cls):
        """Return list of relations between people"""
        return True

    @classmethod
    def _request(cls, state_type, day=None):
        """Make request to the server"""
        params = cls.default_params
        params["stateType"] = state_type

        if day is not None:
            params["option"] = day

        request = requests.post(cls.url, headers=cls.headers, json=params)
        response = json.loads(request.text)

        if response["result"]["@c"] == "ultshared.rpc.UltSwitchServerException":
            if "newHostName" in response["result"]:
                new_url = "http://%s" % response["result"]["newHostName"]
                print("new host: %s for %s" % (new_url, cls.game_id))

                raise ServerChangeError(new_url)
            else:
                print("Game %s does not exist" % cls.game_id)

                raise GameDoesNotExistError("Game %s is not found" % cls.game_id)

        return response


class GameDoesNotExistError(Exception):
    """Raise when game does not exist"""
    pass


class ServerChangeError(Exception):
    """Raise when server has changed"""
    pass
