import requests
from constants import BASEURL

def get_all_version_names():
    url = f"{BASEURL}version"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        versions = data['results']
        version_names = [version['name'] for version in versions]
        return version_names
    else:
        print(f"Failed to fetch data: {response.status_code}")
        
def get_all_pokemon_in_dex(version):
    if version == "other":
        pokedex_url = f"{BASEURL}pokedex/1"
    else:
        region_url = f"{BASEURL}version/{version}"
        response = requests.get(region_url)
    
        if response.status_code == 200:
            data = response.json()
            version_group_url = data['version_group']['url']
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
        
        response = requests.get(version_group_url)
    
        if response.status_code == 200:
            data = response.json()
            pokedex_url = data['pokedexes'][0]['url']
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
        
    response = requests.get(pokedex_url)    
            
    if response.status_code == 200:
        data = response.json()
        pokedex = data['pokemon_entries']
        pokemon_list = [pokemon_entry['pokemon_species']['name'] for pokemon_entry in pokedex]
        return pokemon_list
    else:
        print(f"Failed to fetch data: {response.status_code}")