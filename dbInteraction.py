import sqlite3
from sqlstatements import CREATE_TEAMS_TABLE

def init_database():
    connection = sqlite3.connect("mypokemondb")
    cursor = connection.cursor()
    cursor.execute(CREATE_TEAMS_TABLE)
    connection.commit()
    return connection

def get_player_names(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT player_name FROM teams")
    player_names = cursor.fetchall()
    return player_names

def get_team_names_from_version(connection, version):
    cursor = connection.cursor()
    cursor.execute("SELECT team_name FROM teams WHERE version = ?", (version,))
    team_names = cursor.fetchall()
    return team_names