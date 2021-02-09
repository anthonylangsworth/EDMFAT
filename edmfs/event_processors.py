from typing import Optional, Dict, Union, Any, Set, List
from abc import ABC, abstractmethod

from .state import Station, StarSystem, Mission, PilotState, GalaxyState
from .event_summaries import EventSummary, RedeemVoucherEventSummary, SellExplorationDataEventSummary, MarketSellEventSummary, MissionCompletedEventSummary, MissionFailedEventSummary, MurderEventSummary


class NoLastDockedStationError(Exception):
    """No last docked station in PilotState. Should not happen in game."""
    pass


class UnknownStarSystemError(Exception):
    """Star system not found in GalaxyState. Should not happen in game."""
    def __init__(self, system: Union[int, str]):
        self._system = system

    @property
    def system(self) -> int:
        return self._system


class UnknownMissionError(Exception):
    """Mission not found in PilotState. Should not happen in game."""
    def __init__(self, id: int):
        self._id = id

    @property
    def id(self) -> int:
        return self._id


def _get_event_minor_faction_impact(event_minor_faction: str, system_minor_factions:iter, inverted:bool = False) -> tuple:
    """
    Return a tuple containing the minor factions this event supported ("pro") and undermined ("anti").

    Technically, there are four states but a pro/anti split is sufficient for this plug-in. The states are:
    1. Direct support: Increases the influence of that minor faction, such as completing a mission for that faction. Considered "pro".
    2. Direct undermine: Decrease the influence of that minor faction, such as an assassination mission against a ship for that faction. Considered "anti".
    3. Indirect support: Decrease the influence of another minor faction in that system. Considered "pro".
    4. Indirect undermine: Increase the influence of another minor faction in that system. Considered "anti".
    """
    if event_minor_faction in system_minor_factions:
        pro = {minor_faction for minor_faction in system_minor_factions if (minor_faction == event_minor_faction)}
        anti = {minor_faction for minor_faction in system_minor_factions if (minor_faction != event_minor_faction)} 
    else:
        pro = set([event_minor_faction])
        anti = set()
    return (
        pro if not inverted else anti,
        anti if not inverted else pro
    ) 


class EventProcessor(ABC):
    @abstractmethod
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        pass


# Also used for FSDJump. They have the same schema.
class LocationEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        pilot_state.system_address = event["SystemAddress"]       
        if "Factions" in event:
            galaxy_state.systems[event["SystemAddress"]] = StarSystem(event["StarSystem"], event["SystemAddress"], [faction["Name"] for faction in event["Factions"]])
        if event.get("Docked", False):
            pilot_state.last_docked_station = Station(event["StationName"], event["SystemAddress"], event["StationFaction"]["Name"])
        return []


class DockedEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        station = Station(event["StationName"], event["SystemAddress"], event["StationFaction"]["Name"])
        pilot_state.last_docked_station = station
        return []


class RedeemVoucherEventProcessor(EventProcessor):
    def _process_bounty(self, event:Dict[str, Any], system_name:str, system_minor_factions:list) -> List[EventSummary]:
        result = []
        for x in event["Factions"]:
            pro, anti = _get_event_minor_faction_impact(x["Faction"], system_minor_factions)
            result.append(RedeemVoucherEventSummary(system_name, pro, anti, event["Type"], x["Amount"]))
        return result

    def _process_combat_bond(self, event:Dict[str, Any], system_name:str, system_minor_factions:list) -> List[EventSummary]:
        pro, anti = _get_event_minor_faction_impact(event["Faction"], system_minor_factions)
        return [RedeemVoucherEventSummary(system_name, pro, anti, event["Type"], event["Amount"])]

    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        star_system = galaxy_state.get_system(pilot_state.system_address)

        result = []
        if event.get("BrokerPercentage", None) == None: # Exclude interstellar factors
            if event["Type"] == "bounty":
                result.extend(self._process_bounty(event, star_system.name, star_system.minor_factions))
            elif event["Type"] == "CombatBond": 
                result.extend(self._process_combat_bond(event, star_system.name, star_system.minor_factions))

        return result


# Also used for MultiSellExplorationData. They have the same schema.
class SellExplorationDataEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        star_system = galaxy_state.get_system(pilot_state.system_address)
        station = pilot_state.last_docked_station
        pro, anti = _get_event_minor_faction_impact(station.controlling_minor_faction, star_system.minor_factions)
        return[SellExplorationDataEventSummary(star_system.name, pro, anti, event["TotalEarnings"])]


class MarketSellEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        star_system = galaxy_state.get_system(pilot_state.system_address)
        station = pilot_state.last_docked_station
        result = []
        if event["SellPrice"] != event["AvgPricePaid"]:
            sold_at_loss = event["SellPrice"] < event["AvgPricePaid"]
            sold_at_blackmarket = "BlackMarket" in event
            pro, anti = _get_event_minor_faction_impact(station.controlling_minor_faction, star_system.minor_factions, 
                (sold_at_loss and not sold_at_blackmarket) or (not sold_at_loss and sold_at_blackmarket))
            result = [MarketSellEventSummary(star_system.name, pro, anti, event["Count"], event["SellPrice"], event["AvgPricePaid"])]
        return result


class MissionAcceptedEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        star_system = galaxy_state.get_system(pilot_state.system_address)
        pilot_state.missions[event["MissionID"]] = Mission(event["MissionID"], event["Faction"], event["Influence"], star_system.address)
        return []


class MissionCompletedEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        mission = pilot_state.missions.get(event["MissionID"], None)      
        # May be empty if not started during this play session. The "Missions" event, listing current missions on startup, lacks source system and minor faction.

        result = []
        if not mission or mission.influence != "None":
            # Use the highest influence to mirror the game UI. 
            max_influence = mission.influence if mission else "+"
            for faction_effect in [x for x in event["FactionEffects"]]:
                for influence_effect in faction_effect["Influence"]:
                    max_influence = max(influence_effect["Influence"], max_influence)

            # Try the Influence entries
            for faction_effect in event["FactionEffects"]:
                for influence_effect in faction_effect["Influence"]:
                    star_system = galaxy_state.get_system(influence_effect["SystemAddress"])
                    if not star_system:
                        raise UnknownStarSystemError(influence_effect["SystemAddress"])
                    pro, anti = _get_event_minor_faction_impact(faction_effect["Faction"], star_system.minor_factions, influence_effect["Trend"] != "UpGood")
                    result.append(MissionCompletedEventSummary(star_system.name, pro, anti, max_influence))

            # This logic may have issues with the source and destination system are the same but have different source and target factions differ

            # Add the source system if missing and the mission is known
            if mission:
                source_system = galaxy_state.get_system(mission.system_address)
                if not source_system:
                    raise UnknownStarSystemError(mission.system_address)
                if not any([x for x in result if x.system_name == source_system.name]):
                    pro, anti = _get_event_minor_faction_impact(event["Faction"], source_system.minor_factions)
                    result.append(MissionCompletedEventSummary(source_system.name, pro, anti, max_influence))

            # Add the target system if required and missing
            if "TargetFaction" in event:
                destination_system_name = event.get("NewDestinationSystem", None) if "NewDestinationSystem" in event != None else event.get("DestinationSystem", None)
                if destination_system_name:
                    destination_system = next((star_system for star_system in galaxy_state.systems.values() if star_system.name == destination_system_name), None)
                    if not destination_system:
                        raise UnknownStarSystemError(destination_system_name)
                    if not any([x for x in result if x.system_name == destination_system_name]):
                        pro, anti = _get_event_minor_faction_impact(event["TargetFaction"], destination_system.minor_factions)
                        result.append(MissionCompletedEventSummary(destination_system.name, pro, anti, max_influence))                            

        if mission:
            del pilot_state.missions[mission.id]

        return result


class MissionAbandonedEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        if event["MissionID"] in pilot_state.missions:
            del pilot_state.missions[event["MissionID"]]
        return []


class MissionFailedEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[MissionFailedEventSummary]:
        result = []
        mission = pilot_state.missions.get(event["MissionID"], None)
        if mission:
            star_system = galaxy_state.get_system(mission.system_address)
            if not star_system:
                raise UnknownStarSystemError(mission.system_address)
            pro, anti = _get_event_minor_faction_impact(mission.minor_faction, star_system.minor_factions, True)
            result.append(MissionFailedEventSummary(star_system.name, pro, anti))
            del pilot_state.missions[mission.id]
        return result


class CommitCrimeEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[MurderEventSummary]:
        result = []
        if event["CrimeType"] == "murder":
            star_system = galaxy_state.get_system(pilot_state.system_address)
            if not star_system:
                raise UnknownStarSystemError(pilot_state.system_address)
            pro, anti = _get_event_minor_faction_impact(event["Faction"], star_system.minor_factions, True)
            result.append(MurderEventSummary(star_system.name, pro, anti))
        return result


# Module non-public
_default_event_processors:Dict[str, EventProcessor] = {
    "Location": LocationEventProcessor(),
    "FSDJump": LocationEventProcessor(),
    "Docked": DockedEventProcessor(),
    "RedeemVoucher": RedeemVoucherEventProcessor(),
    "SellExplorationData": SellExplorationDataEventProcessor(),
    "MultiSellExplorationData": SellExplorationDataEventProcessor(),
    "MarketSell": MarketSellEventProcessor(),
    "MissionAccepted": MissionAcceptedEventProcessor(),
    "MissionCompleted": MissionCompletedEventProcessor(),
    "MissionAbandoned": MissionAbandonedEventProcessor(),
    "MissionFailed": MissionFailedEventProcessor(),
    "CommitCrime": CommitCrimeEventProcessor()
}
