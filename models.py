from peewee import *

db = SqliteDatabase('db.sqlite3')


class Base(Model):
    class Meta:
        database = db


class User(Base):
    user_id = IntegerField(unique=True)


class Guild(Base):
    guild_id = IntegerField(unique=True)
    settings = BlobField(null=True)


class UserInGuild(Base):
    user = ForeignKeyField(User)
    guild = ForeignKeyField(User)
    settings = BlobField(null=True)
    roles = BlobField(null=True)
    guild_username = BlobField(null=True)


db.create_tables([User, Guild, UserInGuild])
db.connect()
