import sqlite3
from sqlstatements import (
    CREATE_PLAYER_TABLE,
    CREATE_POKEMON_TABLE,
    CREATE_TEAMS_TABLE
)

from classes import (
    Pokemon,
    Team
)

class DatabaseInsertionError(Exception):
    pass

def init_database():
    connection = sqlite3.connect("mypokemondb")
    cursor = connection.cursor()
    cursor.execute(CREATE_PLAYER_TABLE)
    cursor.execute(CREATE_POKEMON_TABLE)
    cursor.execute(CREATE_TEAMS_TABLE)
    connection.commit()
    return connection

def get_player_names(connection) -> list:
    cursor = connection.cursor()
    cursor.execute("SELECT player_name FROM players")
    player_names = cursor.fetchall()
    return player_names

def get_team_names_from_version(connection, version: str) -> list:
    cursor = connection.cursor()
    cursor.execute("SELECT team_name FROM teams WHERE version = ?", (version,))
    team_names = cursor.fetchall()
    return team_names

def get_team_names_from_player_name(connection, player_name) -> list:
    cursor = connection.cursor()
    player_id = get_player_id_from_name(player_name)
    if player_id == None: return None
    cursor.execute("SELECT team_name FROM teams WHERE player_id = ?", (player_id,))
    team_names = cursor.fetchall()
    return team_names

def get_player_id_from_name(connection, player_name) -> int:
    cursor = connection.cursor()
    cursor.execute("SELECT player_id FROM players WHERE player_name = ?", (player_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None
    
def add_player(connection, player_name: str) -> int:
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO players (player_name) VALUES (?)", (player_name,))
    connection.commit()
    return get_player_id_from_name(connection, player_name)

def add_pokemon(connection, pokemon: Pokemon) -> int:
    cursor = connection.cursor()
    cursor.execute("""
                   INSERT OR IGNORE INTO pokemon 
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

def add_team(connection, new_team: Team):
    team_name = new_team.get_team_name()
    cursor = connection.cursor()
    player_id = add_player(connection, new_team.get_player_name())
    pokemon_ids = []
    for pokemon in new_team.get_all_pokemon():
        if pokemon is None: continue
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

    
    