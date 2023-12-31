import keys
import po_api
import json

if __name__ == "__main__":
    po = po_api.PropOddsAPI(keys.prop_odds)
    games_data = po.get_games()
    print(games_data)

    if len(games_data['games']) == 0:
        print('No games scheduled for today.')

    game_ids = [game['game_id'] for game in games_data['games']]
    # print('Game IDs:', game_ids)

    all_odds = po.get_most_recent_odds(game_ids[-1], 'moneyline')
    print(json.dumps(all_odds, indent=2))
    for bookie_data in all_odds['sportsbooks']:
        bookie_name = bookie_data['bookie_key']
        print(f"\nBookie: {bookie_name}")

        for outcome in bookie_data['market']['outcomes']:
            team_name = outcome['name']
            odds = outcome['odds']
            print(f"Team: {team_name}, Odds: {odds}")
