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
        await ctx.send(embed=await self.c.info(ctx))

    @cog_ext.cog_slash(name='ping', description="Get bot latency.")
    async def ping(self, ctx: SlashContext):
        await ctx.respond()
        await ctx.send(embed=await self.c.ping(ctx))

    @cog_ext.cog_slash(name='set', description="Change bot settings")
    async def set(self, ctx, setting, *, value):
        await ctx.respond()
        await ctx.send(embed=await self.c.set(ctx, setting, value))

    @cog_ext.cog_slash(name='get', description="Get bot settings")
    async def get(self, ctx, setting):
        await ctx.respond()
        await ctx.send(embed=await self.c.get(ctx, setting))

    @cog_ext.cog_slash(name='error', description="Cause error")
    async def error(self, ctx):
        await ctx.respond()
        await self.c.error()

    async def on_message(self, message):
        print(message.content)


def setup(bot):
    bot.add_cog(SlashCog(bot))
