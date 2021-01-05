from typing import Dict, Any
from abc import ABC, abstractmethod

from .state import Station, StarSystem, Mission, PilotState, GalaxyState
from .event_summaries import RedeemVoucherEventSummary, SellExplorationDataEventSummary, MarketSellEventSummary, MissionCompletedEventSummary

class NoLastDockedStationError(Exception):
    """No last docked station in PilotState. Should not happen in game."""
    pass

class UnknownStarSystemError(Exception):
    """Star system not found in GalaxyState. Should not happen in game."""
    def __init__(self, system_address: int):
        self._system_address = system_address

    @property
    def system_address(self) -> int:
        return self._system_address

class UnknownMissionError(Exception):
    """Mission not found in PilotState. Should not happen in game."""
    def __init__(self, id: int):
        self._id = id

    @property
    def id(self) -> int:
        return self._id

def _supports_minor_faction(minor_faction: str, supported_minor_faction:str, system_minor_factions:iter, supports_value:bool = True, undermines_value:bool = False):
    if not supported_minor_faction in system_minor_factions:
        supports = None
    elif minor_faction == supported_minor_faction:
        supports = supports_value
    elif minor_faction in system_minor_factions:
        supports = undermines_value   
    else:
        supports = None
    return supports 

def _get_location(pilot_state: PilotState, galaxy_state:GalaxyState) -> tuple:
    if not pilot_state.last_docked_station:
        raise NoLastDockedStationError()

    if not galaxy_state.systems.get(pilot_state.last_docked_station.system_address, None):
        raise UnknownStarSystemError(pilot_state.last_docked_station.system_address)

    star_system = galaxy_state.systems[pilot_state.last_docked_station.system_address]
    station = pilot_state.last_docked_station

    return (star_system, station)

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

        if event.get("Docked", False):
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
            supports = _supports_minor_faction(x["Faction"], minor_faction, system_minor_factions)

            if supports != None:
                result.append(RedeemVoucherEventSummary(system_name, supports, event["Type"], x["Amount"]))
        return result

    def _process_combat_bond(self, event:Dict[str, Any], system_name:str, minor_faction:str, system_minor_factions:list) -> list:
        supports = _supports_minor_faction(event["Faction"], minor_faction, system_minor_factions)

        result = []
        if supports != None:
            result.append(RedeemVoucherEventSummary(system_name, supports, event["Type"], event["Amount"]))
        return result

    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        star_system, _ = _get_location(pilot_state, galaxy_state)

        # Carriers use a faction of "", excluding it from the logic below

        result = []   
        if minor_faction in star_system.minor_factions: # Exclude interstellar factors
            if event["Type"] == "bounty":
                result.extend(self._process_bounty(event, star_system.name, minor_faction, star_system.minor_factions))
            elif event["Type"] == "CombatBond": 
                result.extend(self._process_combat_bond(event, star_system.name, minor_faction, star_system.minor_factions))

        return result

# Also used for MultiSellExplorationData. They have the same schema.
class SellExplorationDataEventProcessor(EventProcessor):
    @property
    def eventName(self) -> str:
        return "SellExplorationData"

    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        star_system, station = _get_location(pilot_state, galaxy_state)
        supports = _supports_minor_faction(minor_faction, station.controlling_minor_faction, star_system.minor_factions)

        result = []        
        if supports != None:
            result.append(SellExplorationDataEventSummary(star_system.name, supports, event["TotalEarnings"]))
        return result

class MarketSellEventProcessor(EventProcessor):
    @property
    def eventName(self) -> str:
        return "MarketSell"

    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        star_system, station = _get_location(pilot_state, galaxy_state)
        supports = _supports_minor_faction(minor_faction, station.controlling_minor_faction, star_system.minor_factions, not event.get("BlackMarket", False), event.get("BlackMarket", False))

        result = []        
        if supports != None:
            if event["SellPrice"] <  event["AvgPricePaid"]:
                supports = not supports
            result.append(MarketSellEventSummary(star_system.name, supports, event["Count"], event["SellPrice"], event["AvgPricePaid"]))

        return result

class MissionCompletedEventProcessor(EventProcessor):
    @property
    def eventName(self) -> str:
        return "MissionCompleted"
        
    def process(self, event:Dict[str, Any], minor_faction:str, pilot_state:PilotState, galaxy_state:GalaxyState) -> list:
        result = []

        # Use the highest influence to mirror the game UI. 

        max_influence = ""
        for faction_effect in [x for x in event["FactionEffects"]]:
            for influence_effect in faction_effect["Influence"]:
                max_influence = influence_effect["Influence"] if influence_effect["Influence"] > max_influence else max_influence

        for faction_effect in [x for x in event["FactionEffects"]]:
            for influence_effect in faction_effect["Influence"]:
                star_system = galaxy_state.systems.get(influence_effect["SystemAddress"], None)
                if not star_system:
                    raise UnknownStarSystemError(influence_effect["SystemAddress"])
                supports = _supports_minor_faction(faction_effect["Faction"], minor_faction, star_system.minor_factions, influence_effect["Trend"] == "UpGood", influence_effect["Trend"] != "UpGood")
                if supports != None:
                    result.append(MissionCompletedEventSummary(star_system.name, supports, max_influence))
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
    "MarketSell": MarketSellEventProcessor(),
    "MissionCompleted": MissionCompletedEventProcessor()
}
