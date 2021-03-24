from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
import cogs as c


class SlashCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.c = c.setup(bot)

    @cog_ext.cog_slash(name='info', description="Get bot description.")
    async def info(self, ctx):
        await ctx.send(embed=self.c.info(ctx))

    @cog_ext.cog_slash(name='ping', description="Get bot latency.")
    async def ping(self, ctx: SlashContext):
        await ctx.respond()
        await ctx.send(self.c.ping(ctx))

    async def on_message(self, message):
        print(message.content)


def setup(bot):
    bot.add_cog(SlashCog(bot))
