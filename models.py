from peewee import *
try:
   import cPickle as pickle
except ModuleNotFoundError:
   import pickle
import settings as st
import time


db = SqliteDatabase('db.sqlite3')


class Base(Model):
    class Meta:
        database = db


class User(Base):
    user_id = IntegerField(unique=True)

    @staticmethod
    def get_from_object(author):
        user = User.get_or_none(user_id=author.id)
        if user is None:
            user = User(user_id=author.id)
            user.save()
        return user


class Role(Base):
    role_id = IntegerField(unique=True)
    name = TextField()
    position = IntegerField()
    permissions = IntegerField()

    @staticmethod
    def get_from_object(role):
        obj = Role.get_or_none(role_id=role.id)
        if obj is None:
            obj = Role(role_id=role.id)
        obj.name = role.name
        obj.position = role.position
        obj.permissions = role.permissions.value
        obj.save()
        return obj


class Guild(Base):
    name = TextField()
    guild_id = IntegerField(unique=True)
    settings = BlobField(null=True)
    roles = ManyToManyField(Role)

    @staticmethod
    def get_from_object(guild):
        server = Guild.get_or_none(guild_id=guild.id)
        if server is None:
            server = Guild(guild_id=guild.id)
        server.name = guild.name
        try:
            settings = pickle.loads(server.settings)
        except:
            settings = {}
        settings |= st.base_settings
        server.save()
        server.roles.clear()
        for role in guild.roles:
            server.roles.add(Role.get_from_object(role))
        server.save()
        return server, settings

    def save_settings(self, settings):
        settings |= st.base_settings
        self.settings = pickle.dumps(settings)
        self.save()


class UserInGuild(Base):
    user = ForeignKeyField(User)
    guild = ForeignKeyField(Guild)
    settings = BlobField(null=True)
    roles = BlobField(null=True)
    guild_username = BlobField(null=True)

    @staticmethod
    def get_from_object(user, guild):
        obj = UserInGuild.get_or_none(user=user, guild=guild)
        if obj is None:
            obj = UserInGuild(user=user, guild=guild)
        try:
            settings = pickle.loads(obj.settings)
        except:
            settings = {}
        settings |= st.base_user_settings
        obj.save()
        return obj, settings

    def save_settings(self, settings):
        settings |= st.base_user_settings
        self.settings = pickle.dumps(settings)
        self.save()


class Message(Base):
    parent = ForeignKeyField('self', null=True)
    user = ForeignKeyField(UserInGuild)
    message_id = IntegerField()
    text = TextField(null=True)
    timestamp = IntegerField(default=time.time)
    latest = BooleanField(True)

    @staticmethod
    def get_from_object(ctx, user):
        obj = Message.get_or_none(user=user, message_id=ctx.id)
        if obj is None:
            obj = UserInGuild(user=user, message_id=ctx.id)
        obj.text = ctx.content
        obj.message_id = ctx.id
        obj.save()
        return obj


db.connect()
db.create_tables([User, Guild, UserInGuild, Role, Guild.roles.get_through_model(),
                  Message])
