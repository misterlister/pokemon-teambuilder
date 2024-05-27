from sqlite3 import Connection
from editTeams import (
    create_team,
    edit_team
)

from dbInteraction import (
    get_player_names,
    get_team_names_from_player_name,
    get_team_names_from_version,
    get_team_from_db,
    get_team_id_from_player,
    get_team_id_from_version,
    get_existing_versions
)

from printouts import print_list

from textManip import press_enter, get_close_string, confirm

from constants import (
    MDBORDER, SMBORDER,
    CREATE_TEAM, VIEW_TEAMS, PLAYER, VERSION,
    CANCEL, QUIT, LIST
)

def main_menu(connection: Connection) -> None:
    while True:
        print(f"""
    {MDBORDER}
    Select from the following options (Enter the first letter or whole word):
    {MDBORDER}
        {SMBORDER}
        {CREATE_TEAM} - Create a new team
        {VIEW_TEAMS} - View all teams from a specific version, or by a specific player
        {QUIT} - Quit the program
        {SMBORDER}
            """)
        user_input = input().strip().lower()
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
        user_input = input(f"""
    {MDBORDER}
    Choose how you would like to search for teams: 
    (Enter the first letter or whole word):
    {MDBORDER}
        {SMBORDER}
        {PLAYER} - Search by the player's name
        {VERSION} - Search by the game version
        {CANCEL} - Cancel and return to the main menu
        {SMBORDER}
""").strip().lower()
        if user_input == PLAYER or user_input == "p":
            team_search_player(connection)
            break
        elif user_input == VERSION or user_input == "v":
            team_search_version(connection)
            break
        elif user_input == CANCEL or user_input == "c":
            break
        else:
            print("Sorry. That is not a valid command selection.")    
    return

def team_search_player(connection: Connection) -> None:
    existing_players = get_player_names(connection)
    if len(existing_players) == 0:
        print("No Teams were found. The database is currently empty.")
        return
    while True:
        chosen_player = input(f"""
    {MDBORDER}
    Enter the name of the player you would like to search for (eg. 'Ash'). 
    {MDBORDER}
        {SMBORDER}
        {LIST} - Print out a list of all existing players
        [player name] - Type in a player's name to search for their teams
        {CANCEL} - Cancel and return to the main menu
        {SMBORDER}
""")
        if chosen_player == LIST or chosen_player == "l":
            print_list(existing_players, "Players:")
            press_enter()
        elif chosen_player == CANCEL or chosen_player == "c":
            return
        else:
            if chosen_player in existing_players:
                break
            close_string = get_close_string(chosen_player, existing_players)
            if close_string != None:
                if confirm(f"Did you mean '{close_string}'?"):
                    chosen_player = close_string
                    break
            print(f"Sorry, there are no teams for '{chosen_player}'.")
                
    choose_team_by_player(connection, chosen_player)
    
def choose_team_by_player(connection: Connection, player: str) -> None:
    existing_teams = get_team_names_from_player_name(connection, player)
    while True:
        chosen_team = input(f"""
    {MDBORDER}
    Enter the name of the team you would like to view (eg. 'Classic Team'). 
    {MDBORDER}
        {SMBORDER}
        {LIST} - Print out a list of all of {player}'s teams
        [team name] - Type in a team name to see its details
        {CANCEL} - Cancel and return to the main menu
        {SMBORDER}
""")
        if chosen_team == LIST or chosen_team == "l":
            print_list(existing_teams, f"{player}'s Teams:")
            press_enter()
        elif chosen_team == CANCEL or chosen_team == "c":
            return
        else:
            if chosen_team in existing_teams:
                break
            close_string = get_close_string(chosen_team, existing_teams)
            if close_string != None:
                if confirm(f"Did you mean '{close_string}'?"):
                    chosen_team = close_string
                    break
            print(f"Sorry, there is no team called '{chosen_team}' for player '{player}'.")
            
    try:
        team_id = get_team_id_from_player(connection, chosen_team, player)
        team = get_team_from_db(connection, team_id)
        team.printout()
        press_enter()
    except Exception as e:
        print(e)
                
def team_search_version(connection: Connection) -> None:
    existing_versions = get_existing_versions(connection)
    if len(existing_versions) == 0:
        print("No Teams were found. The database is currently empty.")
        return
    while True:
        chosen_version = input(f"""
    {MDBORDER}
    Enter the name of the version you would like to search for (eg. 'red'). 
    {MDBORDER}
        {SMBORDER}
        {LIST} - Print out a list of all versions that have saved teams
        [version name] - Type in a version name to search for its teams
        {CANCEL} - Cancel and return to the main menu
        {SMBORDER}
""").strip().lower()
        if chosen_version == LIST or chosen_version == "l":
            print_list(existing_versions, "Versions:")
            press_enter()
        elif chosen_version == CANCEL or chosen_version == "c":
            return
        else:
            if chosen_version in existing_versions: 
                break
            close_string = get_close_string(chosen_version, existing_versions)
            if close_string != None:
                if confirm(f"Did you mean '{close_string}'?"):
                    chosen_version = close_string
                    break
            print(f"Sorry, there are no teams for '{chosen_version}'.")
            
    choose_team_by_version(connection, chosen_version)

                
                
def choose_team_by_version(connection: Connection, version: str) -> None:
    existing_teams = get_team_names_from_version(connection, version)
    while True:
        chosen_team = input(f"""
    {MDBORDER}
    Enter the name of the team you would like to view (eg. 'Classic Team'). 
    {MDBORDER}
        {SMBORDER}
        {LIST} - Print out a list of all teams for {version} version
        [team name] - Type in a team name to see its details
        {CANCEL} - Cancel and return to the main menu
        {SMBORDER}
""")
        if chosen_team == LIST or chosen_team == "l":
            print_list(existing_teams, f"Teams for {version} version:")
            press_enter()
        elif chosen_team == CANCEL or chosen_team == "c":
            return
        else:
            if chosen_team in existing_teams: 
                break
            close_string = get_close_string(chosen_team, existing_teams)
            if close_string != None:
                if confirm(f"Did you mean '{close_string}'?"):
                    chosen_team = close_string
                    break
            print(f"Sorry, there is no team called '{chosen_team}' for '{version}' version.")
    try:
        team_id = get_team_id_from_version(connection, chosen_team, version)
        team = get_team_from_db(connection, team_id)
        team.printout()
        press_enter()
    except Exception as e:
        print(e)
                