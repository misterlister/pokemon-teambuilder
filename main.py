import sqlite3
from editTeams import create_team

connection = sqlite3.connect("mypokemondb")


if __name__ == "__main__":
    create_team()