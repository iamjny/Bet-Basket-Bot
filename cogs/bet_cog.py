import discord
from discord.ext import commands
import keys
import po_api
from pycaret.regression import *
import pandas as pd
from datetime import date


class BetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.po = po_api.PropOddsAPI(keys.prop_odds)
        self.games = self.po.get_games()

    @commands.command()
    async def cmd(self, ctx):
        embed = discord.Embed(title="Commands available",
                              description="Here is a comprehensive list of available commands and their "
                                          "functionalities: ",
                              color=discord.Color.random())
        embed.set_author(name="Bet Basket Bot", url="https://github.com/iamjny/Bet-Basket-Bot")
        embed.add_field(name="!today", value="Displays today's NBA matchups", inline=True)
        embed.add_field(name="!team_odds", value="Displays today's NBA matchups money line odds", inline=False)
        embed.add_field(name="!predict", value="Displays user inputted NBA matchup winning prediction", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def today(self, ctx):
        game_count = len(self.games['games'])
        embed = discord.Embed(title="Today's NBA games",
                              description=f'There are {game_count} games today ({date.today()}):',
                              color=discord.Color.random())
        embed.set_author(name="Bet Basket Bot", url="https://github.com/iamjny/Bet-Basket-Bot")

        count = 1
        for game in self.games['games']:
            away = game['away_team']
            home = game['home_team']
            embed.add_field(name=f"\nGame #{count}", value=f'{away} @ {home}', inline=True)
            count += 1

        await ctx.send(embed=embed)

    @commands.command()
    async def team_odds(self, ctx):
        game_ids = [game['game_id'] for game in self.games['games']]

        embed = discord.Embed(title="Money line Odds",
                              description=f'These are the following money line odds from FanDuel for today ({date.today()}):',
                              color=discord.Color.random())
        embed.set_author(name="Bet Basket Bot", url="https://github.com/iamjny/Bet-Basket-Bot")

        game_count = 1

        for game_id in game_ids:

            # Fetch odds
            all_odds = self.po.get_most_recent_odds(game_id, 'moneyline')

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

        if len(embed.fields) > 0:
            await ctx.send(embed=embed)

    @commands.command()
    async def predict(self, ctx, *, matchup):
        loaded_model = load_model('bet_model')

        dfa = pd.read_csv('data/nba_game_data_020124.csv')

        prediction = predict_model(loaded_model, data=dfa)
        # output_columns = ['TEAM_NAME', 'MATCHUP', 'prediction_label']

        embed = discord.Embed(title="Predict",
                              description="Using a machine learning regression model to predict the following matchup:",
                              color=discord.Color.random())
        embed.set_author(name="Bet Basket Bot", url="https://github.com/iamjny/Bet-Basket-Bot")

        matchup_data = prediction[prediction['MATCHUP'] == matchup]
        avg_prediction = matchup_data['prediction_label'].mean()

        user_input = matchup.split()
        first_word = user_input[0]
        embed.add_field(name=f"{matchup}", value=f"Chances of {first_word} winning: {avg_prediction:.3f}", inline=True)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(BetCog(bot))
