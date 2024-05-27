from sqlite3 import Connection
from editTeams import (
    create_team,
    edit_team
)

from constants import (
    LGBORDER,
    MDBORDER,
    SMBORDER,
    CREATE_TEAM,
    VIEW_TEAMS,
    PLAYER,
    VERSION,
    CANCEL,
    QUIT
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
        print(f"""
    {MDBORDER}
    Choose how you would like to search for teams (Enter the first letter or whole word):
    {MDBORDER}
        {SMBORDER}
        {PLAYER} - Search by the player's name
        {VERSION} - Search by the game version
        {CANCEL} - Cancel and return to the main menu
        {SMBORDER}
              """)
        user_input = input().strip().lower()
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

def team_search_player(connection: Connection):
    print("Player Search!")
    press_enter()
    pass

def team_search_version(connection: Connection):
    print("Version Search!")
    press_enter()
    pass

def press_enter() -> None:
    input("Press Enter to continue ")