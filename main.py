from discord.ext import commands
import os

bot = commands.Bot(command_prefix='/')
bot.load_extension("cogs.maincog")
bot.run(os.environ['TOKEN'])
