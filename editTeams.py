from dbInteraction import (
    get_player_names, 
    get_team_names_from_version
    )
from apiInteraction import (
    get_all_version_names,
    get_all_pokemon_in_dex,
    get_pokemon_moves
)

def create_team(connection):
    player_name = get_player_name(connection)
    if player_name is None: return
    version = choose_version()
    if version is None: return
    teamName = choose_team_name(connection, version)
    if teamName is None: return
    pokemon_team = choose_pokemon(version)
    if confirm("Would you like to set the team's movesets?"):
        select_movesets(pokemon_team, version)
    
def get_player_name(connection):
    valid = False
    existing_names = get_player_names(connection)
    while not valid:
        team_name = input("Please enter the name of the player who will use this team (eg. 'Ash'). Type 'list' to see all existing names: ")
        if team_name == "list":
                print_list(existing_names)
        else:
            return team_name
    
def choose_version():
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
                print("Sorry, '{version}' is not a valid Pokemon game version.")
                if not confirm("Would you like to try again?"):
                    return None
        else:
            return version
    
def choose_team_name(connection, version):
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
                print_team(team)
            else:
                close_string = get_close_string(pokemon_name, available_pokemon)
                if close_string != None:
                    if confirm(f"Did you mean '{close_string}'?"):
                        team.append({"name": close_string})
                        party_full += 1
                        if party_full == entries:
                            print_team(team)
                        continue
                print(f"Sorry, '{pokemon_name}' is not a valid Pokemon in {version} version.")
                if not confirm("Would you like to try again?"):
                    return None
        else:
            team.append({"name": pokemon_name})
            party_full += 1
            if party_full == entries:
                print_team(team)
    return team

def select_movesets(team, version):
    for pokemon in team:
        name = pokemon["name"]
        pokemon["moves"] = []
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
                            pokemon["moves"].append(close_string)
                            i += 1
                            continue
                    print(f"Sorry, '{selected_move}' is not a valid move for {name} in {version} version.")
                    if not confirm("Would you like to try again?"):
                        return
            else:
                pokemon["moves"].append(selected_move)
                i += 1
        print(f"{name}'s moveset:")
        print_list(pokemon["moves"])
    return
        
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
        
def print_team(team):
    pokemon_names = []
    for pokemon in team:
        pokemon_names.append(pokemon["name"])
    print("\nTeam:")
    print_list(pokemon_names)
        
def select_number(low, high, question):
    valid = False
    while not valid:
        input_num = input(question)
        if input_num.isdigit():
            input_num = int(input_num)
            if input_num > low and input_num < high:
                return input_num
        print(f"Please enter a number between {low} and {high}")

def get_close_string(orig_string, string_list):
    closest_match = None
    max_matches = 0
    orig_len = len(orig_string)
    if orig_len == 0: return None
    for string in string_list:
        string_len = len(string)
        if string_len > 0:
            i = 0
            match_count = 0
            
            for j in range (string_len):
                matched = False
                if i >= orig_len: break
                if orig_string[i] == string[j]:
                    i += 1
                    matched = True
                if not matched and i + 1 < orig_len:
                    if orig_string[i+1] == string[j]:
                        i += 2
                        matched = True
                if not matched and j + 1 < string_len:
                    if orig_string[i] == string[j+1]:
                        i += 1
                        j += 1
                        matched = True
                if matched: match_count += 1
                else: i += 1
                        
            if match_count > max_matches:
                max_matches = match_count
                closest_match = string
    if max_matches > (len(closest_match)) / 2:
        return closest_match
    return None

        
                        
            
        


        
