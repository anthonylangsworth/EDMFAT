import requests

from .state import StarSystem

def resolve_star_system_via_edsm(system_address:int) -> StarSystem:
    URL = "https://www.edsm.net/api-system-v1/factions"
    star_system = None
    response = requests.get(URL, params={ "systemId64": system_address })
    if response.status_code == 200:
        output = response.json()
        minor_factions = [faction["name"] for faction in output["factions"]]
        star_system = StarSystem(output["name"], system_address, minor_factions) 
    return star_system
