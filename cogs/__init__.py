import gettext
import discord
import settings as st
import traceback
from discord.ext.commands import errors as cog_errors
import sys

langs = {}


def lang_init(l='en'):
    path = './locale'
    lang = gettext.translation('bot', path, [l])
    return lang.gettext


def init():
    for lang in ['en']:
        langs[lang] = lang_init(l=lang)


def _(text, l='en'):
    return langs[l](text)


init()


class Commands:
    def __init__(self, bot):
        self.bot = bot

    async def before_invoke(self, ctx):
        print(dir(ctx))
        print(ctx.guild)
        print(dir(ctx.guild))
        print(ctx.guild.roles)
        print(ctx.guild.categories)
        print(ctx.guild.channels)
        print(ctx.channel.nsfw)

    async def ping(self, ctx):
        await self.before_invoke(ctx)
        return _('ping_command').format(latency=int(self.bot.latency*1000))

    async def info(self, ctx):
        await self.before_invoke(ctx)
        return await self.get_embed(_('Info'), _('command_info').format(commit=st.commit))

    async def get_embed(self, title, description):
        embed = discord.Embed(title=title, description=description)
        embed.set_footer(text=_("bot_name"), icon_url=st.author_url)
        return embed

    async def on_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = ()

        msg = ''

        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, cog_errors.DisabledCommand):
            msg = _('{command} has been disabled.').format(command=ctx.command)
        elif isinstance(error, cog_errors.NoPrivateMessage):
            try:
                msg = _('{command} can not be used in private messages.').format(command=ctx.command)
                return await ctx.send(msg)
            except discord.HTTPException:
                pass
        elif isinstance(error, cog_errors.CommandNotFound):
            msg = _('Command not found')
        elif isinstance(error, (discord.ext.commands.errors.MissingRequiredArgument, cog_errors.BadArgument)):
            msg = _('Check the arguments in the command')
        else:
            msg = _('Unexpected error "{error}"').format(error=str(error))
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        return await ctx.send(msg)


def setup(bot):
    return Commands(bot)
