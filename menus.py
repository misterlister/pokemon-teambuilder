from sqlite3 import Connection
from classes import Pokemon, Team
from printouts import print_list, print_heading
from textManip import press_enter, confirm_close_string, select_number, clear

from dbInteraction import (
    get_player_names,
    get_team_names_from_player_name,
    get_team_names_from_version,
    get_team_from_db,
    get_existing_versions,
    add_team,
    update_team_name,
    update_pokemon_slot,
    update_moveset,
    update_single_move,
    get_all_team_names
)

from apiInteraction import (
    get_all_version_names,
    get_all_pokemon_in_dex,
    get_pokemon_moves
)

from constants import (
    CREATE_TEAM, VIEW_TEAMS, EDIT_TEAM, PLAYER, VERSION,
    CANCEL, QUIT, LIST, SINGLE, ALL, MOVES, STOP, NAME, POKEMON,
    VIEW_TITLE, MAIN_TITLE, CREATE_TITLE, EDIT_TITLE, INVALID, BACK
)

def menu(question: str, 
         options: dict, 
         choice_list: list = None, 
         list_heading: str = None,
         printing_list: str = None,
         list_heading_2: str = None,
         printing_list_2: str = None,
         title: str = None, 
         message: str = None,
         show_list: bool = False) -> str:
    while True:
        clear()
        if title:
            print_heading(title)
        if message:
            print("\n"+ message)
        if show_list and printing_list:
            print_list(printing_list, list_heading, True)
            if printing_list_2:
                print_list(printing_list_2, list_heading_2, True)
        print_heading(question)
        print("")
        for option in options:
            print(f"\t{option} - {options[option]}")
        response = input()
        if response in options: return response
        if len(response) == 1 and response != "[":
            for option in options:
                if option != None:
                    if response == option[0]:
                        return response
        if choice_list == None:
            return response
        if response not in choice_list:
            response = confirm_close_string(response, choice_list)
        return response

def main_menu(connection: Connection) -> None:
    current_message = None
    while True:
        user_input = menu("Select from the following options:",
                {CREATE_TEAM: "Create a new team",
                VIEW_TEAMS: "View all teams from a specific version, or by a specific player",
                EDIT_TEAM: "Edit an existing team",
                QUIT: "Quit the program"
                }, title = MAIN_TITLE,
                message = current_message)
        if user_input == CREATE_TEAM or user_input == "c":
            create_team(connection)
            current_message = None
        elif user_input == VIEW_TEAMS or user_input == "v":
            view_teams(connection)
            current_message = None
        elif user_input == EDIT_TEAM or user_input == "e":
            edit_team(connection)
            current_message = None
        elif user_input == QUIT or user_input == "q":
            break
        else:
            current_message = INVALID 
    return

def view_teams(connection: Connection):
    team = team_search(connection, VIEW_TITLE)
    print_team(team)
    
def print_team(team: Team) -> None:
    if team == None: return
    clear()
    team.printout()
    press_enter()
    
def team_search(connection: Connection, title_base: str) -> Team:
    existing_teams = get_all_team_names(connection)
    if len(existing_teams) == 0:
        print("No Teams were found. The database is currently empty.")
        press_enter()
        return None
    current_message = None
    list_flag = True
    while True:
        user_input = menu("Choose how you would like to search for teams:",
                {"[team name]": "Select a team by name",
                PLAYER: "Search for teams by a specific player",
                VERSION: "Search for teams from a specific game version",
                CANCEL: "Cancel and return to the main menu"
                },
                existing_teams,
                list_heading = "Existing Teams:",
                printing_list = existing_teams,
                title = title_base,
                message = current_message,
                show_list = list_flag)
        if user_input == PLAYER or user_input == "p":
            team = team_search_player(connection, title_base)
            return team
        elif user_input == VERSION or user_input == "v":
            team = team_search_version(connection, title_base)
            return team
        elif user_input == CANCEL or user_input == "c":
            return None
        elif user_input in existing_teams:
            team = import_team(connection, user_input)
            return team
        else:
            current_message = INVALID 

