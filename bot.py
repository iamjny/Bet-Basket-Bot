import discord
from discord.ext import commands
import keys
import po_api
from datetime import date

# Initialize PropOddsAPI
po = po_api.PropOddsAPI(keys.prop_odds)
games = po.get_games()

intents = discord.Intents.all()
# handler = logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


# Show NBA matchups for today
@bot.command()
async def matchups(ctx):
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


@bot.command()
async def moneyline(ctx):
    game_ids = [game['game_id'] for game in games['games']]

    embed = discord.Embed(title="Money line Odds",
                          description=f'These are the following money line odds from FanDuel for today ({date.today()}):',
                          color=discord.Color.random())
    embed.set_author(name="Bet Basket Bot")

    count = 1
    for game_id in game_ids:
        # Fetch odds
        all_odds = po.get_most_recent_odds(game_id, 'moneyline')

        il_val = True

        for bookie_data in all_odds['sportsbooks']:
            bookie_name = bookie_data['bookie_key']

            # Check for FanDuel odds only
            if bookie_name == 'fanduel':

                embed.add_field(name=f"\nGame #{count}", value="", inline=il_val)
                count += 1
                # Iterate through outcomes (teams)
                for outcome in bookie_data['market']['outcomes']:
                    team_name = outcome['name']
                    odds = outcome['odds']

                    # await ctx.send(f"{team_name},Odds: {odds} ")
                    embed.add_field(name=f"{team_name}", value=f"Odds: {odds}", inline=il_val)

            il_val = not il_val

    await ctx.send(embed=embed)


bot.run(keys.token, log_handler=None)
