from peewee import *

db = SqliteDatabase('db.sqlite3')


class Base(Model):
    class Meta:
        database = db


class User(Base):
    user_id = IntegerField(unique=True)


class Role(Base):
    role_id = IntegerField(unique=True)
    name = TextField()


class Guild(Base):
    name = TextField()
    guild_id = IntegerField(unique=True)
    settings = BlobField(null=True)
    roles = ManyToManyField(Role)

    def get_from_object(self, obj):
        return None


class UserInGuild(Base):
    user = ForeignKeyField(User)
    guild = ForeignKeyField(User)
    settings = BlobField(null=True)
    roles = BlobField(null=True)
    guild_username = BlobField(null=True)

    def get_from_object(self, obj):
        return None


class Message(Base):
    parent = ForeignKeyField('self', null=True)
    user = ForeignKeyField(UserInGuild)
    message_id = IntegerField()
    text = TextField(null=True)
    timestamp = IntegerField()
    latest = BooleanField(True)


db.connect()
db.create_tables([User, Guild, UserInGuild, Role, Guild.roles.get_through_model(),
                  Message])