def team_search_player(connection: Connection, title_base: str) -> None:
    list_flag = True
    current_message = None
    existing_players = get_player_names(connection)
    if len(existing_players) == 0:
        print("No players were found. The database is currently empty.")
        press_enter()
        return None
    while True:
        chosen_player = menu("Enter the name of the player you would like to search for:",
                {"[player name]": "Type in a player's name to search for their teams",
                LIST: "Toggle list of all existing players",
                CANCEL: "Cancel and return to the main menu"
                },
                existing_players,
                list_heading = "Players",
                printing_list = existing_players,
                title = title_base,
                message = current_message,
                show_list = list_flag)
        if chosen_player == LIST or chosen_player == "l":
            list_flag = not list_flag
            current_message = None
        elif chosen_player == CANCEL or chosen_player == "c":
            return None
        elif chosen_player in existing_players:
            team = choose_team_by_player(connection, chosen_player, title_base)
            return team
        else:
            current_message = f"Sorry, there are no teams for '{chosen_player}'."
                
def choose_team_by_player(connection: Connection, player: str, title_base: str) -> None:
    list_flag = True
    current_message = None
    existing_teams = get_team_names_from_player_name(connection, player)
    while True:
        chosen_team = menu("Enter the name of the team you would like to select:",
                {"[team name]": "Type in a team name to select it",
                LIST: f"Toggle list of all of {player}'s teams",
                CANCEL: "Cancel and return to the main menu"
                },
                existing_teams,
                list_heading = f"{player}'s Teams:",
                printing_list = existing_teams,
                title = f"{title_base} - {player},",
                message = current_message,
                show_list = list_flag)
        if chosen_team == LIST or chosen_team == "l":
            list_flag = not list_flag
            current_message = None
        elif chosen_team == CANCEL or chosen_team == "c":
            return None
        elif chosen_team in existing_teams:
            team = import_team(connection, chosen_team)
            return team
        else:
            current_message = f"Sorry, there is no team called '{chosen_team}' for player '{player}'."
    
def team_search_version(connection: Connection, title_base: str) -> None:
    list_flag = True
    current_message = None
    existing_versions = get_existing_versions(connection)
    if len(existing_versions) == 0:
        print("No Teams were found. The database is currently empty.")
        press_enter()
        return None
    while True:
        chosen_version = menu("Enter the name of the version you would like to search for:",
                {"[version name]": "Type in a version name to search for its teams",
                LIST: f"Toggle list of all versions that have saved teams",
                CANCEL: "Cancel and return to the main menu"
                },
                existing_versions,
                list_heading = "Versions:",
                printing_list = existing_versions,
                title = title_base,
                message = current_message,
                show_list = list_flag)
        if chosen_version == LIST or chosen_version == "l":
            list_flag = not list_flag
            current_message = None
        elif chosen_version == CANCEL or chosen_version == "c":
            return None
        elif chosen_version in existing_versions: 
            team = choose_team_by_version(connection, chosen_version, title_base)
            return team
        else:
            current_message = f"Sorry, there are no teams for '{chosen_version}'."
            
def choose_team_by_version(connection: Connection, version: str, title_base: str) -> None:
    list_flag = True
    current_message = None
    existing_teams = get_team_names_from_version(connection, version)
    while True:
        chosen_team = menu("Enter the name of the team you would like to select:",
                {"[Team name]": "Type in a team name to select it",
                LIST: f"Toggle list of all teams for {version} version",
                CANCEL: "Cancel and return to the main menu"
                }, 
                existing_teams,
                list_heading = f"Teams for {version} version:",
                printing_list = existing_teams,
                title = f"{title_base} - {version}",
                message = current_message,
                show_list = list_flag)
        if chosen_team == LIST or chosen_team == "l":
            list_flag = not list_flag
            current_message = None
        elif chosen_team == CANCEL or chosen_team == "c":
            return None
        elif chosen_team in existing_teams: 
            team = import_team(connection, chosen_team)
            return team
        else:
            current_message = f"Sorry, there is no team called '{chosen_team}' for '{version}' version."
            
def import_team(connection: Connection, team_name: str):
    try:
        team = get_team_from_db(connection, team_name)
        return team
    except Exception as e:
        print(e)
        press_enter()
        return None
    
    
def create_team(connection: Connection) -> None:
    new_team = Team()
    title_base = CREATE_TITLE
    try:
        player_name = get_player_name(connection)
        new_team.set_player_name(player_name)
        
        version = choose_version()
        new_team.set_version(version)
        
        team_name = choose_team_name(connection, title_base)
        new_team.set_team_name(team_name)
        
        team_list = choose_team_pokemon(version, title_base)
        assign_pokemon(new_team, team_list)
        
        select_team_movesets(new_team)
        
        clear()
        print_heading(title_base)    
        new_team.printout()
        
        add_team(connection, new_team)
        press_enter()
        
    except Exception as e:
        print(e)
    
