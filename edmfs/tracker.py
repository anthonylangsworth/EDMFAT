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

class GalaxyState:
    def __init__(self):
        self._systems:Dict[int, StarSystemState] = {}

    @property
    def systems(self) -> list:
        return self._systems

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

class EventSummary():
    def __init__(self, system_name:str, supports:bool):
        self._system_name:str = system_name
        self._supports:str = supports

    @property
    def system_name(self) -> str:
        return self._system_name

    @property
    def supports(self) -> bool:
        return self._supports

class RedeemVoucherEventSummary(EventSummary):
    def __init__(self, system_name:str, supports:bool, type:str, amount:int):
        super(RedeemVoucherEventSummary, self).__init__(system_name, supports)
        self._type:str = type
        self._amount:int = amount
    
    @property
    def type(self) -> str:
        return self._type

    @property
    def amount(self) -> int:
        return self._amount

class EventProcessor(ABC):
    @property
    @abstractmethod
    def eventName(self) -> str:
        pass

    @abstractmethod
    def process(self, minor_faction:str, entry:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        pass

class LocationEventProcessor(EventProcessor):
    @property
    def eventName(self) -> str:
        return "Location"

    def process(self, minor_faction:str, entry:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        station:Station = None
        if(entry.get("Docked")):
            station = Station(entry["StationName"], entry["SystemAddress"], entry["StationFaction"]["Name"])
            pilot_state.last_docked_station = station
            # galaxy_state. # TODO: Add station to Galaxy State
            return None

class RedeemVoucherEventProcessor(EventProcessor):
    @property
    def eventName(self) -> str:
        return "RedeemVoucher"

    def process(self, minor_faction:str, entry:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        result:list = []
        result.append({"Type": entry[""], "Supports": True, "Amount":x["Amount"] } for x in entry["Factions"] if x.name == minor_faction)
        # if(pilot_state.last_docked_station.system_address):
        #     result.append({"Type": entry[""], "Supports": True, "Amount":x["Amount"] } for x in entry["Factions"] if x.name != minor_faction)
        return result
    
# TODO: move this to an IoC setup
_eventProcessors:Dict[str, EventProcessor] = {
    "Location": LocationEventProcessor(),
    "RedeemVoucher": RedeemVoucherEventProcessor()
}

class Tracker:
    def __init__(self, minor_faction:str):
        self._minor_faction:str = minor_faction
        self._pilot_state:PilotState = PilotState()
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

    def on_event(self, entry:Dict[str, Any]):
        eventProcessor:EventProcessor = _eventProcessors.get(entry["event"], None)
        if eventProcessor != None:
            eventProcessor.process(entry, self.pilot_state, self.galaxy_state)
        return None

