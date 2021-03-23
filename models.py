from peewee import *

db = SqliteDatabase('db.sqlite3')


class Base(Model):
    class Meta:
        database = db


db.create_tables([])
db.connect()
