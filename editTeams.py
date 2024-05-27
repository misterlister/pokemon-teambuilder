from sqlite3 import Connection
from textManip import get_close_string, confirm, select_number
from printouts import print_list
from classes import Pokemon, Team
from dbInteraction import (
    get_player_names, 
    get_team_names_from_version,
    add_team
    )
from apiInteraction import (
    get_all_version_names,
    get_all_pokemon_in_dex,
    get_pokemon_moves
)

def create_team(connection: Connection) -> None:
    new_team = Team()
    try:
        player_name = get_player_name(connection)
        new_team.set_player_name(player_name)
        
        version = choose_version()
        new_team.set_version(version)
        
        team_name = choose_team_name(connection, version)
        new_team.set_team_name(team_name)
        
        team_list = choose_pokemon(version)
        assign_pokemon(new_team, team_list)
        
        if confirm("Would you like to set the team's movesets?"):
            select_movesets(new_team)
            
        new_team.printout()
        add_team(connection, new_team)
        
    except Exception as e:
        print(e)
    
def get_player_name(connection: Connection) -> str:
    valid = False
    existing_names = get_player_names(connection)
    while not valid:
        team_name = input("Please enter the name of the player who will use this team (eg. 'Ash'). Type 'list' to see all existing names: ")
        if team_name == "list":
                print_list(existing_names)
        else:
            return team_name
    
def choose_version() -> str:
    valid = False
    versions = get_all_version_names()
    while not valid:
        version = input("Please enter the game version for this team (eg. red). Type 'list' to see all options: ")
        version = version.lower()
        if version not in versions:
            if version == "list":
                print_list(versions)
            else:
                close_string = get_close_string(version, versions)
                if close_string != None:
                    if confirm(f"Did you mean '{close_string}'?"):
                        return close_string
                print(f"Sorry, '{version}' is not a valid Pokemon game version.")
                if not confirm("Would you like to try again?"):
                    return None
        else:
            return version
    
def choose_team_name(connection: Connection, version: str) -> str:
    valid = False
    existing_names = get_team_names_from_version(connection, version)
    while not valid:
        team_name = input("Please enter the name for this team (eg. 'ruby team'). Type 'list' to see all existing names: ")
        if team_name == "list":
                print_list(existing_names)
        elif team_name in existing_names:
            print("Sorry, that team name already exists for this game.")
            if not confirm("Would you like to try again?"):
                return None
        else:
            return team_name
            
def choose_pokemon(version: str) -> list:
    team_list = []
    slots_filled = 0
    to_fill = select_number(1, 6, "Please select the number of Pokemon you wish to add to your party (Between 1 and 6): ")
    available_pokemon = get_all_pokemon_in_dex(version)
    while slots_filled < to_fill:
        pokemon_name = input(f"Please enter the species name of pokemon #{slots_filled + 1} (eg. pikachu). Type 'list' to see all options: ")
        pokemon_name = pokemon_name.lower()
        if pokemon_name not in available_pokemon:
            if pokemon_name == "list":
                print(f"Available Pokemon in Pokemon {version} version:\n")
                print_list(available_pokemon)
                if len(team_list) > 0:
                    print("Team so far:")
                    print_list(team_list)
            else:
                close_string = get_close_string(pokemon_name, available_pokemon)
                if close_string != None:
                    if confirm(f"Did you mean '{close_string}'?"):
                        team_list.append(close_string)
                        slots_filled += 1
                        continue
                print(f"Sorry, '{pokemon_name}' is not a valid Pokemon in {version} version.")
                if not confirm("Would you like to try again?"):
                    return team_list
        else:
            team_list.append(pokemon_name)
            slots_filled += 1
    return team_list

def assign_pokemon(new_team: Team, team_list: list) -> None:
    if len(team_list) == 0:
        raise Exception("No pokemon for team selected. Cancelling team creation.")
    for pokemon_name in team_list:
        new_pokemon = Pokemon(pokemon_name)
        new_team.set_pokemon(new_pokemon)
    return
        

def select_movesets(team: Team) -> None:
    version = team.get_version()
    for pokemon in team.get_all_pokemon():
        if pokemon is None: return
        name = pokemon.get_species()
        print(f"Selecting moves for {name}")
        available_moves = get_pokemon_moves(version, name)
        max_moves = min(len(available_moves), 4)
        i = 1
        while i < max_moves + 1:
            selected_move = input(f"Please enter move #{i} (eg. hydro-pump). Type 'list' to see all options: ")
            selected_move = selected_move.lower()
            if selected_move not in available_moves:
                if selected_move == "list":
                    print(f"Available moves for {name} in {version} version:\n")
                    print_list(available_moves)
                else:
                    close_string = get_close_string(selected_move, available_moves)
                    if close_string != None:
                        if confirm(f"Did you mean '{close_string}'?"):
                            pokemon.set_move(close_string)
                            i += 1
                            continue
                    print(f"Sorry, '{selected_move}' is not a valid move for {name} in {version} version.")
                    if not confirm("Would you like to try again?"):
                        return
            else:
                pokemon.set_move(selected_move)
                i += 1
        print(f"{name}'s moveset:")
        print_list(pokemon.get_all_moves())
    return
        
def edit_team():
    pass


        
                        
            
        


        
