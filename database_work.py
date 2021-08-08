import sqlite3
from database_init import *

@db_session
def add_new_player():
    pl1 = User(players=input('players: '), nickname=input('nick: '))
    commit()

add_new_player()