def get_player_name(connection: Connection) -> str:
    list_flag = True
    existing_names = get_player_names(connection)
    while True:
        player_name = menu("Please enter the name of the player who will use this team:",
                {"[player name]": "Select the name of the player for this team",
                LIST: "Toggle list of all existing players",
                CANCEL: "Cancel and return to the main menu"
                },
                list_heading = "Existing Players",
                printing_list = existing_names,
                title = f"{CREATE_TITLE} - Player Selection",
                show_list = list_flag)
        if player_name == LIST or player_name == "l":
            list_flag = not list_flag
        elif player_name == CANCEL or player_name == "c":
            raise Exception("")
        else:
            return player_name
    
def choose_version() -> str:
    list_flag = True
    current_message = None
    existing_versions = get_all_version_names()
    while True:
        version = menu("Please enter the game version for this team:",
                {"[version name]": "Select the version for this team",
                LIST: "Toggle list of versions",
                CANCEL: "Cancel and return to the main menu"
                },
                existing_versions,
                list_heading = "Game Versions:",
                printing_list = existing_versions,
                title = f"{CREATE_TITLE} - Version Selection",
                message = current_message,
                show_list = list_flag)
        if version == LIST or version == "l":
            list_flag = not list_flag
            current_message = None
        elif version == CANCEL or version == "c":
            raise Exception("")
        elif version in existing_versions:
            return version
        else:
            current_message = f"Sorry, '{version}' is not a valid Pokemon game version."
    
def choose_team_name(connection: Connection, title_base: str) -> str:
    list_flag = True
    current_message = None
    existing_names = get_all_team_names(connection)
    while True:
        team_name = menu("Please enter the name for this team:",
                {"[team name]": "Select a Team Name",
                LIST: f"Toggle list of existing team names",
                CANCEL: "Cancel and return to the last menu"
                },
                list_heading = f"Existing teams:",
                printing_list = existing_names,
                title = f"{title_base} - Team Name Selection",
                message = current_message,
                show_list = list_flag)
        if team_name == LIST or team_name == "l":
            list_flag = not list_flag
            current_message = None
        elif team_name == CANCEL or team_name == "c":
            raise Exception("")
        elif team_name in existing_names:
            current_message = "Sorry, that team name already exists."
        else:
            return team_name
        
def choose_team_pokemon(version: str, title_base: str):
    try:
        team_list = []
        clear()
        print_heading(f"{title_base} - Choose Team Size")
        slots = select_number(1, 6, "Please select the number of Pokemon you wish to add to your party (Between 1 and 6): ")
        message = None
        for i in range (slots):
            new_pokemon, message = choose_pokemon(version, i+1, title_base, team_list, message)
            team_list.append(new_pokemon)
        clear()
        print_heading(title_base)
        print_list(team_list, "Team:", True)
        press_enter()
        return team_list
    except Exception as e:
        raise(e)
            
def choose_pokemon(version: str, slot: int, title_base: str, team_list: list, current_message: str = None) -> tuple:
    full_title = f"{title_base} - Choose Pokemon"
    available_pokemon = get_all_pokemon_in_dex(version)
    list_flag = True
    while True:
        pokemon_name = menu(f"Please enter the pokemon to add to slot #{slot}:",
                {"[species name]": "Select the pokemon you want to add to the team",
                LIST: f"Toggle list of all pokemon for {version} version",
                CANCEL: "Cancel and return to the previous menu"
                },
                available_pokemon,
                list_heading = f"Available Pokemon in Pokemon {version} version:",
                printing_list = available_pokemon,
                list_heading_2 = "Pokemon Team:",
                printing_list_2 = team_list,
                title = full_title,
                message = current_message,
                show_list = list_flag)
        if pokemon_name == LIST or pokemon_name == "l":
            list_flag = not list_flag
            current_message = None
        elif pokemon_name == CANCEL or pokemon_name == "c":
            raise Exception("")
        elif pokemon_name in available_pokemon:
            return pokemon_name, f"Added {pokemon_name} to the team!"
        else:
            current_message = f"Sorry, '{pokemon_name}' is not a valid Pokemon in {version} version."

