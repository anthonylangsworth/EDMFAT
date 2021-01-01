from typing import Dict

class StarSystem:
    def __init__(self, name:str, address:int, minor_factions:tuple):
        self._name = name
        self._address = address
        self._minor_factions = minor_factions

    @property
    def name(self) -> str:
        return self._name

    @property
    def address(self) -> str:
        return self._address

    @property
    def minor_factions(self) -> str:
        return self._minor_factions

    def __str__(self) -> str:
        return f"{self._name} [{self._address}]"

class Station:
    def __init__(self, name:str, system_address:int, controlling_minor_faction:str):
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
            and self._controlling_minor_faction == other._controlling_minor_faction

    def __str__(self) -> str:
        return f"{self._name} [{self._system_address}]"

class GalaxyState:
    def __init__(self):
        self._systems:Dict[int, StarSystem] = {}

    @property
    def systems(self) -> list:
        return self._systems

    def __eq__(self, other) -> bool:
        if not isinstance(other, GalaxyState):
            return NotImplemented

        return self._systems == other._systems

class PilotState:
    def __init__(self):
        self._last_docked_station:Station = None
        self._missions:list = []

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
                

