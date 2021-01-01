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
        try:
            system_name = galaxy_state.systems[pilot_state.last_docked_station.system_address].name
        except:
            system_name = "unknown"

        if(event["Type"] == "bounty"):
            result.extend([RedeemVoucherEventSummary(system_name, True, event["Type"], x["Amount"]) for x in event["Factions"] if x["Faction"] == minor_faction])
            # Fleet carriers have a faction "" which should not count against the minor faction
            result.extend([RedeemVoucherEventSummary(system_name, False, event["Type"], x["Amount"]) for x in event["Factions"] if x["Faction"] != minor_faction and x["Faction"] != ""])
        elif(event["Type"] == "CombatBond"):
            if(event["Faction"] == minor_faction):
                result.append(RedeemVoucherEventSummary(system_name, True, event["Type"], event["Amount"]))
            elif(minor_faction in galaxy_state.systems[pilot_state.last_docked_station.system_address].minor_factions):
                result.append(RedeemVoucherEventSummary(system_name, False, event["Type"], event["Amount"]))
        elif(event["Type"] == "scannable"):
            if(pilot_state.last_docked_station.controlling_minor_faction == minor_faction):
                result.append(RedeemVoucherEventSummary(system_name, True, event["Type"], event["Amount"]))
        return result
    
# Module non-public
# TODO: move this to an IoC setup
_eventProcessors:Dict[str, EventProcessor] = {
    "Location": LocationEventProcessor(),
    "RedeemVoucher": RedeemVoucherEventProcessor()
}
