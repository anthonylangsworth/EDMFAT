from typing import Dict

class StarSystem:
    def __init__(self, name:str, address:int, minor_factions:iter):
        self._name = name
        self._address = address
        self._minor_factions = set(minor_factions)

    @property
    def name(self) -> str:
        return self._name

    @property
    def address(self) -> str:
        return self._address

    @property
    def minor_factions(self) -> set:
        return self._minor_factions

    def __repr__(self) -> str:
        return f"StarSystem('{self._name}', {self._address}, {self._minor_factions})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, StarSystem):
            return NotImplemented

        return self._name == other._name \
            and self._address == other._address \
            and set(self._minor_factions) == set(other._minor_factions)

    def __hash__(self) -> int:
        return hash((self._name, self._address, self._minor_factions))


class Station:
    def __init__(self, name:str, system_address:int, controlling_minor_faction:set):
        self._name:str = name
        self._system_address:int = system_address
        self._controlling_minor_faction:str = controlling_minor_faction

    @property
    def name(self) -> str:
        return self._name

    @property
    def system_address(self) -> int:
        return self._system_address

    @property
    def controlling_minor_faction(self) -> str:
        return self._controlling_minor_faction

    def __eq__ (self, other) -> bool:
        if not isinstance(other, Station):
            return NotImplemented

        return self._name == other._name \
            and self._system_address == other._system_address \
            and self._controlling_minor_faction == other._controlling_minor_faction

    def __repr__(self) -> str:
        return f"Station('{self._name}', {self._system_address}, '{self._controlling_minor_faction}')"

class GalaxyState:
    def __init__(self, star_systems:Dict[int, StarSystem] = {}):
        self._systems:Dict[int, StarSystem] = star_systems

    @property
    def systems(self) -> Dict[int, StarSystem]:
        return self._systems

    def __eq__(self, other) -> bool:
        if not isinstance(other, GalaxyState):
            return NotImplemented

        return self._systems == other._systems

    def __hash__(self) -> int:
        return hash(self._systems)

class PilotState:
    def __init__(self, last_docked_station:Station = None, missions:list = []):
        self._last_docked_station:Station = last_docked_station
        self._missions:list = missions

    @property
    def last_docked_station(self) -> Station:
        return self._last_docked_station

    @last_docked_station.setter
    def last_docked_station(self, value:Station) -> None:
        self._last_docked_station = value

    @property
    def missions(self) -> list:
        return self._missions

    def __eq__(self, other) -> bool:
        if not isinstance(other, PilotState):
            return NotImplemented

        return self._last_docked_station == other._last_docked_station \
            and self._missions == other._missions