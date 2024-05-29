from sqlite3 import Connection
from classes import Pokemon, Team
from printouts import print_list, print_heading, print_title
from textManip import press_enter, confirm_close_string, confirm, select_number, clear

from dbInteraction import (
    get_player_names,
    get_team_names_from_player_name,
    get_team_names_from_version,
    get_team_from_db,
    get_team_id_from_player,
    get_team_id_from_version,
    get_existing_versions,
    add_team
)

from apiInteraction import (
    get_all_version_names,
    get_all_pokemon_in_dex,
    get_pokemon_moves
)

from constants import (
    CREATE_TEAM, VIEW_TEAMS, PLAYER, VERSION,
    CANCEL, QUIT, LIST, EDIT, TEAM, MOVES, STOP, FINISH,
    VIEW_TITLE, MAIN_TITLE, CREATE_TITLE, EDIT_TITLE
)

def menu(question: str, options: dict, choice_list: list = None, title: str = None) -> str:
    while True:
        clear()
        if title:
            print_heading(title)
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
        if response in choice_list:
            return response
        response = confirm_close_string(response, choice_list)
        if response in choice_list:
            return response
        print("Invalid response, please try again.")
        press_enter

def main_menu(connection: Connection) -> None:
    while True:
        user_input = menu("Select from the following options:",
                {CREATE_TEAM: "Create a new team",
                VIEW_TEAMS: "View all teams from a specific version, or by a specific player",
                QUIT: "Quit the program"
                }, title = MAIN_TITLE)
        if user_input == CREATE_TEAM or user_input == "c":
            create_team(connection)
        elif user_input == VIEW_TEAMS or user_input == "v":
            view_teams(connection)
        elif user_input == QUIT or user_input == "q":
            break
        else:
            print("Sorry. That is not a valid command selection.")    
    return

def view_teams(connection: Connection):
    while True:
        user_input = menu("Choose how you would like to search for teams:",
                {PLAYER: "Search by the player's name",
                VERSION: "Search by the game version",
                CANCEL: "Cancel and return to the main menu"
                }, title = VIEW_TITLE)
        if user_input == PLAYER or user_input == "p":
            team_search_player(connection)
            return
        elif user_input == VERSION or user_input == "v":
            team_search_version(connection)
            return
        elif user_input == CANCEL or user_input == "c":
            return
        else:
            print("Sorry. That is not a valid command selection.")    

def team_search_player(connection: Connection) -> None:
    existing_players = get_player_names(connection)
    if len(existing_players) == 0:
        print("No Teams were found. The database is currently empty.")
        press_enter()
        return
    question = "Enter the name of the player you would like to search for:"
    while True:
        chosen_player = menu(question,
                {"[player name]": "Type in a player's name to search for their teams",
                LIST: "Print out a list of all existing players",
                CANCEL: "Cancel and return to the main menu"
                },
                existing_players,
                title = VIEW_TITLE)
        if chosen_player == LIST or chosen_player == "l":
            print_list(existing_players, "Players:", True)
            print_heading(question)
            chosen_player = input()
            if chosen_player not in existing_players:
                chosen_player = confirm_close_string(chosen_player, existing_players)
        if chosen_player == CANCEL or chosen_player == "c":
            return
        if chosen_player in existing_players:
            choose_team_by_player(connection, chosen_player)
            return
        print(f"Sorry, there are no teams for '{chosen_player}'.")
        press_enter()
                
def choose_team_by_player(connection: Connection, player: str) -> None:
    existing_teams = get_team_names_from_player_name(connection, player)
    question = "Enter the name of the team you would like to view:"
    while True:
        chosen_team = menu(question,
                {"[team name]": "Type in a team name to see its details",
                LIST: f"Print out a list of all of {player}'s teams",
                CANCEL: "Cancel and return to the main menu"
                },
                existing_teams,
                title = f"{VIEW_TITLE} - {player}")
        if chosen_team == LIST or chosen_team == "l":
            print_list(existing_teams, f"{player}'s Teams:", True)
            print_heading(question)
            chosen_team = input()
            if chosen_team not in existing_teams:
                chosen_team = confirm_close_string(chosen_team, existing_teams)
        if chosen_team == CANCEL or chosen_team == "c":
            return
        if chosen_team in existing_teams:
            try:
                team_id = get_team_id_from_player(connection, chosen_team, player)
                team = get_team_from_db(connection, team_id)
                team.printout()
                press_enter()
            except Exception as e:
                print(e)
            return
        print(f"Sorry, there is no team called '{chosen_team}' for player '{player}'.")
        press_enter()
    
                
