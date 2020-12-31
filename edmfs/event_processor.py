from typing import Dict, Any
from abc import ABC, abstractmethod

from .state import Station, PilotState, GalaxyState
from .event_summary import RedeemVoucherEventSummary

class EventProcessor(ABC):
    @property
    @abstractmethod
    def eventName(self) -> str:
        pass

    @abstractmethod
    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        pass

class LocationEventProcessor(EventProcessor):
    @property
    def eventName(self) -> str:
        return "Location"

    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        station:Station = None
        if(event.get("Docked")):
            station = Station(event["StationName"], event["SystemAddress"], event["StationFaction"]["Name"])
            pilot_state.last_docked_station = station
            # galaxy_state. # TODO: Add station to Galaxy State
            return None

class RedeemVoucherEventProcessor(EventProcessor):
    @property
    def eventName(self) -> str:
        return "RedeemVoucher"

    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        result:list = []
        result.extend([RedeemVoucherEventSummary("", True, event["Type"], x["Amount"]) for x in event["Factions"] if x["Faction"] == minor_faction])
        # TODO: Add Anti-faction summary entries
        # TODO: Remember fleet carriers have a faction "" which should not count against the minor faction
        # if(pilot_state.last_docked_station.system_address):
        #     result.append({"Type": entry[""], "Supports": True, "Amount":x["Amount"] } for x in entry["Factions"] if x.name != minor_faction)
        return result
    
