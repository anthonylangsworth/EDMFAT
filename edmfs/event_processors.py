from typing import Optional, Dict, Union, Any, Set, List, Tuple
from abc import ABC, abstractmethod

from .state import Station, StarSystem, Mission, PilotState, GalaxyState
from .event_summaries import EventSummary, RedeemVoucherEventSummary, SellExplorationDataEventSummary, MarketSellEventSummary, MarketBuyEventSummary, MissionCompletedEventSummary, MissionFailedEventSummary, MurderEventSummary, SellOrganicDataEventSummary


class UnknownPlayerLocationError(Exception):
    """No last docked station or current system in PilotState. Should only happen when EDMC is started during play."""
    pass


class UnknownStarSystemError(Exception):
    """Star system not found in GalaxyState. Often happens in game."""
    def __init__(self, system: Union[int, str]):
        self._system = system

    @property
    def system(self) -> Union[int, str]:
        return self._system


class UnknownMissionError(Exception):
    """Mission not found in PilotState. Should only happen when EDMC is started during play."""
    def __init__(self, id: int):
        self._id = id

    @property
    def id(self) -> int:
        return self._id


class CommodityNotInLastMarketError(Exception):
    """Commodities were sold or bought at a market without a corresponding entry in market.json."""
    def __init__(self, commodity_name: str):
        self._name = commodity_name

    @property
    def name(self) -> str:
        return self._name


def _get_system(galaxy_state:GalaxyState, system_address:int) -> StarSystem:
    """Convert any KeyError into an UnknownStarSystemError. Convert a missing system_address into an UnknownPlayerLocationError"""
    if system_address == None:
        raise UnknownPlayerLocationError
    try:
        return galaxy_state.systems[system_address]
    except KeyError as e:
        raise UnknownStarSystemError(system_address) from e


def _get_event_minor_faction_impact(event_minor_faction: str, system_minor_factions:iter, inverted:bool = False) -> Tuple[Set[str], Set[str]]:
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
    return (pro, anti) if not inverted else (anti, pro)


class EventProcessor(ABC):
    @abstractmethod
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        pass


# Also used for FSDJump. They have the same schema.
class LocationEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        if "SystemAddress" in event:
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
        if "SystemAddress" in event:
            pilot_state.system_address = event["SystemAddress"]
        return []


class MarketEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        galaxy_state.last_market.clear()
        return []


class RedeemVoucherEventProcessor(EventProcessor):
    def _process_bounty(self, event:Dict[str, Any], system_name:str, system_minor_factions:list) -> List[EventSummary]:
        result = []
        # Redeems at interstellar factors never have a local minor faction name, being ignored.
        # Redeems at fleet carriers do list minor factions names and do count for influence at
        # the final cashed amount.
        for x in event["Factions"]:
            if x["Faction"] != "":
                pro, anti = _get_event_minor_faction_impact(x["Faction"], system_minor_factions)
                result.append(RedeemVoucherEventSummary(system_name, pro, anti, event["Type"], x["Amount"]))
        return result

    def _process_combat_bond(self, event:Dict[str, Any], system_name:str, system_minor_factions:list) -> List[EventSummary]:
        result = []
        # Redeems at interstellar factors never have a local minor faction name, being ignored.
        # Redeems at fleet carriers do list minor factions names and do count for influence at
        # the final cashed amount. However, consider the full amount because this is the best way to
        # approximate the work in a war, at least until conflict zone wins and losses are added to the
        # journal file.
        if event["Faction"] != "":
            pro, anti = _get_event_minor_faction_impact(event["Faction"], system_minor_factions)
            # Remove any broker percentage. We want the full amount to approximate work done in a war.
            amount = event["Amount"]
            if "BrokerPercentage" in event:
                try:
                    broker_percentage = float(event["BrokerPercentage"])
                    if broker_percentage > 0 and broker_percentage < 100:
                        amount = int(round(float(amount) * 100.0/(100.0 - broker_percentage), 0))
                except ValueError:
                    pass
            result = [RedeemVoucherEventSummary(system_name, pro, anti, event["Type"], amount)]
        return result

    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        star_system = _get_system(galaxy_state, pilot_state.system_address)

        result = []
        if event["Type"] == "bounty":
            result.extend(self._process_bounty(event, star_system.name, star_system.minor_factions))
        elif event["Type"] == "CombatBond": 
            result.extend(self._process_combat_bond(event, star_system.name, star_system.minor_factions))

        return result


