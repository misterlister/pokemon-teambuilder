"""
Contains functions dealing with interactions with the sqlite3 database.
"""

import sqlite3
from classes import Pokemon, Team, DatabaseInsertionError
from sql_statements import (
    CREATE_PLAYER_TABLE,
    CREATE_POKEMON_TABLE,
    CREATE_TEAMS_TABLE
)

def init_database() -> sqlite3.Connection:
    connection = sqlite3.connect("mypokemondb")
    cursor = connection.cursor()
    cursor.execute(CREATE_PLAYER_TABLE)
    cursor.execute(CREATE_POKEMON_TABLE)
    cursor.execute(CREATE_TEAMS_TABLE)
    connection.commit()
    return connection

def get_player_names(connection: sqlite3.Connection) -> list:
    cursor = connection.cursor()
    cursor.execute("SELECT player_name FROM players")
    player_names = cursor.fetchall()
    player_list = [name[0] for name in player_names]
    return player_list

def get_all_team_names(connection: sqlite3.Connection) -> list:
    cursor = connection.cursor()
    cursor.execute("SELECT team_name FROM teams")
    team_names = cursor.fetchall()
    team_list = [name[0] for name in team_names]
    return team_list

def get_team_names_from_version(connection: sqlite3.Connection, version: str) -> list:
    cursor = connection.cursor()
    cursor.execute("SELECT team_name FROM teams WHERE version = ?", (version,))
    team_names = cursor.fetchall()
    team_list = [name[0] for name in team_names]
    return team_list

def get_team_names_from_player_name(connection: sqlite3.Connection, player_name: str) -> list:
    cursor = connection.cursor()
    player_id = get_player_id_from_name(connection, player_name)
    if player_id is None:
        return None
    cursor.execute("SELECT team_name FROM teams WHERE player_id = ?", (player_id,))
    team_names = cursor.fetchall()
    team_list = [name[0] for name in team_names]
    return team_list

