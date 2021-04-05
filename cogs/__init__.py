import gettext
import discord
import settings as st
import traceback
from discord.ext.commands import errors as cog_errors
import sys
import asyncio
import models
import errors

try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle
from collections import namedtuple

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
Info = namedtuple('Info', ['server', 'server_settings', 'author', 'author_settings', 'user',
                           'message'])


class Commands:
    def __init__(self, bot):
        self.bot = bot

    async def before_invoke(self, ctx):
        server = models.Guild.get_from_object(ctx.guild)
        server[0].save()
        if ctx.author.bot:
            raise errors.IgnoringBot
        user = models.User.get_from_object(ctx.author)
        author = models.UserInGuild.get_from_object(user, server[0])
        # message = models.Message.get_from_object(ctx.message, author[0])
        message = None
        return Info(server=server[0], server_settings=server[1], author=author[0],
                    author_settings=author[1], user=user, message=message)

    async def error(self):
        blablabla

    async def ping(self, ctx):
        await self.before_invoke(ctx)
        return await self.get_embed(_('Ping'), _('ping_command').format(latency=int(self.bot.latency * 1000)))

    async def get(self, ctx, setting: str):
        info = await self.before_invoke(ctx)
        setting = setting.lower()
        s = info.server_settings['user'].get(setting)
        if s is not None:
            return await self.get_embed(_('Setting "{}"').format(setting), _('Value: **{}**').format(s))
        else:
            raise errors.SettingNotFound

    async def set(self, ctx, setting: str, value: str):
        info = await self.before_invoke(ctx)
        setting = setting.lower()
        schema = st.settings['schema'].get(setting)
        if schema is not None:
            info.server_settings['user'][setting] = schema['type'](value)
            if schema['check_type'] == 'minmax':
                if schema['max'] >= info.server_settings['user'][setting] >= schema['min']:
                    info.server.save_settings(info.server_settings)
                    return await self.get_embed(_('Success'), _('Applied!'))
                else:
                    info.server_settings['user'][setting] = schema['default']
                    info.server.save_settings(info.server_settings)
                    raise errors.MinMaxError
            elif schema['check_type'] is None:
                info.server.save_settings(info.server_settings)
                return await self.get_embed(_('Success'), _('Applied!'))
        else:
            raise errors.SettingNotFound

    async def info(self, ctx):
        info = await self.before_invoke(ctx)
        return await self.get_embed(_('Info'), _('command_info').format(commit=st.commit))

    async def get_embed(self, title, description, color='darkgrey'):
        embed = discord.Embed(title=title, description=description, color=st.colors[color])
        embed.set_footer(text=_("bot_name"), icon_url=st.author_url)
        return embed

    async def on_message(self, ctx):
        await self.before_invoke(ctx)

    async def on_error(self, ctx, error):
        info = await self.before_invoke(ctx)

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
            except discord.HTTPException:
                pass
        elif isinstance(error, cog_errors.CommandNotFound):
            if info.server_settings['user']['error_on_non_existent_command'] == 0:
                return
            msg = _('Command not found')
        elif isinstance(error, errors.SettingNotFound):
            msg = _('Setting not found, read the docs.')
        elif isinstance(error, errors.IgnoringBot):
            return
        elif isinstance(error, errors.MinMaxError):
            msg = _('Min/Max error')
        elif isinstance(error, (discord.ext.commands.errors.MissingRequiredArgument, cog_errors.BadArgument)):
            msg = _('Check the arguments in the command')
        else:
            msg = _('Unexpected error "{error}"').format(error=str(error))
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        m = await ctx.send(msg)
        print(info.server_settings)
        if info.server_settings['user']['delete_error_messages'] != 0:
            await asyncio.sleep(info.server_settings['user']['delete_error_messages'])
            await m.delete()


def setup(bot):
    return Commands(bot)
