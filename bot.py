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
    intents.members = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

        # Load multiple cogs
        for ext in extensions:
            await bot.load_extension(ext)

    # Sync hybrid/slash commands globally
    @bot.command()
    @commands.is_owner()
    async def sync(ctx):
        await bot.tree.sync()
        await ctx.send('Command tree synced.')

    # Shutdown bot
    @bot.command()
    @commands.is_owner()
    async def close(ctx):
        print("Bot is now shutting down...")
        await bot.close()

    # Replace 'keys.token' with your own token
    bot.run(keys.token, log_handler=handler)
