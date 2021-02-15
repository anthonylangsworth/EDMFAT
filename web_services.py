import requests
import logging
from typing import Tuple

from edmfs.state import StarSystem

def resolve_star_system_via_edsm(logger: logging.Logger, system_address:int) -> StarSystem:
    URL = "https://www.edsm.net/api-system-v1/factions"
    try:
        response = requests.get(URL, params={ "systemId64": system_address }, timeout=30)
        if response.status_code == 200:
            output = response.json()
            if "factions" in output and "name" in output:
                minor_factions = [faction["name"] for faction in output["factions"]]
                star_system = StarSystem(output["name"], system_address, minor_factions) 
                logger.info(f"Resolved from EDSM: { star_system }")
                return star_system
            else:
                raise Exception(f"Response mising 'factions' or 'output': {output}")
    except Exception as e:
        logger.exception(f"Error resolving { system_address } from EDSM: { e }")        
        raise

# See https://docs.github.com/en/rest/reference/repos#get-the-latest-release
def get_latest_release(logger: logging.Logger, owner:str, repo:str) -> Tuple:
    URL = f"/repos/{owner}/{repo}/releases/latest"
    try:
        response = requests.get(URL, headers={"accept":"application/vnd.github.v3+json"}, timeout=30)
        if response.status_code == 200:
            output = response.json()
            return (output["tag_name"], output["url"])
    except Exception as e:
        logger.exception(f"Error: { e }")        
        raise

def split_tag(tag:str) -> Tuple[int]:
    return tuple(map(int, tag.lstrip("v").split(".")))

def is_later_release_available(logger: logging.Logger, owner:str, repo:str, current_version:Tuple[int]) -> str:
    tag_name, url = get_latest_release(logger, owner, repo)
    return url if split_tag(tag_name) > current_version else None
