from printouts import print_list, print_title

class Pokemon():
    def __init__(self, 
                 species_name,
                 move1 = None,
                 move2 = None,
                 move3 = None,
                 move4 = None) -> None:
        self.species_name = species_name
        self.moves = []
        self.moves.append(move1)
        self.moves.append(move2)
        self.moves.append(move3)
        self.moves.append(move4)
        
    def get_species(self) -> str:
        return self.species_name
    
    def get_all_moves(self) -> list:
        return self.moves
    
    def get_move_in_slot(self, number: int) -> str:
        if number > 4 or number <= 0:
            raise ValueError(f"Error: Invalid move number '{number}'.")
        return self.moves[number - 1]
    
    def get_num_moves(self) -> int:
        size = 0
        for slot in self.moves:
            if slot is not None:
                size += 1
        return size
    
    def set_move(self, new_move: str) -> None:
        for i in range (len(self.moves)):
            if self.moves[i] == None:
                self.moves[i] = new_move
                return
        raise Exception(f"Error: All moves have already been selected.")
    
    def reset_moves(self) -> None:
        for i in range (len(self.moves)):
            self.moves[i] = None
        return
    
    def change_move(self, number: int, new_move: str) -> None:
        if number > 4 or number <= 0:
            raise ValueError(f"Error: Invalid move number '{number}'.")
        elif self.get_num_moves() < 4:
            self.set_move(new_move)
        else:
            self.moves[number - 1] = new_move
        
    def printout(self) -> None:
        print_list(self.moves, self.species_name, True)
        

class Team():
    def __init__(self, 
                 player_name: str = None,
                 team_name: str = None,
                 version: str = None,
                 pokemon1: Pokemon = None,
                 pokemon2: Pokemon = None,
                 pokemon3: Pokemon = None,
                 pokemon4: Pokemon = None,
                 pokemon5: Pokemon = None,
                 pokemon6: Pokemon = None,
                 team_id: int = None
                 ) -> None:
        self.player_name = player_name
        self.team_name = team_name
        self.version = version
        self.pokemon = []
        self.pokemon.append(pokemon1)
        self.pokemon.append(pokemon2)
        self.pokemon.append(pokemon3)
        self.pokemon.append(pokemon4)
        self.pokemon.append(pokemon5)
        self.pokemon.append(pokemon6)
        self.team_id = team_id
        
    def get_player_name(self) -> str:
        return self.player_name
    
    def get_team_name(self) -> str:
        return self.team_name
    
    def get_version(self) -> str:
        return self.version
    
    def get_team_size(self) -> str:
        size = 0
        for slot in self.pokemon:
            if slot is not None:
                size += 1
        return size
    
    def get_all_pokemon(self) -> list:
        return self.pokemon
    
    def get_pokemon_name_list(self) -> list:
        name_list = []
        for slot in self.pokemon:
            if slot != None:
                name_list.append(slot.get_species())
        return name_list
    
    def get_pokemon_in_slot(self, number: int) -> str:
        if number > 6 or number <= 0:
            raise ValueError(f"Error: Invalid pokemon number '{number}'.")
        return self.pokemon[number - 1]
    
    def get_slot_number_for_pokemon(self, check_pokemon: Pokemon) -> int:
        for i in range (len(self.pokemon)):
            if self.pokemon[i] == check_pokemon:
                return i+1
        return None
    
    def get_team_id(self) -> int:
        return self.team_id
        
    def set_player_name(self, player_name: str) -> None:
        self.player_name = player_name
        
    def set_team_name(self, team_name: str) -> None:
        self.team_name = team_name
        
    def set_version(self, version: str) -> None:
        if self.version is None:
            self.version = version
        else:
            raise Exception("Error: you cannot change the version of an existing team")
            
    def set_pokemon(self, new_pokemon: Pokemon) -> None:
        for i in range(len(self.pokemon)):
            if self.pokemon[i] is None:
                self.pokemon[i] = new_pokemon
                return
        raise Exception(f"Error: Pokemon roster is already full.")
        
    def swap_pokemon(self, new_pokemon: Pokemon, slot_number: int) -> None:
        if slot_number > 6 or slot_number <= 0:
            raise ValueError(f"Error: Invalid pokemon number '{slot_number}'.")
        elif self.get_team_size() < 6:
            self.set_pokemon(new_pokemon)
        else:
            self.pokemon[slot_number - 1] = new_pokemon
            
    def set_team_id(self, team_id: int) -> None:
        if self.team_id is None:
            self.team_id = team_id
        else:
            raise Exception("Error: you cannot change the team ID of an existing team")
        
    def printout(self) -> None:
        print_title(f"Team {self.team_name}:")
        print(f"Player: {self.player_name}")
        print(f"Version: {self.version}")
        for slot in self.pokemon:
            if slot is not None:
                slot.printout()
            
class DatabaseInsertionError(Exception):
    pass