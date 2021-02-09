from typing import Dict, Callable


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
            and self._system_address == other._system_address \
            and self._controlling_minor_faction == other._controlling_minor_faction

    def __repr__(self) -> str:
        return f"Station('{self._name}', {self._system_address}, '{self._controlling_minor_faction}')"


class Mission:
    def __init__(self, id:int, minor_faction:str, influence:str, system_address:int):
        self._id = id
        self._minor_faction = minor_faction
        self._influence = influence
        self._system_address = system_address

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def minor_faction(self) -> int:
        return self._minor_faction
    
    @property
    def influence(self) -> str:
        return self._influence
    
    @property
    def system_address(self) -> int:
        return self._system_address
    
    def __eq__ (self, other) -> bool:
        if not isinstance(other, Mission):
            return NotImplemented

        return (self._id == other._id
            and self._minor_faction == other._minor_faction
            and self._influence == other._influence
            and self._system_address == other._system_address)

    def __repr__(self) -> str:
        return f"Mission({self._id}, '{self._minor_faction}', '{self._influence}', {self._system_address})"


class GalaxyState:
    def __init__(self, star_system_resolver:Callable[[int], StarSystem] = None, star_systems:Dict[int, StarSystem] = None):
        self._systems:Dict[int, StarSystem] = star_systems if star_systems else {} # Workaround for {} being shared in edge cases
        self._star_system_resolver = star_system_resolver if star_system_resolver else lambda x: None

    @property
    def systems(self) -> Dict[int, StarSystem]:
        return self._systems

    def get_system(self, system_address:int) -> StarSystem:
        star_system = self._systems.get(system_address, None)
        if not star_system:
            star_system = self._star_system_resolver(system_address)
            self._systems[system_address] = star_system
        return star_system

    def __eq__(self, other) -> bool:
        if not isinstance(other, GalaxyState):
            return NotImplemented

        return self._systems == other._systems

    def __repr__(self) -> str:
        return f"GalaxyState({self._star_system_resolver}, {self._systems})"


class PilotState:
    def __init__(self, system_address:int = None, last_docked_station:Station = None, missions:Dict[int, Mission] = None):
        self._system_address = system_address
        self._last_docked_station = last_docked_station
        self._missions = missions if missions else dict() # Workaround for {} being shared in edge cases

    @property
    def last_docked_station(self) -> Station:
        return self._last_docked_station

    @last_docked_station.setter
    def last_docked_station(self, value:Station) -> None:
        self._last_docked_station = value

    @property
    def system_address(self) -> int:
        return self._system_address

    @system_address.setter
    def system_address(self, value:int) -> None:
        self._system_address = value        

    @property
    def missions(self) -> Dict[int, Mission]:
        return self._missions

    def __eq__(self, other) -> bool:
        if not isinstance(other, PilotState):
            return NotImplemented

        return self._system_address == other._system_address \
            and self._last_docked_station == other._last_docked_station \
            and self._missions == other._missions

    def __repr__(self) -> str:
        return f"PilotState({self._system_address}, {self._last_docked_station}, {self._missions})"
