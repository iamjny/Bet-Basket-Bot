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
    for game in games['games']:
        away = game['away_team']
        home = game['home_team']
        embed.add_field(name=f'{away} @ {home}', value="\n", inline=False)

    await ctx.send(embed=embed)

bot.run(keys.token, log_handler=None)
