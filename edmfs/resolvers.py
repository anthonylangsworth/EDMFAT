import requests
import logging
from collections.abc import MutableMapping

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
    except Exception as e:
        logger.exception(f"Error resolving { system_address } from EDSM: { e }")        
    return star_system


# class ResolvingDict(MutableMapping):
#     def __init__(self, resolver:callable, inner:MutableMapping = None):
#         self._resolver = resolver
#         self._dict = inner if inner else dict()

#     @property
#     def resolver(self) -> callable:
#         return self._resolver

#     def __getitem__(self, key):
#         if key in self._dict:
#             result = self._dict[key]
#         else:
#             result = self._resolver(key)
#             if result:
#                 self._dict[key] = result
#         return result

#     def __setitem__(self, key, value):
#         self._dict[key] = value
    
#     def __delitem__(self, key):
#         del self._dict[key]

#     def __iter__(self):
#         return self._dict.__iter__()

#     def __len__(self):
#         return len(self._dict)

