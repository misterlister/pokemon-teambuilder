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