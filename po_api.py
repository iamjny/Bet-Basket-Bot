from datetime import datetime
import requests
import keys


class PropOddsAPI:
    def __init__(self, token):
        self.base_url = 'https://api.prop-odds.com'
        self.api_key = keys.prop_odds

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

    def get_game_info(self, game_id):
        url = self.base_url + '/beta/game/' + game_id + '?'
        query_params = {
            'api_key': self.api_key
        }
        response = requests.get(url, params=query_params)
        data = response.json()
        return data

    def get_markets(self, game_id):
        url = self.base_url + '/beta/markets/' + game_id + '?'
        query_params = {
            'api_key': self.api_key
        }
        response = requests.get(url, params=query_params)
        data = response.json()
        return data

    def get_most_recent_odds(self, game_id, market):
        url = self.base_url + '/beta/odds/' + game_id + '/' + market + '?'
        query_params = {
            'api_key': self.api_key,
        }
        response = requests.get(url, params=query_params)
        data = response.json()
        return data