# Also used for MultiSellExplorationData. They have the same schema.
class SellExplorationDataEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        star_system = _get_system(galaxy_state, pilot_state.system_address)
        station = pilot_state.last_docked_station
        pro, anti = _get_event_minor_faction_impact(station.controlling_minor_faction, star_system.minor_factions)
        return[SellExplorationDataEventSummary(star_system.name, pro, anti, event["TotalEarnings"])]


class MarketSellEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        star_system = _get_system(galaxy_state, pilot_state.system_address)
        station = pilot_state.last_docked_station
        result = []
        if event["SellPrice"] != event["AvgPricePaid"]:
            sold_at_loss = event["SellPrice"] < event["AvgPricePaid"]
            sold_at_blackmarket = "BlackMarket" in event
            pro, anti = _get_event_minor_faction_impact(station.controlling_minor_faction, star_system.minor_factions, 
                (sold_at_loss and not sold_at_blackmarket) or (not sold_at_loss and sold_at_blackmarket))
            result = [MarketSellEventSummary(star_system.name, pro, anti, event["Count"], event["SellPrice"], event["AvgPricePaid"])]
        return result


class MarketBuyEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        star_system = _get_system(galaxy_state, pilot_state.system_address)
        station = pilot_state.last_docked_station
        pro, anti = _get_event_minor_faction_impact(station.controlling_minor_faction, star_system.minor_factions)
        if "Type_Localised" in event.keys():
            commodity_name = event["Type_Localised"]
            market_entry = galaxy_state.last_market[commodity_name]
        elif "Type" in event.keys():
            commodity_name = event["Type"]
            market_entry = next(filter(lambda me: me["Name"] == f'${commodity_name}_name;', galaxy_state.last_market.values()), None) 
        else:
            raise CommodityNotInLastMarketError("(Unknown)")
        if not market_entry:
            raise CommodityNotInLastMarketError(commodity_name)
        result = [MarketBuyEventSummary(star_system.name, pro, anti, event["Count"], event["BuyPrice"], market_entry["StockBracket"])]
        return result


class MissionAcceptedEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        star_system = _get_system(galaxy_state, pilot_state.system_address)
        pilot_state.missions[event["MissionID"]] = Mission(event["MissionID"], event["Faction"], event["Influence"], star_system.address)
        return []


