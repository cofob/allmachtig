from discord.ext import commands
import cogs as c


class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.c = c.setup(bot)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(self.c.ping(ctx))

    async def on_message(self, message):
        print(message.content)


def setup(bot):
    bot.add_cog(MainCog(bot))
