import unittest

from apiInteraction import (
    get_all_version_names,
    get_all_pokemon_in_dex,
    get_pokedex_url,
    get_pokemon_moves,
    get_version_group,
    add_move_by_version,
    move_version_is_valid
)

class Tests(unittest.TestCase):
    def test_get_all_version_names(self):
        version_names = get_all_version_names()
        self.assertEqual(
            version_names, [
                "red", "blue", "yellow", 
                "gold", "silver", "crystal",
                "ruby", "sapphire", "emerald", "firered", "leafgreen",
                "diamond", "pearl", "platinum", "heartgold", "soulsilver",
                "black", "white", "colosseum", "xd", "other"
            ]
        )
        
    def test_get_version_group_red(self):
        version_group = get_version_group("red")
        self.assertEqual(
            version_group, "red-blue"
        )
        
    def test_get_version_group_yellow(self):
        version_group = get_version_group("yellow")
        self.assertEqual(
            version_group, "yellow"
        )
    
    def test_get_version_group_heartgold(self):
        version_group = get_version_group("heartgold")
        self.assertEqual(
            version_group, "heartgold-soulsilver"
        )
        
    def test_get_version_group_xd(self):
        version_group = get_version_group("xd")
        self.assertEqual(
            version_group, "xd"
        )
        
    def test_get_pokemon_moves(self):
        moves = get_pokemon_moves("red", "pikachu")
        self.assertEqual(
            moves, [
                "mega-punch",
                "pay-day",
                "mega-kick",
                "body-slam",
                "take-down",
                "double-edge",
                "growl",
                "surf",
                "submission",
                "seismic-toss",
                "thunder-shock",
                "thunderbolt",
                "thunder-wave",
                "thunder",
                "toxic",
                "agility",
                "quick-attack",
                "rage",
                "mimic",
                "double-team",
                "reflect",
                "bide",
                "swift",
                "skull-bash",
                "flash",
                "rest",
                "substitute"
            ]
        )
    
if __name__ == "__main__":
    unittest.main()