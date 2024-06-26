"""
Contains functions dealing with interacting with the pokeapi API.
"""

import requests
from constants import (
    BASEURL,
    XD_MONS,
    COLOSSEUM_MONS
    )

from text_manip import (
    convert_generation_to_num
    )

def get_all_version_names() -> list:
    url = f"{BASEURL}version"
    version_names = get_all_version_names_r(url)
    if version_names is not None:
        version_names.append("other")
    return version_names

def get_all_version_names_r(url: str) -> list:
    response = requests.get(url)
    version_names = []

    if response.status_code == 200:
        data = response.json()
        versions = data["results"]
        version_names = [version["name"] for version in versions]
        if data["next"] is not None:
            version_names.extend(get_all_version_names_r(data["next"]))
        return version_names

    print(f"Failed to fetch data: {response.status_code}")
    return None

def get_all_pokemon_in_dex(version: str) -> list:
    if version == "other":
        pokedex_url = f"{BASEURL}pokedex/1"
    elif version == "colosseum":
        return COLOSSEUM_MONS
    elif version == "xd":
        return XD_MONS
    else:
        pokedex_url = get_pokedex_url(version)
        if pokedex_url is None:
            return None

    response = requests.get(pokedex_url)

    if response.status_code == 200:
        data = response.json()
        pokedex = data["pokemon_entries"]
        pokemon_list = [pokemon_entry["pokemon_species"]["name"] for pokemon_entry in pokedex]
        return pokemon_list

    print(f"Failed to fetch data: {response.status_code}")
    return None

def get_pokedex_url(version: str) -> str:
    version_group = get_version_group(version)
    if version_group is None:
        return None

    response = requests.get(f"{BASEURL}version-group/{version_group}")

    if response.status_code == 200:
        data = response.json()
        pokedex_url = data["pokedexes"][0]["url"]
        return pokedex_url

    print(f"Failed to fetch data: {response.status_code}")
    return None

def get_pokemon_moves(version: str, name: str) -> list:
    version_group = get_version_group(version)
    if version_group is None:
        return None
    url = f"{BASEURL}pokemon/{name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        moves = data["moves"]
        move_list = []
        for move in moves:
            add_move_by_version(move_list, move, version_group)
        return move_list

    print(f"Failed to fetch data: {response.status_code}")
    return None

def get_version_group(version: str) -> str:
    url = f"{BASEURL}version/{version}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        version_group = data["version_group"]["name"]
        return version_group

    print(f"Failed to fetch data: {response.status_code}")
    return None

def add_move_by_version(movelist: list, move: str, version_group: str) -> None:
    move_name = move["move"]["name"]
    if move_version_is_valid(move["version_group_details"], version_group):
        movelist.append(move_name)

def move_version_is_valid(move_version_groups: list, version_group: str) -> bool:
    for entry in move_version_groups:
        if entry["version_group"]["name"] == version_group:
            return True
    return False

def get_version_generation(version: str) -> int:
    version_group = get_version_group(version)
    url = f"{BASEURL}version-group/{version_group}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        generation = data["generation"]["name"]
        gen_num = convert_generation_to_num(generation)
        return gen_num

    print(f"Failed to fetch data: {response.status_code}")
    return None

def get_all_types(version: str) -> list:
    gen_num = get_version_generation(version)
    url = f"{BASEURL}type"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        type_data = data["results"]
        types = [type["name"] for type in type_data]

        types.remove("unknown")
        if gen_num < 9:
            types.remove("stellar")
        if gen_num < 6:
            types.remove("fairy")
        if gen_num < 2:
            types.remove("steel")
            types.remove("dark")
        return types
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

"""
def get_pokemon_team_types(team_list, version: str):
    gen_num = get_version_generation(version)
    if version is None: return None
    for pokemon in team_list:
        pass
"""