def team_search_version(connection: Connection) -> None:
    existing_versions = get_existing_versions(connection)
    question = "Enter the name of the version you would like to search for:"
    if len(existing_versions) == 0:
        print("No Teams were found. The database is currently empty.")
        press_enter()
        return
    while True:
        chosen_version = menu(question,
                {"[version name]": "Type in a version name to search for its teams",
                LIST: f"Print out a list of all versions that have saved teams",
                CANCEL: "Cancel and return to the main menu"
                },
                existing_versions,
                title = VIEW_TITLE)
        if chosen_version == LIST or chosen_version == "l":
            print_list(existing_versions, "Versions:", True)
            print_heading(question)
            chosen_version = input()
            if chosen_version not in existing_versions:
                chosen_version = confirm_close_string(chosen_version, existing_versions)
        if chosen_version == CANCEL or chosen_version == "c":
            return
        if chosen_version in existing_versions: 
            choose_team_by_version(connection, chosen_version)
            return
        print(f"Sorry, there are no teams for '{chosen_version}'.")
        press_enter()
            
def choose_team_by_version(connection: Connection, version: str) -> None:
    existing_teams = get_team_names_from_version(connection, version)
    question = "Enter the name of the team you would like to view:"
    while True:
        chosen_team = menu(question,
                {"[Team name]": "Type in a team name to see its details",
                LIST: f"Print out a list of all teams for {version} version",
                CANCEL: "Cancel and return to the main menu"
                }, 
                existing_teams,
                title = f"{VIEW_TITLE} - {version}")
        if chosen_team == LIST or chosen_team == "l":
            print_list(existing_teams, f"Teams for {version} version:", True)
            print_heading(question)
            chosen_team = input()
            if chosen_team not in existing_teams:
                chosen_team = confirm_close_string(chosen_team, existing_teams)
        if chosen_team == CANCEL or chosen_team == "c":
            return
        if chosen_team in existing_teams: 
            try:
                team_id = get_team_id_from_version(connection, chosen_team, version)
                team = get_team_from_db(connection, team_id)
                team.printout()
                press_enter()
            except Exception as e:
                print(e)
            return
        print(f"Sorry, there is no team called '{chosen_team}' for '{version}' version.")
        press_enter()
    
                
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
        
        select_movesets(new_team)
            
        new_team.printout()
        add_team(connection, new_team)
        press_enter()
        
    except Exception as e:
        print(e)
    
def get_player_name(connection: Connection) -> str:
    existing_names = get_player_names(connection)
    question = "Please enter the name of the player who will use this team:"
    while True:
        player_name = menu(question,
                {"[player name]": "Select the name of the player for this team",
                LIST: "Print out a list of all existing players",
                CANCEL: "Cancel and return to the main menu"
                },
                title = f"{CREATE_TITLE} - Player Selection")
        if player_name == LIST or player_name == "l":
            print_list(existing_names, "Players:", True)
            print_heading(question)
            player_name = input()
        if player_name == CANCEL or player_name == "c":
            raise Exception("")
        else:
            return player_name
    
def choose_version() -> str:
    existing_versions = get_all_version_names()
    question = "Please enter the game version for this team:"
    while True:
        version = menu(question,
                {"[version name]": "Select the version for this team",
                LIST: "Print out a list of all versions",
                CANCEL: "Cancel and return to the main menu"
                },
                existing_versions,
                title = f"{CREATE_TITLE} - Version Selection")
        if version == LIST or version == "l":
            print_list(existing_versions, "Game versions:", True)
            print_heading(question)
            version = input()
            if version not in existing_versions:
                version = confirm_close_string(version, existing_versions)
        if version == CANCEL or version == "c":
            raise Exception("")
        if version in existing_versions:
            return version
        else:
            print(f"Sorry, '{version}' is not a valid Pokemon game version.")
            press_enter()
    
