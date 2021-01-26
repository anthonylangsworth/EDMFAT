import requests

from .state import StarSystem

def resolve_star_system_via_edsm(system_address:int) -> StarSystem:
    URL = "https://www.edsm.net/api-system-v1/factions"
    star_system = None

    post = {
        "systemId": system_address
    }
    response = requests.post(URL, json=post)
    if response.status_code == 200:
        output = response.json()
        minor_factions = [faction["name"] for faction in output["factions"]]
        star_system = StarSystem(response.name, system_address, minor_factions) 
    return star_system
