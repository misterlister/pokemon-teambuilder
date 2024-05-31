"""
Contains unittests for various functions in the application.
"""

import unittest

from textManip import (
    get_close_string
)

from apiInteraction import (
    get_pokemon_moves,
    get_version_group,
    get_all_types,
)

from textManip import (
    convert_generation_to_num
)

class Tests(unittest.TestCase):

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

    def test_get_close_string_1(self):
        string = "pikochu"
        string_list = ["pichu", "pikachu", "raichu"]
        close_string = get_close_string(string, string_list)
        self.assertEqual(
            close_string, "pikachu"
        )

    def test_get_close_string_2(self):
        string = "pokocho"
        string_list = ["pichu", "pikachu", "raichu"]
        close_string = get_close_string(string, string_list)
        self.assertEqual(
            close_string, "pikachu"
        )

    def test_get_close_string_3(self):
        string = "tokocho"
        string_list = ["pichu", "pikachu", "raichu"]
        close_string = get_close_string(string, string_list)
        self.assertEqual(
            close_string, None
        )

    def test_get_close_string_4(self):
        string = ""
        string_list = ["pichu", "pikachu", "raichu"]
        close_string = get_close_string(string, string_list)
        self.assertEqual(
            close_string, None
        ) 

    def test_get_close_string_5(self):
        string = "zapcannon"
        string_list = ["zap-cannon"]
        close_string = get_close_string(string, string_list)
        self.assertEqual(
            close_string, "zap-cannon"
        ) 

    def test_convert_gen_to_num_1(self):
        gen = "generation-i"
        num = convert_generation_to_num(gen)
        self.assertEqual(
            num, 1
        ) 

    def test_convert_gen_to_num_3(self):
        gen = "generation-iii"
        num = convert_generation_to_num(gen)
        self.assertEqual(
            num, 3
        ) 

    def test_convert_gen_to_num_4(self):
        gen = "generation-iv"
        num = convert_generation_to_num(gen)
        self.assertEqual(
            num, 4
        ) 

    def test_convert_gen_to_num_6(self):
        gen = "generation-vi"
        num = convert_generation_to_num(gen)
        self.assertEqual(
            num, 6
        ) 

    def test_convert_gen_to_num_9(self):
        gen = "generation-ix"
        num = convert_generation_to_num(gen)
        self.assertEqual(
            num, 9
        ) 

    def test_convert_gen_to_num_11(self):
        gen = "generation-xi"
        num = convert_generation_to_num(gen)
        self.assertEqual(
            num, 11
        ) 

    def test_get_all_types_gen1(self):
        version = "red"
        types = get_all_types(version)
        self.assertEqual(
            len(types), 15
        )

    def test_get_all_types_gen2(self):
        version = "crystal"
        types = get_all_types(version)
        self.assertEqual(
            len(types), 17
        )

    def test_get_all_types_gen5(self):
        version = "black"
        types = get_all_types(version)
        self.assertEqual(
            len(types), 17
        )

    def test_get_all_types_gen6(self):
        version = "x"
        types = get_all_types(version)
        self.assertEqual(
            len(types), 18
        )

    def test_get_all_types_gen9(self):
        version = "violet"
        types = get_all_types(version)
        self.assertEqual(
            len(types), 19
        )

if __name__ == "__main__":
    unittest.main()
