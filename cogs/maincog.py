from discord.ext import commands
import cogs as c
import errors


class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.c = c.setup(bot)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(embed=await self.c.ping(ctx))

    @commands.command(aliases=['version', 'status'])
    async def info(self, ctx):
        await ctx.send(embed=await self.c.info(ctx))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await self.c.on_error(ctx, error)

    async def on_message(self, message):
        print(message.content)


def setup(bot):
    bot.add_cog(MainCog(bot))
