import gettext

gettext.install('bot', './locale')


class Commands:
    def __init__(self, bot):
        self.bot = bot

    def ping(self, ctx):
        return _('ping_command').format(latency=int(self.bot.latency*1000))


def setup(bot):
    return Commands(bot)
