from discord.ext import commands
import discord
import os
from discord_slash import SlashCommand
import settings

# отправляем сообщение админу о загрузке
if settings.debug:
    try:
        os.system('python3 backup_db.py boot')
    except:
        pass

bot = commands.Bot(command_prefix=os.environ.get('PREFIX', '.'), intents=discord.Intents.all(),
                   help_command=None)
slash = SlashCommand(bot, sync_commands=True)
bot.load_extension("cogs.maincog")
bot.load_extension("cogs.slashcog")
bot.run(os.environ['TOKEN'])
