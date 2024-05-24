import unittest

from apiInteraction import (
    get_all_version_names,
    get_all_pokemon_in_dex
)

class Tests(unittest.TestCase):
    version = 'red'
    pokemon_list = get_all_pokemon_in_dex(version)
    print(pokemon_list)
    
if __name__ == "__main__":
    unittest.main()