def assign_pokemon(new_team: Team, team_list: list) -> None:
    if len(team_list) == 0:
        raise Exception("No pokemon for team selected. Cancelling team creation.")
    for pokemon_name in team_list:
        new_pokemon = Pokemon(pokemon_name)
        new_team.set_pokemon(new_pokemon)
    return  

def select_team_movesets(team: Team) -> None:
    try:
        for pokemon in team.get_all_pokemon():
            if pokemon is None: return
            select_moveset(team.get_version(), pokemon, CREATE_TITLE)
            clear()
            print_list(pokemon.get_all_moves(), f"{pokemon.get_species()}'s moveset:")
            press_enter()
        return
    except Exception as e:
        raise(e)
    
def select_moveset(version: str, pokemon: Pokemon, title_base: str) -> bool:
    try:
        message = None
        name = pokemon.get_species()
        available_moves = get_pokemon_moves(version, name)
        max_moves = min(len(available_moves), 4)
        for i in range(1, max_moves + 1):
            still_adding, message = select_move(version, pokemon, i, title_base, message, available_moves)
            if not still_adding: break
    except Exception as e:
        raise(e)   
    
    
def select_move(version: str, pokemon: Pokemon, moveslot: int, title_base: str, current_message: str = None, available_moves: list = None) -> tuple:
    list_flag = True
    name = pokemon.get_species()
    if available_moves is None:
        available_moves = get_pokemon_moves(version, name)
    while True:
        selected_move = menu(f"Please enter move #{moveslot}:",
                {"[move name]": "Select the name of a move to add",
                LIST: f"Toggle list of all valid moves for {name}",
                STOP: f"Stop adding moves for this pokemon",
                CANCEL: "Cancel and return to the previous menu"
                },
                available_moves,
                list_heading = f"Available moves for {name} in {version} version:",
                printing_list = available_moves,
                list_heading_2 = f"{name}'s moveset:",
                printing_list_2 = pokemon.get_all_moves(),
                title = f"{title_base} - Selecting {name}'s Moves",
                message = current_message,
                show_list = list_flag)
        if selected_move == LIST or selected_move == "l":
            list_flag = not list_flag
            current_message = None
        elif selected_move == STOP or selected_move == "s":
            return False, current_message
        elif selected_move == CANCEL or selected_move == "c":
            raise Exception("")
        elif selected_move in available_moves:
            pokemon.change_move(moveslot, selected_move)
            available_moves.remove(selected_move)
            current_message = f"Added '{selected_move}' to {name}'s moveset "
            return True, current_message
        else:
            current_message = f"Sorry, '{selected_move}' is not a valid move to select."
    
def edit_team(connection: Connection) -> None:
    try:
        title_base = EDIT_TITLE
        team = team_search(connection, title_base)
        if team == None: return
        current_message = None 
        while True:
            user_input = menu("Choose what you would like to edit:",
                    {NAME: "Edit the team's name",
                    MOVES: "Edit a pokemon's moves",
                    POKEMON: "Change the pokemon on the team",
                    LIST: "Print out the team's details",
                    BACK: "Go back to the main menu"
                    }, title = title_base,
                    message = current_message)
            if user_input == NAME or user_input == "n":
                edit_team_name(connection, team)
                current_message = None 
            elif user_input == MOVES or user_input == "m":
                edit_pokemon_moves(connection, team)
                current_message = None 
            elif user_input == POKEMON or user_input == "p":
                edit_team_pokemon(connection, team)
                current_message = None 
            elif user_input == LIST or user_input == "l":
                print_team(team)
                current_message = None 
            elif user_input == BACK or user_input == "b":
                return
            else:
                current_message = INVALID
    except Exception as e:
        print(e)

def edit_team_name(connection: Connection, team: Team) -> None:
    title_base = EDIT_TITLE
    new_team_name = choose_team_name(connection, title_base)
    clear()
    print_heading(title_base)
    try:
        update_team_name(connection, team.get_team_id(), new_team_name)
        team.set_team_name(new_team_name)
        print(f"Team name changed to {new_team_name} successfully!")
    except Exception as e:
        print(e)
    press_enter()

