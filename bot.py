import discord
from discord.ext import commands
import keys
import po_api
from datetime import date

from pycaret.regression import *
import pandas as pd

# Initialize PropOddsAPI
po = po_api.PropOddsAPI(keys.prop_odds)
games = po.get_games()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


# Shows NBA matchups for today
@bot.command()
async def today(ctx):
    game_count = len(games['games'])
    embed = discord.Embed(title="NBA Schedule - Games",
                          description=f'There are {game_count} games today ({date.today()}):',
                          color=discord.Color.random())
    embed.set_author(name="Bet Basket Bot", url="https://github.com/iamjny")

    count = 1
    for game in games['games']:
        away = game['away_team']
        home = game['home_team']
        embed.add_field(name=f"\nGame #{count}", value=f'{away} @ {home}', inline=True)
        count += 1

    await ctx.send(embed=embed)


# Suggests which team to bet on using predictions from the trained ML model and money line betting odds.
@bot.command()
async def predict(ctx, *, matchup):
    loaded_model = load_model('bet_model')

    dfa = pd.read_csv('data/nba_game_data_020124.csv')

    prediction = predict_model(loaded_model, data=dfa)
    # output_columns = ['TEAM_NAME', 'MATCHUP', 'prediction_label']

    matchup_data = prediction[prediction['MATCHUP'] == matchup]
    avg_prediction = matchup_data['prediction_label'].mean()

    await ctx.send(f"For {matchup}: {avg_prediction:.3f}")


# Outputs money line betting odds for today's matchups

@bot.command()
async def team_odds(ctx):
    game_ids = [game['game_id'] for game in games['games']]

    embed = discord.Embed(title="Money line Odds",
                          description=f'These are the following money line odds from FanDuel for today ({date.today()}):',
                          color=discord.Color.random())
    embed.set_author(name="Bet Basket Bot")

    game_count = 1

    for game_id in game_ids:

        # Fetch odds
        all_odds = po.get_most_recent_odds(game_id, 'moneyline')

        il_val = True

        for bookie_data in all_odds['sportsbooks']:
            bookie_name = bookie_data['bookie_key']

            if len(embed.fields) >= 9:
                await ctx.send(embed=embed)
                embed.clear_fields()

            if bookie_name == 'fanduel':

                embed.add_field(name=f"\nGame #{game_count}", value="", inline=il_val)
                game_count += 1

                # Iterate through outcomes (teams)
                for outcome in bookie_data['market']['outcomes']:
                    team_name = outcome['name']
                    odds = outcome['odds']

                    embed.add_field(name=f"{team_name}", value=f"Odds: {odds}", inline=il_val)

            il_val = not il_val

    await ctx.send(embed=embed)


bot.run(keys.token, log_handler=None)
