import discord
from discord.ext import commands
import keys
import logging

extensions = ["cogs.bet_cog",
              "cogs.track_cog"]


def run():

    # Creates instance of a Bot
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

        # Syncing commands to test guild
        # bot.tree.copy_global_to(guild=discord.Guild)

        # Load multiple cogs
        for ext in extensions:
            await bot.load_extension(ext)

    # Replace 'keys.token' with your own token
    bot.run(keys.token, log_handler=handler)