def edit_pokemon_moves(connection: Connection, team: Team) -> None:
    title_base = EDIT_TITLE
    pokemon = select_pokemon_from_team(team, title_base)
    current_message = None 
    while True:
        user_input = menu("Would you like to change a single move, or the whole moveset?:",
                {SINGLE: "Change a single move",
                ALL: "Change all of a pokemon's moves",
                CANCEL: "Go back to the previous menu"
                }, title = f"{title_base} - Change Move",
                message = current_message)
        if user_input == SINGLE or user_input == "s":
            edit_one_move(connection, pokemon, team, title_base)
            return
        elif user_input == ALL or user_input == "a":
            edit_all_moves(connection, pokemon, team, title_base)
            return
        elif user_input == CANCEL or user_input == "c":
            return
        else:
            current_message = INVALID
            
def select_pokemon_from_team(team: Team, title_base: str) -> Pokemon:
    clear()
    print_heading(title_base)
    name_list = team.get_pokemon_name_list()
    for i in range(len(name_list)):
        print(f"{i+1}: {name_list[i]}")
    team_size = len(name_list)
    slot = select_number(1, team_size, f"Please select the pokemon (Between 1 and {team_size}): ")
    pokemon = team.get_pokemon_in_slot(slot)
    return pokemon
            
def edit_one_move(connection: Connection, pokemon: Pokemon, team: Team, title_base: str):
    title = f"{title_base} - Change Move"
    clear()
    print_heading(title)
    print_heading("Current Moves:")
    move_list = pokemon.get_all_moves()
    for i in range(len(move_list)):
        print(f"{i+1}: {move_list[i]}")
    num_moves = pokemon.get_num_moves()
    if num_moves < 4:
        num_moves += 1
        print(f"{num_moves}: Empty")
    moveslot = select_number(1, num_moves, f"Please select the move to change (Between 1 and {num_moves}): ")
    try:
        pokemon_slot = team.get_slot_number_for_pokemon(pokemon)
        if pokemon_slot == None:
            raise Exception("Error: Pokemon not found on team")
        select_move(team.get_version(), pokemon, moveslot, title_base)
        clear()
        print_heading(title)
        print_list(pokemon.get_all_moves(), f"{pokemon.get_species()}'s new moveset:")
        press_enter()
        update_single_move(connection, team.get_team_id(), pokemon, pokemon_slot, moveslot)
        clear()
        print_heading(title)
        print(f"Changed move successfully!")
        
    except Exception as e:
        if e.args[0] == "":
            raise(e)
        print(e)
    press_enter()
    
def edit_all_moves(connection: Connection, pokemon: Pokemon, team: Team, title_base: str):
    clear()
    title = f"{title_base} - Change Moveset"
    print_heading(title)
    try:
        pokemon_slot = team.get_slot_number_for_pokemon(pokemon)
        if pokemon_slot == None:
            raise Exception("Error: Pokemon not found on team")
        select_moveset(team.get_version(), pokemon, title_base)
        clear()
        print_heading(title)
        print_list(pokemon.get_all_moves(), f"{pokemon.get_species()}'s new moveset:")
        press_enter()
        update_moveset(connection, team.get_team_id(), pokemon, pokemon_slot)
        clear()
        print_heading(title)
        print(f"Changed moveset successfully!")
        
    except Exception as e:
        if e.args[0] == "":
            raise(e)
        print(e)
    press_enter()

def edit_team_pokemon(connection: Connection, team: Team) -> None:
    title_base = EDIT_TITLE
    clear()
    print_heading(f"{title_base} - Change Pokemon")
    name_list = team.get_pokemon_name_list()
    for i in range(len(name_list)):
        print(f"{i+1}: {name_list[i]}")
    team_size = len(name_list)
    if team_size < 6:
        team_size += 1
        print(f"{team_size}: Empty")
    slot = select_number(1, team_size, f"Please select the pokemon (Between 1 and {team_size}): ")
    try:
        new_pokemon, new_message = choose_pokemon(team.get_version(), slot, title_base, name_list)
        replacement = Pokemon(new_pokemon)
        select_moveset(team.get_version(), replacement, title_base)
        clear()
        print_list(replacement.get_all_moves(), f"{replacement.get_species()}'s moveset:")
        press_enter()
        
        update_pokemon_slot(connection, team.get_team_id(), replacement, slot)
        team.swap_pokemon(replacement, slot)
        clear()
        print_heading(f"{title_base} - Change Pokemon")
        print(f"Swapped {replacement.get_species()} into slot {slot} successfully!")
        
    except Exception as e:
        print(e)
    press_enter()