def get_player_id_from_name(connection: sqlite3.Connection, player_name: str) -> int:
    cursor = connection.cursor()
    cursor.execute("SELECT player_id FROM players WHERE player_name = ?", (player_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

def get_existing_versions(connection: sqlite3.Connection) -> list:
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT version FROM teams")
    versions = cursor.fetchall()
    version_list = [version[0] for version in versions]
    return version_list

def add_player(connection: sqlite3.Connection, player_name: str) -> int:
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO players (player_name) VALUES (?)", (player_name,))
    connection.commit()
    return get_player_id_from_name(connection, player_name)

def add_pokemon(connection: sqlite3.Connection, pokemon: Pokemon) -> int:
    cursor = connection.cursor()
    cursor.execute("""
                   INSERT INTO pokemon 
                   (pokemon_name, move1, move2, move3, move4) 
                   VALUES (?, ?, ?, ?, ?)
                   """,
                   (pokemon.get_species(),
                    pokemon.get_move_in_slot(1),
                    pokemon.get_move_in_slot(2),
                    pokemon.get_move_in_slot(3),
                    pokemon.get_move_in_slot(4)))

    if cursor.lastrowid == 0:
        connection.rollback()
        raise DatabaseInsertionError(f"Failed to insert Pokémon: {pokemon.get_species()}")

    pokemon_id = cursor.lastrowid
    connection.commit()
    return pokemon_id

def add_team(connection: sqlite3.Connection, new_team: Team) -> int:
    team_name = new_team.get_team_name()
    cursor = connection.cursor()
    player_id = add_player(connection, new_team.get_player_name())
    pokemon_ids = []
    for pokemon in new_team.get_all_pokemon():
        if pokemon is None: 
            continue
        try:
            pokemon_id = add_pokemon(connection, pokemon)
            pokemon_ids.append(pokemon_id)
        except DatabaseInsertionError as e:
            print(e)
    while len(pokemon_ids) < 6:
        pokemon_ids.append(None)

    cursor.execute("""
                   INSERT INTO teams 
                   (player_id, team_name, version, 
                   pokemon1, pokemon2, pokemon3, 
                   pokemon4, pokemon5, pokemon6)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   """,
                   (player_id, team_name, new_team.get_version(), *pokemon_ids))

    if cursor.lastrowid == 0:
        connection.rollback()
        raise DatabaseInsertionError(f"Failed to insert Team: {team_name}")

    team_id = cursor.lastrowid
    connection.commit()
    print(f"Added team {team_name} to database successfully!")
    return team_id

def get_team_from_db(connection: sqlite3.Connection, team_name: int) -> Team:
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT player_name, team_name, version, 
                   pokemon1, pokemon2, pokemon3,
                   pokemon4, pokemon5, pokemon6, team_id
                   FROM teams
                   JOIN players on teams.player_id = players.player_id
                   WHERE team_name = ?
                   """,(team_name,))
    row = cursor.fetchone()
    if row:
        player_name = row[0]
        team_name = row[1]
        version = row[2]
        pokemon_ids = row[3:9]
        team_id = row[9]

        pokemon_list = [extract_pokemon(connection, pid) if pid else None for pid in pokemon_ids]
        team = Team(player_name, team_name, version,
                    {"pokemon1": pokemon_list[0], "pokemon2": pokemon_list[1],
                     "pokemon3": pokemon_list[2], "pokemon4": pokemon_list[3],
                     "pokemon5": pokemon_list[4], "pokemon6": pokemon_list[5]},
                    team_id)
        return team
    return None

def extract_pokemon(connection: sqlite3.Connection, pokemon_id: int) -> Pokemon:
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT pokemon_name, move1, move2, move3, move4 
                   FROM pokemon
                   WHERE pokemon_id = ?
                   """, (pokemon_id,))
    row = cursor.fetchone()
    if row:
        return Pokemon(species_name=row[0],
                       moves =
                       {"move1":row[1], "move2":row[2],
                       "move3":row[3], "move4":row[4]})
    return None

def remove_pokemon(connection: sqlite3.Connection, pokemon_id: int):
    cursor = connection.cursor()

    if pokemon_id is not None:

        cursor.execute("""
                        DELETE FROM pokemon
                        WHERE pokemon_id = ?
                        """, (pokemon_id,))

        connection.commit()

def get_pokemon_id_in_slot(connection: sqlite3.Connection, team_id: int, slot: int) -> int:
    cursor = connection.cursor()
    slot_column = f"pokemon{slot}"
    cursor.execute(f"""
                   SELECT {slot_column}
                   FROM teams
                   WHERE team_id = ?
                   """, (team_id,))
    pokemon_id = cursor.fetchone()

    if pokemon_id:
        return pokemon_id[0]
    return None

def update_team_name(connection: sqlite3.Connection, team_id: int, new_team_name: str):
    try:
        cursor = connection.cursor()
        cursor.execute("""
                    UPDATE teams
                    SET team_name = ?
                    WHERE team_id = ?
                    """,
                    (new_team_name, team_id))
        connection.commit()
    except sqlite3.Error as e:
        connection.rollback()
        raise e

def update_pokemon_slot(connection: sqlite3.Connection, team_id: int, pokemon: Pokemon, slot: int):
    try:
        cursor = connection.cursor()

        slot_column = f"pokemon{slot}"
        new_id = add_pokemon(connection, pokemon)
        old_id = get_pokemon_id_in_slot(connection, team_id, slot)
        if old_id:
            remove_pokemon(connection, old_id)

        cursor.execute(f"""
                    UPDATE teams
                    SET {slot_column} = ?
                    WHERE team_id = ?
                    """,
                    (new_id, team_id))

        connection.commit()
    except sqlite3.Error as e:
        connection.rollback()
        raise e

def update_single_move(connection: sqlite3.Connection, team_id: int,
                       pokemon: Pokemon, pokemon_slot: int, moveslot: int):
    try:
        cursor = connection.cursor()

        moveslot_column = f"move{moveslot}"
        pokemon_id = get_pokemon_id_in_slot(connection, team_id, pokemon_slot)

        cursor.execute(f"""
                    UPDATE pokemon
                    SET {moveslot_column} = ?
                    WHERE pokemon_id = ?
                    """,
                    (pokemon.get_move_in_slot(moveslot), pokemon_id))

        connection.commit()
    except sqlite3.Error as e:
        connection.rollback()
        raise e

def update_moveset(connection: sqlite3.Connection, team_id: int,
                   pokemon: Pokemon, pokemon_slot: int):
    try:
        cursor = connection.cursor()

        pokemon_id = get_pokemon_id_in_slot(connection, team_id, pokemon_slot)

        cursor.execute("""
                    UPDATE pokemon
                    SET move1 = ?, move2 = ?, move3 = ?, move4 = ?
                    WHERE pokemon_id = ?
                    """,
                    (pokemon.get_move_in_slot(1),
                     pokemon.get_move_in_slot(2),
                     pokemon.get_move_in_slot(3),
                     pokemon.get_move_in_slot(4),
                     pokemon_id))

        connection.commit()
    except sqlite3.Error as e:
        connection.rollback()
        raise e
