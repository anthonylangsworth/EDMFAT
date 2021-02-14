import requests
import logging
from typing import Tuple

from edmfs.state import StarSystem

def resolve_star_system_via_edsm(logger: logging.Logger, system_address:int) -> StarSystem:
    URL = "https://www.edsm.net/api-system-v1/factions"
    star_system = None
    try:
        response = requests.get(URL, params={ "systemId64": system_address }, timeout=30)
        if response.status_code == 200:
            output = response.json()
            if "factions" in output and "name" in output:
                minor_factions = [faction["name"] for faction in output["factions"]]
                star_system = StarSystem(output["name"], system_address, minor_factions) 
                logger.info(f"Resolved from EDSM: { star_system }")
            else:
                raise Exception(f"Response mising 'factions' or 'output': {output}")
    except Exception as e:
        logger.exception(f"Error resolving { system_address } from EDSM: { e }")        
    return star_system

# See https://docs.github.com/en/rest/reference/repos#get-the-latest-release
def get_latest_release(logger: logging.Logger, current_version:Tuple[int], owner:str, repo:str):
    URL = f"/repos/{owner}/{repo}/releases/latest"
    try:
        response = requests.get(URL, headers={"accept":"application/vnd.github.v3+json"}, timeout=30)
        if response.status_code == 200:
            output = response.json()
            if "tag_name" in output and "url" in output:
                # logger.info(f"Resolved from EDSM: { star_system }")
                pass
            else:
                raise Exception(f"Response mising 'tag_name' or 'url': {output}")
    except Exception as e:
        logger.exception(f"Error: { e }")        
    return []

def split_tag(tag:str) -> Tuple[int]:
    return tuple(map(int, tag.lstrip("v").split(".")))

