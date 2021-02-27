import requests
import logging
from typing import Tuple, Callable, Optional

import edmfs

def resolve_star_system_via_edsm(logger: logging.Logger, system_address:int) -> edmfs.StarSystem:
    """
    Get the minor factions for the given star system using the ESM API.
    """
    URL = "https://www.edsm.net/api-system-v1/factions"
    try:
        response = requests.get(URL, params={ "systemId64": system_address }, timeout=30)
        if response.status_code == 200:
            output = response.json()
            if "factions" in output and "name" in output:
                minor_factions = [faction["name"] for faction in output["factions"]]
                star_system = edmfs.StarSystem(output["name"], system_address, minor_factions) 
                logger.info(f"Resolved from EDSM: { star_system }")
                return star_system
            else:
                raise Exception(f"Response mising 'factions' or 'output': {output}")
        else:
            response.raise_for_status()
    except Exception as e:
        raise edmfs.UnknownStarSystemError(system_address) from e

# See https://docs.github.com/en/rest/reference/repos#get-the-latest-release
def get_latest_release(logger: logging.Logger, owner:str, repo:str) -> Tuple[str, str]:
    """
    Get the latest github release for the given owner and repo. Returns a tuple containing the tag name and the HTML URL.
    """
    URL = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    try:
        response = requests.get(URL, headers={"accept":"application/vnd.github.v3+json"}, timeout=30)
        if response.status_code == 200:
            output = response.json()
            logger.info(f"Latest version for {owner}/{repo} is '{output['tag_name']}' at '{output['html_url']}'")
            return (output["tag_name"], output["html_url"])
        else:
            response.raise_for_status()
    except Exception as e:
        logger.exception(f"Error getting latest version from github: {e}")
        raise

def split_tag(tag:str) -> Tuple[int]:
    return tuple(map(int, tag.lstrip("v").split(".")))

def get_newer_release(logger: logging.Logger, owner:str, repo:str, current_version:Tuple,
        get_latest_release_callable:Callable[[logging.Logger, str, str], Tuple[str, str]] = get_latest_release) -> Optional[str]:
    """
    Get the URL of the most recent release for the given open and repo if it is a later version than current_version. Otherwise, return None.
    """
    tag_name, url = get_latest_release_callable(logger, owner, repo)
    return url if split_tag(tag_name) > current_version else None
