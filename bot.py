import discord
from discord.ext import commands
import keys
import logging


def run():
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')
        await bot.load_extension("cogs.bet_cog")
        await bot.load_extension("cogs.track_cog")

    bot.run(keys.token, log_handler=handler)
