import discord
from discord.ext import commands
import keys
from pymongo import MongoClient


class TrackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Establish connection to MongoDB
        self.mongo_client = MongoClient(keys.mongo_uri)
        self.db = self.mongo_client.betBasketBot
        try:
            # Test the connection
            self.mongo_client.server_info()
            print("MongoDB connection successful")
        except Exception as e:
            print(f"MongoDB connection error: {e}")

    # Register user (input) bets to database
    @commands.hybrid_command()
    async def register(self, ctx, matchup, team, outcome):
        embed = discord.Embed(title="Register betting pick to compare ✅",
                              description="Tracking money line team bets for users in the server to compare",
                              color=discord.Color.random())
        embed.set_author(name="Bet Basket Bot", url="https://github.com/iamjny/Bet-Basket-Bot")

        self.db.user_bets.insert_one({
            "Username": ctx.author.name,
            "Matchup": matchup,
            "Team to win": team,
            "Outcome": outcome
        })

        embed.add_field(name=f"For {ctx.author.name}",
                        value=f"Bet on {matchup} for {team} to win with final outcome '{outcome}'"
                              f" has been registered! \n\n ***Use !dashboard to see how "
                              f"your bets have performed compared to others!***",
                        inline=True)
        await ctx.send(embed=embed)

    # Displays user (input) bets from database
    @commands.hybrid_command()
    async def dashboard(self, ctx):
        # Check for empty database
        bets_cursor = list(self.db.user_bets.find())
        if len(bets_cursor) == 0:
            await ctx.send("Error: There are no bets to display on the dashboard!")

        else:

            embed = discord.Embed(title="Betting dashboard 🏆", description="Compare your winnings/losses with other users",
                                  color=discord.Color.random())
            embed.set_author(name="Bet Basket Bot", url="https://github.com/iamjny/Bet-Basket-Bot")

            for user_bet in bets_cursor:
                username = user_bet["Username"]
                matchup = user_bet["Matchup"]
                team_to_win = user_bet["Team to win"]
                outcome = user_bet["Outcome"]

                embed.add_field(name=username,
                                value=f"```\nMatchup: {matchup}\nTeam to win: {team_to_win}\nOutcome: {outcome}\n```",
                                inline=True)

            await ctx.send(embed=embed)

    # Deletes all data in database
    @commands.hybrid_command()
    async def delete_db(self, ctx):
        x = self.db.user_bets.delete_many({})
        await ctx.send(f"{x.deleted_count} document(s) deleted.")


async def setup(bot):
    await bot.add_cog(TrackCog(bot))