class MissionCompletedEventProcessor(EventProcessor):
    def _create_summary(self, star_system:StarSystem, faction:str, inverted:bool, influence:str) -> MissionCompletedEventSummary:
        pro, anti = _get_event_minor_faction_impact(faction, star_system.minor_factions, inverted)
        return MissionCompletedEventSummary(star_system.name, pro, anti, influence)

    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[EventSummary]:
        mission = pilot_state.missions.get(event["MissionID"], None)      
        # May be empty if not started during this play session. The "Missions" event, listing current missions on startup, lacks source system and minor faction.

        mission_events = []
        if not mission or mission.influence != "None":
            # Use the highest influence to mirror the game UI. 
            max_influence = mission.influence if mission else "+"
            for faction_effect in [x for x in event["FactionEffects"]]:
                for influence_effect in faction_effect["Influence"]:
                    max_influence = max(influence_effect["Influence"], max_influence)

            # Try the Influence entries
            for faction_effect in event["FactionEffects"]:
                for influence_effect in faction_effect["Influence"]:
                    star_system = _get_system(galaxy_state, influence_effect["SystemAddress"])
                    mission_events.append((star_system, faction_effect["Faction"], influence_effect["Trend"] != "UpGood", max_influence))

            # This implementation is technically incorrect, missing situations where the source and destination
            # faction are in the same system. However, this gives a close enough approximation of what is in the
            # Elite Dangerous UI.

            # Add the source faction if missing and the mission is known
            if mission:
                source_system = _get_system(galaxy_state, mission.system_address)
                if not any([x for x in mission_events if x[0].address == source_system.address]): #  and x[1] == event["Faction"]
                    mission_events.append((source_system, event["Faction"], False, max_influence))

            # Add the target faction if supplied and missing
            if "TargetFaction" in event:
                destination_system_name = event.get("DestinationSystem", None) # Ignore redirects from "NewDestinationSystem". It usually applies to assassination or similar missions and not the target faction.
                if destination_system_name:
                    destination_system = next((star_system for star_system in galaxy_state.systems.values() if star_system.name == destination_system_name), None)
                    if not destination_system:
                        raise UnknownStarSystemError(destination_system_name)
                    if not any([x for x in mission_events if x[0].address == destination_system.address]): #  and x[1] == event["TargetFaction"]
                        mission_events.append((destination_system, event["TargetFaction"], False, max_influence))

        if mission:
            del pilot_state.missions[mission.id]

        return [self._create_summary(mission_event[0], mission_event[1], mission_event[2], mission_event[3]) for mission_event in mission_events]


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
            star_system = _get_system(galaxy_state, mission.system_address)
            pro, anti = _get_event_minor_faction_impact(mission.minor_faction, star_system.minor_factions, True)
            result.append(MissionFailedEventSummary(star_system.name, pro, anti))
            del pilot_state.missions[mission.id]
        return result


class CommitCrimeEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[MurderEventSummary]:
        result = []
        if event["CrimeType"] == "murder":
            star_system = _get_system(galaxy_state, pilot_state.system_address)
            pro, anti = _get_event_minor_faction_impact(event["Faction"], star_system.minor_factions, True)
            result.append(MurderEventSummary(star_system.name, pro, anti))
        return result


class SellOrganicDataEventProcessor(EventProcessor):
    def process(self, event:Dict[str, Any], pilot_state:PilotState, galaxy_state:GalaxyState) -> List[SellOrganicDataEventSummary]:
        result = []
        value = 0
        for biodata_entry in event["BioData"]:
            value += biodata_entry["Value"]
        if value > 0:
            star_system = _get_system(galaxy_state, pilot_state.system_address)
            pro, anti = _get_event_minor_faction_impact(pilot_state.last_docked_station.controlling_minor_faction, star_system.minor_factions)
            result.append(SellOrganicDataEventSummary(star_system.name, pro, anti, value))
        return result


# Map journal file event types to the EventProcessor that handles them
_default_event_processors:Dict[str, EventProcessor] = {
    "Location": LocationEventProcessor(),
    "FSDJump": LocationEventProcessor(),
    "CarrierJump": LocationEventProcessor(),
    "Docked": DockedEventProcessor(),
    "RedeemVoucher": RedeemVoucherEventProcessor(),
    "SellExplorationData": SellExplorationDataEventProcessor(),
    "MultiSellExplorationData": SellExplorationDataEventProcessor(),
    "MarketSell": MarketSellEventProcessor(),
    "MarketBuy": MarketBuyEventProcessor(),
    "MissionAccepted": MissionAcceptedEventProcessor(),
    "MissionCompleted": MissionCompletedEventProcessor(),
    "MissionAbandoned": MissionAbandonedEventProcessor(),
    "MissionFailed": MissionFailedEventProcessor(),
    "CommitCrime": CommitCrimeEventProcessor(),
    "SellOrganicData": SellOrganicDataEventProcessor(),
    "Market": MarketEventProcessor()
}
