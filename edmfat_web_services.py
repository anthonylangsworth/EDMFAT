import requests
import logging
from typing import Tuple, Callable, Optional, Dict
import json
import os

import edmfs
try:
    from config import config
except ImportError:
    class config:
        def get_str(self, s):
            return ''

        @property
        def default_journal_dir(self):
            return os.path.expandvars("${userprofile}\\Saved Games\\Frontier Developments\\Elite Dangerous\\")


def resolve_star_system_via_edsm(logger: logging.Logger, system_address: int) -> edmfs.StarSystem:
    """
    Get the minor factions for the given star system using the ESM API.
    """
    URL = "https://www.edsm.net/api-system-v1/factions"
    try:
        with requests.get(URL, params={"systemId64": system_address}, timeout=30) as response:
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
def get_latest_release(logger: logging.Logger, owner: str, repo: str) -> Tuple[str, str]:
    """
    Get the latest github release for the given owner and repo. Returns a tuple containing the tag name and the HTML URL.
    """
    URL = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    try:
        with requests.get(URL, headers={"accept": "application/vnd.github.v3+json"}, timeout=30) as response:
            if response.status_code == 200:
                output = response.json()
                logger.info(f"Latest version for {owner}/{repo} is '{output['tag_name']}' at '{output['html_url']}'")
                return (output["tag_name"], output["html_url"])
            else:
                response.raise_for_status()
    except Exception as e:
        logger.exception(f"Error getting latest version from github: {e}")
        raise


def split_tag(tag: str) -> Tuple[int]:
    return tuple(map(int, tag.lstrip("v").split(".")))


def get_newer_release(logger: logging.Logger, owner: str, repo: str, current_version: Tuple,
        get_latest_release_callable: Callable[[logging.Logger, str, str], Tuple[str, str]] = get_latest_release) -> Optional[str]:
    """
    Get the URL of the most recent release for the given open and repo if it is a later version than current_version. Otherwise, return None.
    """
    tag_name, url = get_latest_release_callable(logger, owner, repo)
    return url if split_tag(tag_name) > current_version else None


def get_last_market(logger: logging.Logger, market_json_file_path: str = None) -> Dict[str, Dict]:
    """
    Return a Dict containing market.json Items. Technically not a web service but still an external access.
    """
    if market_json_file_path is None:
        config_journal_dir = config.get_str("journaldir")
        journal_dir = config_journal_dir if os.path.exists(config_journal_dir) else config.default_journal_dir
        file_path = os.path.join(journal_dir, "market.json")
    else:
        file_path = market_json_file_path
    with open(file_path, mode="r") as market_json_file:
        market = json.load(market_json_file)
    result = {}
    for market_entry in market["Items"]:
        result[str(market_entry["Name_Localised"]).strip()] = market_entry
    logger.info(f"Reloaded '{file_path}'")
    return result
