from discord.ext import commands


class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.reply("pong")

    async def on_message(self, message):
        print(message.content)


def setup(bot):
    bot.add_cog(MainCog(bot))

