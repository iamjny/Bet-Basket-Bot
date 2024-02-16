from nba_api.stats.endpoints import LeagueGameFinder
from datetime import datetime
import pandas as pd

# Retrieve NBA game data from nba_api
game_finder = LeagueGameFinder()

game_finder_df = game_finder.get_data_frames()[0]

game_finder_df['GAME_DATE'] = pd.to_datetime(game_finder_df['GAME_DATE'])

# Filtering data to show W/L as 1/0
game_finder_df['WL'] = game_finder_df['WL'].replace({'W': 1, 'L': 0})

# Filtering data to show games played at the start of 2023-24 NBA season
game_finder_df = game_finder_df[game_finder_df['GAME_DATE'] >= '2023-10-05']

# Save data
today = datetime.today().strftime('%d%m%y')
filtered_csv_file = f'nba_game_data_{today}.csv'
game_finder_df.to_csv(filtered_csv_file, index=False)
print(f'Modified and filtered data has been saved to {filtered_csv_file}')

