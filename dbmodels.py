from peewee import *
from playhouse.sqliteq import SqliteQueueDatabase

db1 = SqliteQueueDatabase(
    'base.db',
    autostart=True,
    queue_max_size=128,
    results_timeout=5.0
)

db = SqliteDatabase(
    'base.db'
)


class Menu(Model):
    date = TextField()
    tipp = TextField(default='[]')
    komponentenessen = TextField(default='[]')
    beilagen = TextField(default='[]')
    aktionen = TextField(default='[]')
    suppe = TextField(default='[]')
    extra = TextField(default='[]')

    class Meta:
        database = db
        table_name = 'Menus'
