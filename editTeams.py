from dbInteraction import (
    get_player_names, 
    get_team_names_from_version
    )
from apiInteraction import (
    get_all_version_names,
    get_all_pokemon_in_dex
)

def create_team(connection):
    player_name = get_player_name(connection)
    if player_name is None: return
    version = choose_version()
    if version is None: return
    teamName = choose_team_name(connection, version)
    if teamName is None: return
    pokemon_team = choose_pokemon(version)
    
def get_player_name(connection):
    valid = False
    existing_names = get_player_names(connection)
    while not valid:
        team_name = input("Please enter the name of the player who will use this team (eg. 'Ash'). Type 'list' to see all existing names: ")
        if team_name == "list":
                print_list(existing_names)
        elif team_name in existing_names:
            print("Sorry. That team name already exists for this game.")
            if not confirm("Would you like to try again?"):
                return None
        else:
            #if confirm(f"You entered the name: '{team_name}'. Is this correct?"):
                #print("")
            return team_name
    
def choose_version():
    valid = False
    versions = get_all_version_names()
    versions.append("other")
    while not valid:
        version = input("Please enter the game version for this team (eg. red). Type 'list' to see all options: ")
        version = version.lower()
        if version not in versions:
            if version == "list":
                print_list(versions)
            else:
                print("Sorry. That is not a valid Pokemon game version.")
                if not confirm("Would you like to try again?"):
                    return None
        else:
            #if confirm(f"You selected: '{version}' version. Is this correct?"):
                #print("")
            return version
    
def choose_team_name(connection, version):
    valid = False
    existing_names = get_team_names_from_version(connection, version)
    while not valid:
        team_name = input("Please enter the name for this team (eg. 'ruby team'). Type 'list' to see all existing names: ")
        if team_name == "list":
                print_list(existing_names)
        elif team_name in existing_names:
            print("Sorry. That team name already exists for this game.")
            if not confirm("Would you like to try again?"):
                return None
        else:
            #if confirm(f"You entered the name: '{team_name}'. Is this correct?"):
                #print("")
            return team_name
            
def choose_pokemon(version):
    team = []
    party_full = 0
    entries = select_number(1, 6, "Please select the number of Pokemon you wish to add to your party (Between 1 and 6): ")
    available_pokemon = get_all_pokemon_in_dex(version)
    while party_full < entries:
        pokemon_name = input(f"Please enter the species name of pokemon #{party_full + 1} (eg. pikachu). Type 'list' to see all options: ")
        pokemon_name = pokemon_name.lower()
        if pokemon_name not in available_pokemon:
            if pokemon_name == "list":
                print(f"Available Pokemon in Pokemon {version} version:\n")
                print_list(available_pokemon)
                print("\nTeam:")
                print_list(team)
                print("")
            else:
                print(f"Sorry. That is not a valid Pokemon in {version} version.")
                if not confirm("Would you like to try again?"):
                    return None
        else:
            #if confirm(f"You selected: '{pokemon_name}'. Is this correct?"):
                #print("")
            team.append(pokemon_name)
            party_full += 1
            if party_full == entries:
                print("\nTeam:")
                print_list(team)
                print("")
    return team
        
def edit_team():
    pass

def print_list(list):
    max_size = 1
    if len(list) == 0:
        print("No data exists")
        return
    for item in list:
        if len(item) > max_size:
            max_size = len(item) + 1
    items_per_line = int(90 / max_size)
    for i in range(len(list)):
        if i % items_per_line == 0:
            print("")
        print(f"{list[i].ljust(max_size, " ")} ", end="")
    print("\n")

def confirm(question):
    valid = False
    while not valid:
        response = input(f"{question} Yes/No: ")
        response = response.lower()
        if response == "yes" or response == 'y':
            return True
        if response == "no" or response == 'n':
            return False
        print("Invalid response, please try again.")
        
def select_number(low, high, question):
    valid = False
    while not valid:
        input_num = input(question)
        if input_num.isdigit():
            input_num = int(input_num)
            if input_num > low and input_num < high:
                return input_num
        print(f"Please enter a number between {low} and {high}")

                


        
