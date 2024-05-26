
def convert_generation_to_num(generation: str) -> int:
    i = generation.find("-")
    if i == -1:
        raise Exception(f"Error: Invalid generation format: {generation}")
    value = 0
    i += 1
    size = len(generation)
    while generation[i] == 'x':
        value += 10
        i += 1
        if i == size: return value
    if i < size -1:
        if generation[i] == 'i' and generation[i+1] == 'x':
            value += 9
            i += 2
            if i == size: return value
    if generation[i] == 'v':
        value += 5
        i += 1
        if i == size: return value
    if i < size -1:
        if generation[i] == 'i' and generation[i+1] == 'v':
            value += 4
            i += 2
            if i == size: return value
    while generation[i] == 'i':
        value += 1
        i += 1
        if i == size: return value
    return value

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
