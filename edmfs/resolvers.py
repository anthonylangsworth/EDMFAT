import requests
import logging

from .state import StarSystem
from .event_processors import UnknownStarSystemError

def resolve_star_system_via_edsm(logger: logging.Logger, system_address:int) -> StarSystem:
    URL = "https://www.edsm.net/api-system-v1/factions"
    star_system = None
    try:
        response = requests.get(URL, params={ "systemId64": system_address }, timeout=30)
        if response.status_code == 200:
            output = response.json()
            minor_factions = [faction["name"] for faction in output["factions"]]
            star_system = StarSystem(output["name"], system_address, minor_factions) 
            logger.info(f"Resolved from EDSM: { star_system }")
    except requests.exceptions.RequestException as e:
        logger.exception(f"Error resolving { system_address } from EDSM: { e }")        
    return star_system
