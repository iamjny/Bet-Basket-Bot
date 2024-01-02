from nba_api.stats.endpoints import LeagueGameFinder
from datetime import datetime
import pandas as pd

game_finder = LeagueGameFinder()

game_finder_df = game_finder.get_data_frames()[0]

game_finder_df['GAME_DATE'] = pd.to_datetime(game_finder_df['GAME_DATE'])

game_finder_df['WL'] = game_finder_df['WL'].replace({'W': 1, 'L': 0})

game_finder_df = game_finder_df[game_finder_df['GAME_DATE'] >= '2023-01-01']

today = datetime.today().strftime('%d%m%y')
filtered_csv_file = f'nba_game_data_{today}.csv'
game_finder_df.to_csv(filtered_csv_file, index=False)
print(f'Modified and filtered data has been saved to {filtered_csv_file}')

