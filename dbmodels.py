from peewee import *
from playhouse.db_url import connect
from decouple import config

db_proxy = Proxy()
db = connect(config('DATABASE_URL', default='sqlite:///RUBdb.sqlite', cast=str), autorollback=True)
db_proxy.initialize(db)


class User(Model):
    uid = BigIntegerField()
    username = CharField(null=True)
    joined_on = DateTimeField()

    class Meta:
        database = db


def check_tables():
    if not User.table_exists():
        User.create_table()
