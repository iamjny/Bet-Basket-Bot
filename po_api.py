from datetime import datetime
import requests
import keys


# Re-usable class to interact with prop_odds API
class PropOddsAPI:
    def __init__(self, token):
        self.base_url = 'https://api.prop-odds.com'
        self.api_key = keys.prop_odds

    # Gets all games that takes place today
    def get_games(self):
        now = datetime.now()
        url = self.base_url + '/beta/games/nba?'
        query_params = {
            'date': now.strftime('%Y-%m-%d'),
            'tz': 'America/New_York',
            'api_key': self.api_key,
        }
        response = requests.get(url, params=query_params)
        data = response.json()
        return data

    # Gets more info about a specific game
    def get_game_info(self, game_id):
        url = self.base_url + '/beta/game/' + game_id + '?'
        query_params = {
            'api_key': self.api_key
        }
        response = requests.get(url, params=query_params)
        data = response.json()
        return data

    # Gets all markets available for a given game (money line, spreads, player points, etc.)
    def get_markets(self, game_id):
        url = self.base_url + '/beta/markets/' + game_id + '?'
        query_params = {
            'api_key': self.api_key
        }
        response = requests.get(url, params=query_params)
        data = response.json()
        return data

    # Gets the most recent odds from given market for all available bookies
    def get_most_recent_odds(self, game_id, market):
        url = self.base_url + '/beta/odds/' + game_id + '/' + market + '?'
        query_params = {
            'api_key': self.api_key,
        }
        response = requests.get(url, params=query_params)
        data = response.json()
        return data