def choose_team_name(connection: Connection, version: str) -> str:
    existing_names = get_team_names_from_version(connection, version)
    question = "Please enter the name for this team:"
    while True:
        team_name = menu(question,
                {"[team name]": "Select a Team Name",
                LIST: f"Print out a list of all teams for {version} version",
                CANCEL: "Cancel and return to the main menu"
                },
                existing_names,
                title = f"{CREATE_TITLE} - Team Name Selection")
        if team_name == LIST or version == "l":
            print_list(existing_names, f"Teams from pokemon {version} version:", True)
            print_heading(question)
            team_name = input()
        if version == CANCEL or version == "c":
            raise Exception("")
        elif team_name in existing_names:
            print("Sorry, that team name already exists for this game.")
        else:
            return team_name
            
def choose_pokemon(version: str) -> list:
    team_list = []
    slots_filled = 0
    clear()
    menu_title = f"{CREATE_TITLE} - Choose Pokemon"
    print_title(menu_title)
    to_fill = select_number(1, 6, "Please select the number of Pokemon you wish to add to your party (Between 1 and 6): ")
    available_pokemon = get_all_pokemon_in_dex(version)
    while slots_filled < to_fill:
        question = f"Please enter the species name of pokemon #{slots_filled + 1}:"
        pokemon_name = menu(question,
                {"[species name]": "Select the pokemon you want to add to the team",
                LIST: f"Print out a list of all pokemon for {version} version",
                TEAM: "Print out a list of all pokemon selected for the team so far",
                CANCEL: "Cancel and return to the main menu"
                },
                available_pokemon,
                title = menu_title)
        if pokemon_name == LIST or pokemon_name == "l":
            print_list(available_pokemon, f"Available Pokemon in Pokemon {version} version:", True)
            print_heading(question)
            pokemon_name = input()
            if pokemon_name not in available_pokemon:
                pokemon_name = confirm_close_string(pokemon_name, available_pokemon)
        elif pokemon_name == TEAM or pokemon_name == "t":
            if len(team_list) > 0:
                print_list(team_list, "Team so far:", True)
            else:
                print("No pokemon added yet")
            print_heading(question)
            pokemon_name = input()
            if pokemon_name not in available_pokemon:
                pokemon_name = confirm_close_string(pokemon_name, available_pokemon)
        if pokemon_name == CANCEL or pokemon_name == "c":
            raise Exception("")
        if pokemon_name in available_pokemon:
            team_list.append(pokemon_name)
            slots_filled += 1
        else:
            print(f"Sorry, '{pokemon_name}' is not a valid Pokemon in {version} version.")
            press_enter()
    if len(team_list) > 0:
        clear()
        print_list(team_list, "Team:", True)
        press_enter()
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
        menu_title = f"{CREATE_TITLE} - Selecting {name}'s Moves"
        available_moves = get_pokemon_moves(version, name)
        max_moves = min(len(available_moves), 4)
        i = 1
        while i < max_moves + 1:
            question = f"Please enter move #{i}:"
            selected_move = menu(question,
                    {"[move name]": "Select the name of a move to add",
                    LIST: f"Print out a list of all valid moves for {name}",
                    MOVES: f"Print out a list of {name}'s moves so far",
                    STOP: f"Stop adding moves for this pokemon",
                    FINISH: f"Finish adding moves altogether",
                    CANCEL: "Cancel and return to the main menu"
                    },
                    available_moves,
                    title = menu_title)
            if selected_move == LIST or selected_move == "l":
                print_list(available_moves, f"Available moves for {name} in {version} version:", True)
                print_heading(question)
                selected_move = input()
                if selected_move not in available_moves:
                    selected_move = confirm_close_string(selected_move, available_moves)
            elif selected_move == MOVES or selected_move == "m":
                print_list(pokemon.get_all_moves(), f"{name}'s moveset:")
                print_heading(question)
                selected_move = input()
                if selected_move not in available_moves:
                    selected_move = confirm_close_string(selected_move, available_moves)
            if selected_move == STOP or selected_move == "s":
                break
            if selected_move == FINISH or selected_move == "f":
                return
            if selected_move == CANCEL or selected_move == "c":
                raise Exception("")
            if selected_move in available_moves:
                pokemon.set_move(selected_move)
                i += 1
                available_moves.remove(selected_move)
            else:
                print(f"Sorry, '{selected_move}' is not a valid move for {name} in {version} version.")
                press_enter()
        clear()
        print_list(pokemon.get_all_moves(), f"{name}'s moveset:")
        press_enter()
    return
        
def edit_team():
    pass
