# -*- coding: utf-8 -*-

from peewee import *

db = SqliteDatabase(                                            # initializing database instance
    'base.db'
)


class Menu(Model):                                              # creating db-model for food menu
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


class Subdata(Model):                                           # creating db-model for additional data
    name = TextField()
    fid = TextField()

    class Meta:
        database = db
        table_name = 'Subdata'


class Notify(Model):
    cid = IntegerField()                                        # creating db-model for notifications
    time = TextField()
    res = TextField()

    class Meta:
        database = db
        table_name = 'Notifications'
