from typing import Dict, Any
from abc import ABC, abstractmethod

class StarSystemState:
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

class GalaxyState:
    def __init__(self):
        self._systems:Dict[int, StarSystemState] = {}

    @property
    def systems(self) -> list:
        return self._systems

class PilotState:
    def __init__(self):
        self._last_docked_station = None
        self._missions:list = []

    @property
    def last_docked_station(self) -> object:
        return self._last_docked_station

    @property
    def missions(self) -> list:
        return self.missions

class EventProcessor(ABC):
    @property
    @abstractmethod
    def eventName(self) -> str:
        pass

    @abstractmethod
    def process(self, entry:Dict[str, Any], star_system_state:StarSystemState) -> None:
        pass
    
# Eventually, move this to an IoC setup
_eventProcessors:Dict[str, EventProcessor] = {
    "location": None,
    "docked": None
}

class Tracker:
    def __init__(self, minor_faction:str):
        self._minor_faction:str = minor_faction
        self._pilot_state:PilotState = None
        self._galaxy_state:GalaxyState = None
    
    @property
    def minor_faction(self) -> str:
        return self._minor_faction

    @property
    def pilot_state(self) -> PilotState:
        return self._pilot_state

    @property
    def galaxy_state(self) -> GalaxyState:
        return self._galaxy_state

    def on_entry(self, entry:Dict[str, Any]):
        eventProcessor:EventProcessor = _eventProcessors.get(entry["event"], self._pilot_state, self._galaxy_state)
        if eventProcessor != None:
            eventProcessor.process(entry)
        return None

