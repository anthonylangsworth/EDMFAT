from typing import Dict, Any
from abc import ABC, abstractmethod

from .state import Station, StarSystem,PilotState, GalaxyState
from .event_summaries import RedeemVoucherEventSummary, SellExplorationDataEventSummary, MarketSellEventSummary

def supports_minor_faction(minor_faction: str, supported_minor_faction:str, system_minor_factions:iter, supports_value:bool = True, undermines_value:bool = False):
    if minor_faction == supported_minor_faction:
        supports = supports_value
    elif minor_faction in system_minor_factions:
        supports = undermines_value   
    else:
        supports = None
    return supports 

class EventProcessor(ABC):
    @property
    @abstractmethod
    def eventName(self) -> str:
        #TODO: Make this a list, in case one event processor handles multiple event types
        pass

    @abstractmethod
    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        pass

# Also used for FSDJump. They have the same schema.
class LocationEventProcessor(EventProcessor):
    @property
    def eventName(self) -> str:
        return "Location"

    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        if "Factions" in event.keys():
            galaxy_state.systems[event["SystemAddress"]] = StarSystem(event["StarSystem"], event["SystemAddress"], [faction["Name"] for faction in event["Factions"]])

        if "Docked" in event.keys() and event["Docked"]:
            pilot_state.last_docked_station = Station(event["StationName"], event["SystemAddress"], event["StationFaction"]["Name"])

        return []

class DockedEventProcessor(EventProcessor):
    @property
    def eventName(self) -> str:
        return "Docked"

    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        station = Station(event["StationName"], event["SystemAddress"], event["StationFaction"]["Name"])
        pilot_state.last_docked_station = station
        return []

class RedeemVoucherEventProcessor(EventProcessor):
    @property
    def eventName(self) -> str:
        return "RedeemVoucher"

    def _process_bounty(self, event:Dict[str, Any], system_name:str, minor_faction:str, system_minor_factions:list) -> list:
        result = []
        for x in event["Factions"]:
            supports = supports_minor_faction(x["Faction"], minor_faction, system_minor_factions)

            if supports != None:
                result.append(RedeemVoucherEventSummary(system_name, supports, event["Type"], x["Amount"]))
        return result

    def _process_combat_bond(self, event:Dict[str, Any], system_name:str, minor_faction:str, system_minor_factions:list) -> list:
        supports = supports_minor_faction(event["Faction"], minor_faction, system_minor_factions)

        result = []
        if supports != None:
            result.append(RedeemVoucherEventSummary(system_name, supports, event["Type"], event["Amount"]))
        return result

    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        try:
            star_system = galaxy_state.systems[pilot_state.last_docked_station.system_address]
            system_name = star_system.name
            system_minor_factions = star_system.minor_factions
            known_location = True
        except:
            known_location = False

        # Carriers use a faction of "", excluding it from the logic below

        result = []   
        if known_location and minor_faction in system_minor_factions: # Exclude interstellar factors
            if event["Type"] == "bounty":
                result.extend(self._process_bounty(event, system_name, minor_faction, system_minor_factions))
            elif event["Type"] == "CombatBond": # or event["Type"] == "scannable": # Not sure whether this is BGS relevant
                result.extend(self._process_combat_bond(event, system_name, minor_faction, system_minor_factions))

        return result

# Also used for MultiSellExplorationData. They have the same schema.
class SellExplorationDataEventProcessor(EventProcessor):
    @property
    def eventName(self) -> str:
        return "SellExplorationData"

    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        try:
            star_system = galaxy_state.systems[pilot_state.last_docked_station.system_address]
            system_name = star_system.name
            system_minor_factions = star_system.minor_factions
            controlling_minor_faction = pilot_state.last_docked_station.controlling_minor_faction
            known_location = True
        except: 
            known_location = False

        result = []        
        if known_location:
            supports = supports_minor_faction(minor_faction, controlling_minor_faction, system_minor_factions)

            if supports != None:
                result.append(SellExplorationDataEventSummary(system_name, supports, event["TotalEarnings"]))
        return result

class MarketSellEventProcessor(EventProcessor):
    @property
    def eventName(self) -> str:
        return "MarketSell"

    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        try:
            star_system = galaxy_state.systems[pilot_state.last_docked_station.system_address]
            system_name = star_system.name
            system_minor_factions = star_system.minor_factions
            controlling_minor_faction = pilot_state.last_docked_station.controlling_minor_faction
            known_location = True
        except:
            known_location = False

        result = []        
        if known_location:
            supports = supports_minor_faction(minor_faction, controlling_minor_faction, system_minor_factions, not event.get("BlackMarket", False), event.get("BlackMarket", False))

            if supports != None:
                if event["SellPrice"] <  event["AvgPricePaid"]:
                    supports = not supports
                result.append(MarketSellEventSummary(system_name, supports, event["Count"], event["SellPrice"], event["AvgPricePaid"]))

        return result        
    
# Module non-public
# TODO: move this to an IoC setup
_default_event_processors:Dict[str, EventProcessor] = {
    "Location": LocationEventProcessor(),
    "FSDJump": LocationEventProcessor(),
    "Docked": DockedEventProcessor(),
    "RedeemVoucher": RedeemVoucherEventProcessor(),
    "SellExplorationData": SellExplorationDataEventProcessor(),
    "MultiSellExplorationData": SellExplorationDataEventProcessor(),
    "MarketSell": MarketSellEventProcessor()
}
