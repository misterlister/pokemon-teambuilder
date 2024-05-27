from classes import Pokemon, Team, DatabaseInsertionError
import sqlite3
from sqlstatements import (
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

def get_team_names_from_version(connection: sqlite3.Connection, version: str) -> list:
    cursor = connection.cursor()
    cursor.execute("SELECT team_name FROM teams WHERE version = ?", (version,))
    team_names = cursor.fetchall()
    team_list = [name[0] for name in team_names]
    return team_list

def get_team_names_from_player_name(connection: sqlite3.Connection, player_name: str) -> list:
    cursor = connection.cursor()
    player_id = get_player_id_from_name(connection, player_name)
    if player_id == None: return None
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
    else:
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

def add_team(connection: sqlite3.Connection, new_team: Team) -> int:
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

def get_team_id_from_player(connection: sqlite3.Connection, team: str, player: str) -> int:
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT team_id FROM teams
                   JOIN players on teams.player_id = players.player_id
                   WHERE team_name = ? AND player_name = ?
                   """,(team, player))
    row = cursor.fetchone()
    if row:
        return row[0]
    return None

def get_team_id_from_version(connection: sqlite3.Connection, team: str, version: str) -> int:
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT team_id FROM teams
                   WHERE team_name = ? AND version = ?
                   """,(team, version))
    row = cursor.fetchone()
    if row:
        return row[0]
    return None
    

def get_team_from_db(connection: sqlite3.Connection, team_id: int) -> Team:
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT player_name, team_name, version, 
                   pokemon1, pokemon2, pokemon3,
                   pokemon4, pokemon5, pokemon6
                   FROM teams
                   JOIN players on teams.player_id = players.player_id
                   WHERE team_id = ?
                   """,(team_id,))
    row = cursor.fetchone()
    print(row)
    if row:
        player_name = row[0]
        team_name = row[1]
        version = row[3]
        pokemon_ids = row[3:9]
        
        pokemon_list = [extract_pokemon(connection, pid) if pid else None for pid in pokemon_ids]
        print("got data")
        team = Team(player_name, team_name, version,
                    pokemon_list[0], pokemon_list[1], pokemon_list[2],
                    pokemon_list[3], pokemon_list[4], pokemon_list[5], team_id)
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
                       move1=row[1], move2=row[2],
                       move3=row[3], move4=row[4])
    return None