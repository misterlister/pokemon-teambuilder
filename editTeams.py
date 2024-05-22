import requests
from constants import BASEURL
import sqlite3

def create_team():
    valid = False
    versions = get_all_version_names()
    while not valid:
        version = input("Please enter the game version for this team (eg. red): ")
        version = version.lower()
        if version not in versions:
            print("Sorry. That is not a valid Pokemon game version.")
            if not confirm("Would you like to try again?"):
                return
        else:
            print(f"Creating a new team for Pokemon {version} version!")
            valid = True

def edit_team():
    pass

def confirm(question):
    valid = False
    while not valid:
        response = input(f"{question} Yes/No: ")
        response = response.lower()
        if response == "yes":
            return True
        if response == "no":
            return False
        print("Invalid response, please try again.")
        

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
