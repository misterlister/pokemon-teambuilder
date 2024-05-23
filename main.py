from editTeams import create_team
from dbInteraction import init_database


if __name__ == "__main__":
    connection = init_database()
    create_team(connection)