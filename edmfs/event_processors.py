from typing import Dict, Any
from abc import ABC, abstractmethod

from .state import Station, PilotState, GalaxyState
from .event_summaries import RedeemVoucherEventSummary

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
        if(event["Type"] == "CombatBond"):
            if(event["Faction"] == minor_faction):
                result.append(RedeemVoucherEventSummary("", True, event["Type"], event["Amount"]))
            # elif(minor_faction in galaxy_state.systems[pilot_state.last_docked_station.system_address].minor_factions):
            #    result.append(RedeemVoucherEventSummary("", False, event["Type"], event["Amount"]))
        elif(event["Type"] == "scannable"):
            if(pilot_state.last_docked_station.controlling_minor_faction == minor_faction):
                result.append(RedeemVoucherEventSummary("", True, event["Type"], event["Amount"]))
            # elif # TODO: Handle anti-minor faction work
        elif(event["Type"] == "bounty"):
            result.extend([RedeemVoucherEventSummary("", True, event["Type"], x["Amount"]) for x in event["Factions"] if x["Faction"] == minor_faction])
            # elif # TODO: Handle anti-minor faction work  
            # TODO: Remember fleet carriers have a faction "" which should not count against the minor faction
            # if(pilot_state.last_docked_station.system_address):
            #     result.append({"Type": entry[""], "Supports": True, "Amount":x["Amount"] } for x in entry["Factions"] if x.name != minor_faction)
        return result
    
# Module non-public
# TODO: move this to an IoC setup
_eventProcessors:Dict[str, EventProcessor] = {
    "Location": LocationEventProcessor(),
    "RedeemVoucher": RedeemVoucherEventProcessor()
}
