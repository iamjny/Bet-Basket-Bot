import discord
from discord.ext import commands
import keys
import po_api
from pycaret.regression import *
import pandas as pd
from datetime import date
import math


class BetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.po = po_api.PropOddsAPI(keys.prop_odds)  # Replace 'keys.prop_odds' with your own API key
        self.games = self.po.get_games()

    # Lists the commands available for this bot
    @commands.hybrid_command()
    async def cmd(self, ctx):
        embed = discord.Embed(title="Commands available 👨‍💻",
                              description="Here is a comprehensive list of available commands and their "
                                          "functionalities: ",
                              color=discord.Color.random())
        embed.set_author(name="Bet Basket Bot", url="https://github.com/iamjny/Bet-Basket-Bot")
        embed.add_field(name="today", value="Displays today's NBA matchups", inline=True)
        embed.add_field(name="ml_odds", value="Displays today's NBA matchups money line odds provided by FanDuel",
                        inline=False)
        embed.add_field(name="predict",
                        value="Displays user inputted NBA matchup (ex: LAL vs. GSW) winning prediction using trained "
                              "ML regression model", inline=True)
        embed.add_field(name="team_acronyms",
                        value="Displays all NBA team acronyms", inline=False)
        embed.add_field(name="register",
                        value="Register a (user input) bet in a database to track later on with !dashboard. Input must follow the following format"
                              ": !register [matchup] [team you're betting to win] [outcome (win/loss)] ", inline=False)
        embed.add_field(name="dashboard",
                        value="Displays bets registered by users to compare", inline=False)
        embed.add_field(name="delete_db",
                        value="Delete bets from database", inline=False)
        await ctx.send(embed=embed)

    # Lists the team acronyms for reference when using the !predict command
    @commands.hybrid_command()
    async def team_acronyms(self, ctx):
        embed = discord.Embed(title="Team acronyms 📝",
                              description="In the image below, you will find a list of NBA team acronyms that you can use for the !predict command inputs:",
                              color=discord.Color.random())
        embed.set_author(name="Bet Basket Bot", url="https://github.com/iamjny/Bet-Basket-Bot")
        embed.set_image(
            url="https://user-images.githubusercontent.com/12113222/32106524-925211e2-baf1-11e7-95e0-5d82a52cc7c0.png")
        await ctx.send(embed=embed)

    # Lists today's NBA game matchups
    @commands.hybrid_command()
    async def today(self, ctx):
        game_count = len(self.games['games'])
        embed = discord.Embed(title="Today's NBA games 📅",
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

    # Lists today's games money line odds
    @commands.hybrid_command()
    async def ml_odds(self, ctx):
        game_ids = [game['game_id'] for game in self.games['games']]

        if not game_ids:
            await ctx.send('Error: There are no money line odds available since there are no games today.')
        else:

            embed = discord.Embed(title="Today's money line odds 💰",
                                  description=f'These are the following money line odds from FanDuel for today ({date.today()}):',
                                  color=discord.Color.random())
            embed.set_author(name="Bet Basket Bot", url="https://github.com/iamjny/Bet-Basket-Bot")

            game_count = 1

            for game_id in game_ids:

                # Fetch odds
                all_odds = self.po.get_most_recent_odds(game_id, 'moneyline')
                inline_value = True

                for bookie_data in all_odds['sportsbooks']:
                    bookie_name = bookie_data['bookie_key']

                    if len(embed.fields) >= 9:
                        await ctx.send(embed=embed)
                        embed.clear_fields()

                    if bookie_name == 'fanduel':

                        embed.add_field(name=f"\nGame #{game_count}", value="", inline=inline_value)
                        game_count += 1

                        # Iterate through outcomes (teams)
                        for outcome in bookie_data['market']['outcomes']:
                            team_name = outcome['name']
                            odds = outcome['odds']

                            embed.add_field(name=f"{team_name}", value=f"Odds: {odds}", inline=inline_value)

                    inline_value = not inline_value

            if len(embed.fields) > 0:
                await ctx.send(embed=embed)

    # Predicts chances of a team winning in a user input matchup
    @commands.hybrid_command()
    async def predict(self, ctx, *, matchup):
        # Loading trained model and using relevant dataset generated from nba_data_gen.py
        # Dataset contains variables like W/L, points, home-field advantage, etc.
        loaded_model = load_model('bet_model')
        dfa = pd.read_csv('data/nba_game_data_080224.csv')
        prediction = predict_model(loaded_model, data=dfa)

        embed = discord.Embed(title="Predict winning team through ML 🤖",
                              description="Using a regression model to predict the "
                                          "winning team of"
                                          " the following user inputted matchup (on a scale of 0 to 1):",
                              color=discord.Color.random())
        embed.set_author(name="Bet Basket Bot", url="https://github.com/iamjny/Bet-Basket-Bot")

        matchup_data = prediction[prediction['MATCHUP'] == matchup]
        avg_prediction = matchup_data['prediction_label'].mean()

        # Error check before posting embed message
        if math.isnan(avg_prediction):
            embed.add_field(name=f"{matchup}", value=f"__Error: Please check the matchup format (ex: LAL "
                                                     f"vs. GSW or LAL @ GSW) or ensure that the teams exist.__\n\n Check below for the teams acronyms:",
                            inline=True)
            embed.set_image(
                url="https://user-images.githubusercontent.com/12113222/32106524-925211e2-baf1-11e7-95e0-5d82a52cc7c0.png")
            await ctx.send(embed=embed)
        else:
            user_input = matchup.split()
            first_word = user_input[0]
            embed.add_field(name=f"{matchup}", value=f"Chances of {first_word} winning: __{avg_prediction:.3f}__",
                            inline=True)
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(BetCog(bot))
