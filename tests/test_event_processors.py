import copy
from typing import Dict, Any, Set, List, Iterable, Tuple
import pytest

from edmfs.event_processors import _get_event_minor_faction_impact, LocationEventProcessor, RedeemVoucherEventProcessor, DockedEventProcessor, SellExplorationDataEventProcessor, MarketSellEventProcessor, UnknownPlayerLocationError, UnknownStarSystemError, MissionAcceptedEventProcessor, MissionCompletedEventProcessor, MissionAbandonedEventProcessor, MissionFailedEventProcessor, CommitCrimeEventProcessor
from edmfs.state import PilotState, GalaxyState, Station, Mission, StarSystem
from edmfs.event_summaries import EventSummary, RedeemVoucherEventSummary, SellExplorationDataEventSummary, MarketSellEventSummary, MissionCompletedEventSummary, MissionFailedEventSummary, MurderEventSummary


@pytest.mark.parametrize(
    "event_minor_faction, system_minor_factions, expected_result",
    (
        ("a", {"a", "b"}, ({"a"}, {"b"})),
        ("b", {"a", "b"}, ({"b"}, {"a"})),
        ("c", {"a", "b"}, (set("c"), set())),

        # Should not happen but included for predictability
        ("a", set(), (set("a"), set())),
        ("a", {"c"}, (set("a"), set())),
        ("a", {"c", "d"}, (set("a"), set()))
    )
)
def test_get_event_minor_faction_impact(event_minor_faction: str, system_minor_factions: Iterable, expected_result: tuple):
    assert _get_event_minor_faction_impact(event_minor_faction, system_minor_factions) == expected_result


@pytest.mark.parametrize(
    "location_event, expected_station, expected_system",
    [
        (
            { "timestamp":"2020-12-30T01:04:56Z", "event":"Location", "Docked": True, "StationName": "Q3H-7HT", "StationType": "FleetCarrier", "MarketID": 3703794688, "StationFaction": { "Name": "FleetCarrier" }, "StationGovernment": "$government_Carrier;", "StationGovernment_Localised": "Private Ownership ", "StationServices": [ "dock", "autodock", "commodities", "contacts", "outfitting", "crewlounge", "rearm", "refuel", "repair", "shipyard", "engineer", "flightcontroller", "stationoperations", "stationMenu", "carriermanagement", "carrierfuel", "voucherredemption" ], "StationEconomy":"$economy_Carrier;", "StationEconomy_Localised":"Private Enterprise", "StationEconomies":[ { "Name":"$economy_Carrier;", "Name_Localised":"Private Enterprise", "Proportion":1.000000 } ], "StarSystem":"HR 1597", "SystemAddress":869487593835, "StarPos":[78.18750,-60.87500,-3.43750], "SystemAllegiance":"Independent", "SystemEconomy":"$economy_Military;", "SystemEconomy_Localised":"Military", "SystemSecondEconomy":"$economy_Refinery;", "SystemSecondEconomy_Localised":"Refinery", "SystemGovernment":"$government_PrisonColony;", "SystemGovernment_Localised":"Prison colony", "SystemSecurity":"$SYSTEM_SECURITY_medium;", "SystemSecurity_Localised":"Medium Security", "Population":446938, "Body":"HR 1597 A 1", "BodyID":3, "BodyType":"Planet", "Powers":[ "A. Lavigny-Duval" ], "PowerplayState":"Exploited", "Factions":[ { "Name":"HR 1597 Empire Party", "FactionState":"None", "Government":"Patronage", "Influence":0.010142, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"Co-operative of Shambogi", "FactionState":"None", "Government":"Cooperative", "Influence":0.041582, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"HR 1597 Crimson Comms Network", "FactionState":"None", "Government":"Corporate", "Influence":0.064909, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":23.330000 }, { "Name":"Social HR 1597 Values Party", "FactionState":"None", "Government":"Democracy", "Influence":0.063895, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":20.280001 }, { "Name":"HR 1597 Crimson Brotherhood", "FactionState":"None", "Government":"Anarchy", "Influence":0.010142, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":67.239998 }, { "Name":"HR 1597 & Co", "FactionState":"War", "Government":"Corporate", "Influence":0.404665, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000, "ActiveStates":[ { "State":"War" } ] }, { "Name":"EDA Kunti League", "FactionState":"War", "Government":"PrisonColony", "Influence":0.404665, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "SquadronFaction":True, "MyReputation":100.000000, "ActiveStates":[ { "State":"Boom" }, { "State":"War" } ] } ], "SystemFaction":{ "Name":"EDA Kunti League", "FactionState":"War" }, "Conflicts":[ { "WarType":"war", "Status":"active", "Faction1":{ "Name":"HR 1597 & Co", "Stake":"Elst Prospect", "WonDays":0 }, "Faction2":{ "Name":"EDA Kunti League", "Stake":"Jean City", "WonDays":1 } } ] }, 
            Station("Q3H-7HT", 869487593835, "FleetCarrier"),
            StarSystem("HR 1597", 869487593835, ["HR 1597 Empire Party", "Co-operative of Shambogi", "HR 1597 Crimson Comms Network", "Social HR 1597 Values Party", "HR 1597 Crimson Brotherhood", "HR 1597 & Co", "EDA Kunti League"])
        ),
        (
            { "timestamp": "2020-12-30T02:28:17Z", "event": "Location", "Docked": False, "StarSystem": "HIP 58121", "SystemAddress":285388835187, "StarPos":[118.18750,-10.21875,61.90625], "SystemAllegiance":"", "SystemEconomy":"$economy_None;", "SystemEconomy_Localised":"None", "SystemSecondEconomy":"$economy_None;", "SystemSecondEconomy_Localised":"None", "SystemGovernment":"$government_None;", "SystemGovernment_Localised":"None", "SystemSecurity":"$GAlAXY_MAP_INFO_state_anarchy;", "SystemSecurity_Localised":"Anarchy", "Population":0, "Body":"HIP 58121 A 4", "BodyID":16, "BodyType":"Planet" }, 
            None,
            None, # StarSystem("HIP 58121", 285388835187, []) # No factions for a fleet carrier, therefore ignore
        ),
        (
            { "timestamp":"2020-12-07T10:05:58Z", "event":"Location", "Docked":True, "StationName":"Sabine Installation", "StationType":"CraterOutpost", "MarketID":3516792064, "StationFaction":{ "Name":"CD-51 2650 Guardians", "FactionState":"Drought" }, "StationGovernment":"$government_Patronage;", "StationGovernment_Localised":"Patronage", "StationAllegiance":"Empire", "StationServices":[ "dock", "autodock", "commodities", "contacts", "exploration", "missions", "outfitting", "crewlounge", "rearm", "refuel", "repair", "tuning", "engineer", "missionsgenerated", "facilitator", "flightcontroller", "stationoperations", "powerplay", "searchrescue", "stationMenu", "shop" ], "StationEconomy":"$economy_Colony;", "StationEconomy_Localised":"Colony", "StationEconomies":[ { "Name":"$economy_Colony;", "Name_Localised":"Colony", "Proportion":1.000000 } ], "StarSystem":"Arun", "SystemAddress":4482100335314, "StarPos":[105.25000,-46.62500,-10.40625], "SystemAllegiance":"Independent", "SystemEconomy":"$economy_Colony;", "SystemEconomy_Localised":"Colony", "SystemSecondEconomy":"$economy_Extraction;", "SystemSecondEconomy_Localised":"Extraction", "SystemGovernment":"$government_PrisonColony;", "SystemGovernment_Localised":"Prison colony", "SystemSecurity":"$SYSTEM_SECURITY_low;", "SystemSecurity_Localised":"Low Security", "Population":2542, "Body":"Arun B 4 a", "BodyID":43, "BodyType":"Planet", "Factions":[ { "Name":"Progressive Party of LTT 2684", "FactionState":"None", "Government":"Democracy", "Influence":0.044599, "Allegiance":"Federation", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":6.600000, "RecoveringStates":[ { "State":"PirateAttack", "Trend":0 } ] }, { "Name":"Arun Organisation", "FactionState":"None", "Government":"Corporate", "Influence":0.042616, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":0.000000 }, { "Name":"Antai Energy Group", "FactionState":"Retreat", "Government":"Corporate", "Influence":0.154609, "Allegiance":"Federation", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":45.869999, "ActiveStates":[ { "State":"Retreat" } ] }, { "Name":"Arun Gold Partnership", "FactionState":"Lockdown", "Government":"Anarchy", "Influence":0.009911, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand3;", "Happiness_Localised":"Discontented", "MyReputation":0.000000, "ActiveStates":[ { "State":"Lockdown" }, { "State":"Bust" }, { "State":"Drought" } ] }, { "Name":"CD-51 2650 Guardians", "FactionState":"Drought", "Government":"Patronage", "Influence":0.188305, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":15.000000, "ActiveStates":[ { "State":"Drought" } ] }, { "Name":"Friends of Arun", "FactionState":"None", "Government":"Cooperative", "Influence":0.038652, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":0.000000 }, { "Name":"EDA Kunti League", "FactionState":"Boom", "Government":"PrisonColony", "Influence":0.521308, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "SquadronFaction":True, "MyReputation":100.000000, "ActiveStates":[ { "State":"Boom" }, { "State":"CivilLiberty" }, { "State":"PublicHoliday" } ] } ], "SystemFaction":{ "Name":"EDA Kunti League", "FactionState":"Boom" } }, 
            Station("Sabine Installation", 4482100335314, "CD-51 2650 Guardians"),
            StarSystem("Arun", 4482100335314, ["Progressive Party of LTT 2684", "Arun Organisation", "Antai Energy Group", "Arun Gold Partnership", "CD-51 2650 Guardians", "Friends of Arun", "EDA Kunti League"])
        ),
        (
            { "timestamp":"2020-10-19T11:23:02Z", "event":"FSDJump", "StarSystem":"Kokobii", "SystemAddress":3657399472850, "StarPos":[83.59375,-69.46875,-9.78125], "SystemAllegiance":"Empire", "SystemEconomy":"$economy_HighTech;", "SystemEconomy_Localised":"High Tech", "SystemSecondEconomy":"$economy_Refinery;", "SystemSecondEconomy_Localised":"Refinery", "SystemGovernment":"$government_Patronage;", "SystemGovernment_Localised":"Patronage", "SystemSecurity":"$SYSTEM_SECURITY_high;", "SystemSecurity_Localised":"High Security", "Population":18362954, "Body":"Kokobii A", "BodyID":1, "BodyType":"Star", "Powers":[ "A. Lavigny-Duval" ], "PowerplayState":"Exploited", "JumpDist":11.972, "FuelUsed":0.828394, "FuelLevel":31.171606, "Factions":[ { "Name":"Kokobii Empire League", "FactionState":"Boom", "Government":"Patronage", "Influence":0.621242, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":49.579399, "ActiveStates":[ { "State":"Boom" } ] }, { "Name":"Kokobii Power Company", "FactionState":"None", "Government":"Corporate", "Influence":0.061122, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":0.000000 }, { "Name":"New Kokobii Resistance", "FactionState":"None", "Government":"Democracy", "Influence":0.048096, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":0.000000 }, { "Name":"Kokobii Silver Brothers", "FactionState":"None", "Government":"Anarchy", "Influence":0.022044, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":0.000000 }, { "Name":"San Davokje Transport Company", "FactionState":"War", "Government":"Corporate", "Influence":0.097194, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":8.250000, "ActiveStates":[ { "State":"War" } ] }, { "Name":"Kokobii Empire Pact", "FactionState":"None", "Government":"Patronage", "Influence":0.053106, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":0.000000 }, { "Name":"HYDRIUM CORPORATION", "FactionState":"War", "Government":"Dictatorship", "Influence":0.097194, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":0.000000, "ActiveStates":[ { "State":"War" } ] } ], "SystemFaction":{ "Name":"Kokobii Empire League", "FactionState":"Boom" }, "Conflicts":[ { "WarType":"war", "Status":"active", "Faction1":{ "Name":"San Davokje Transport Company", "Stake":"Kranz Gateway", "WonDays":3 }, "Faction2":{ "Name":"HYDRIUM CORPORATION", "Stake":"Martins Installation", "WonDays":3 } } ] },
            None,
            StarSystem("Kokobii", 3657399472850, ["Kokobii Empire League", "HYDRIUM CORPORATION", "Kokobii Empire Pact", "San Davokje Transport Company", "Kokobii Silver Brothers", "New Kokobii Resistance", "Kokobii Power Company"])
        )
    ])
def test_location_single(location_event: Dict[str, Any], expected_station: Station, expected_system: StarSystem):
    location_event_processor = LocationEventProcessor()
    pilot_state = PilotState()
    galaxy_state = GalaxyState()

    assert not location_event_processor.process(location_event, pilot_state, galaxy_state)

    expected_pilot_state = PilotState()
    if expected_station:
        expected_pilot_state.last_docked_station = expected_station
    expected_pilot_state.system_address = location_event["SystemAddress"]
    assert pilot_state == expected_pilot_state

    expected_galaxy_state = GalaxyState()
    if expected_system:
        expected_galaxy_state.systems[expected_system.address] = expected_system
    assert galaxy_state == expected_galaxy_state


@pytest.mark.parametrize(
    "location_events, expected_station",
    [
        (
            (
                { "timestamp":"2020-12-30T01:04:56Z", "event":"Location", "Docked":True, "StationName":"Q3H-7HT", "StationType":"FleetCarrier", "MarketID":3703794688, "StationFaction":{ "Name":"FleetCarrier" }, "StationGovernment":"$government_Carrier;", "StationGovernment_Localised":"Private Ownership ", "StationServices":[ "dock", "autodock", "commodities", "contacts", "outfitting", "crewlounge", "rearm", "refuel", "repair", "shipyard", "engineer", "flightcontroller", "stationoperations", "stationMenu", "carriermanagement", "carrierfuel", "voucherredemption" ], "StationEconomy":"$economy_Carrier;", "StationEconomy_Localised":"Private Enterprise", "StationEconomies":[ { "Name":"$economy_Carrier;", "Name_Localised":"Private Enterprise", "Proportion":1.000000 } ], "StarSystem":"HR 1597", "SystemAddress":869487593835, "StarPos":[78.18750,-60.87500,-3.43750], "SystemAllegiance":"Independent", "SystemEconomy":"$economy_Military;", "SystemEconomy_Localised":"Military", "SystemSecondEconomy":"$economy_Refinery;", "SystemSecondEconomy_Localised":"Refinery", "SystemGovernment":"$government_PrisonColony;", "SystemGovernment_Localised":"Prison colony", "SystemSecurity":"$SYSTEM_SECURITY_medium;", "SystemSecurity_Localised":"Medium Security", "Population":446938, "Body":"HR 1597 A 1", "BodyID":3, "BodyType":"Planet", "Powers":[ "A. Lavigny-Duval" ], "PowerplayState":"Exploited", "Factions":[ { "Name":"HR 1597 Empire Party", "FactionState":"None", "Government":"Patronage", "Influence":0.010142, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"Co-operative of Shambogi", "FactionState":"None", "Government":"Cooperative", "Influence":0.041582, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"HR 1597 Crimson Comms Network", "FactionState":"None", "Government":"Corporate", "Influence":0.064909, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":23.330000 }, { "Name":"Social HR 1597 Values Party", "FactionState":"None", "Government":"Democracy", "Influence":0.063895, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":20.280001 }, { "Name":"HR 1597 Crimson Brotherhood", "FactionState":"None", "Government":"Anarchy", "Influence":0.010142, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":67.239998 }, { "Name":"HR 1597 & Co", "FactionState":"War", "Government":"Corporate", "Influence":0.404665, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000, "ActiveStates":[ { "State":"War" } ] }, { "Name":"EDA Kunti League", "FactionState":"War", "Government":"PrisonColony", "Influence":0.404665, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "SquadronFaction":True, "MyReputation":100.000000, "ActiveStates":[ { "State":"Boom" }, { "State":"War" } ] } ], "SystemFaction":{ "Name":"EDA Kunti League", "FactionState":"War" }, "Conflicts":[ { "WarType":"war", "Status":"active", "Faction1":{ "Name":"HR 1597 & Co", "Stake":"Elst Prospect", "WonDays":0 }, "Faction2":{ "Name":"EDA Kunti League", "Stake":"Jean City", "WonDays":1 } } ] },
                { "timestamp":"2020-12-30T02:28:17Z", "event":"Location", "Docked":False, "StarSystem":"HIP 58121", "SystemAddress":285388835187, "StarPos":[118.18750,-10.21875,61.90625], "SystemAllegiance":"", "SystemEconomy":"$economy_None;", "SystemEconomy_Localised":"None", "SystemSecondEconomy":"$economy_None;", "SystemSecondEconomy_Localised":"None", "SystemGovernment":"$government_None;", "SystemGovernment_Localised":"None", "SystemSecurity":"$GAlAXY_MAP_INFO_state_anarchy;", "SystemSecurity_Localised":"Anarchy", "Population":0, "Body":"HIP 58121 A 4", "BodyID":16, "BodyType":"Planet" }
            ),
            Station("Q3H-7HT", 869487593835, "FleetCarrier")
        ),
        (
            (
                { "timestamp":"2020-12-30T02:28:17Z", "event":"Location", "Docked":False, "StarSystem":"HIP 58121", "SystemAddress":285388835187, "StarPos":[118.18750,-10.21875,61.90625], "SystemAllegiance":"", "SystemEconomy":"$economy_None;", "SystemEconomy_Localised":"None", "SystemSecondEconomy":"$economy_None;", "SystemSecondEconomy_Localised":"None", "SystemGovernment":"$government_None;", "SystemGovernment_Localised":"None", "SystemSecurity":"$GAlAXY_MAP_INFO_state_anarchy;", "SystemSecurity_Localised":"Anarchy", "Population":0, "Body":"HIP 58121 A 4", "BodyID":16, "BodyType":"Planet" },
                { "timestamp":"2020-12-30T01:04:56Z", "event":"Location", "Docked":True, "StationName":"Q3H-7HT", "StationType":"FleetCarrier", "MarketID":3703794688, "StationFaction":{ "Name":"FleetCarrier" }, "StationGovernment":"$government_Carrier;", "StationGovernment_Localised":"Private Ownership ", "StationServices":[ "dock", "autodock", "commodities", "contacts", "outfitting", "crewlounge", "rearm", "refuel", "repair", "shipyard", "engineer", "flightcontroller", "stationoperations", "stationMenu", "carriermanagement", "carrierfuel", "voucherredemption" ], "StationEconomy":"$economy_Carrier;", "StationEconomy_Localised":"Private Enterprise", "StationEconomies":[ { "Name":"$economy_Carrier;", "Name_Localised":"Private Enterprise", "Proportion":1.000000 } ], "StarSystem":"HR 1597", "SystemAddress":869487593835, "StarPos":[78.18750,-60.87500,-3.43750], "SystemAllegiance":"Independent", "SystemEconomy":"$economy_Military;", "SystemEconomy_Localised":"Military", "SystemSecondEconomy":"$economy_Refinery;", "SystemSecondEconomy_Localised":"Refinery", "SystemGovernment":"$government_PrisonColony;", "SystemGovernment_Localised":"Prison colony", "SystemSecurity":"$SYSTEM_SECURITY_medium;", "SystemSecurity_Localised":"Medium Security", "Population":446938, "Body":"HR 1597 A 1", "BodyID":3, "BodyType":"Planet", "Powers":[ "A. Lavigny-Duval" ], "PowerplayState":"Exploited", "Factions":[ { "Name":"HR 1597 Empire Party", "FactionState":"None", "Government":"Patronage", "Influence":0.010142, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"Co-operative of Shambogi", "FactionState":"None", "Government":"Cooperative", "Influence":0.041582, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"HR 1597 Crimson Comms Network", "FactionState":"None", "Government":"Corporate", "Influence":0.064909, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":23.330000 }, { "Name":"Social HR 1597 Values Party", "FactionState":"None", "Government":"Democracy", "Influence":0.063895, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":20.280001 }, { "Name":"HR 1597 Crimson Brotherhood", "FactionState":"None", "Government":"Anarchy", "Influence":0.010142, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":67.239998 }, { "Name":"HR 1597 & Co", "FactionState":"War", "Government":"Corporate", "Influence":0.404665, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000, "ActiveStates":[ { "State":"War" } ] }, { "Name":"EDA Kunti League", "FactionState":"War", "Government":"PrisonColony", "Influence":0.404665, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "SquadronFaction":True, "MyReputation":100.000000, "ActiveStates":[ { "State":"Boom" }, { "State":"War" } ] } ], "SystemFaction":{ "Name":"EDA Kunti League", "FactionState":"War" }, "Conflicts":[ { "WarType":"war", "Status":"active", "Faction1":{ "Name":"HR 1597 & Co", "Stake":"Elst Prospect", "WonDays":0 }, "Faction2":{ "Name":"EDA Kunti League", "Stake":"Jean City", "WonDays":1 } } ] },
            ),
            Station("Q3H-7HT", 869487593835, "FleetCarrier")
        ),
        (
            (
                { "timestamp": "2020-12-30T01:04:56Z", "event": "Location", "Docked": True, "StationName": "Q3H-7HT", "StationType": "FleetCarrier", "MarketID": 3703794688, "StationFaction": { "Name": "FleetCarrier" }, "StationGovernment": "$government_Carrier;", "StationGovernment_Localised": "Private Ownership ", "StationServices": [ "dock", "autodock", "commodities", "contacts", "outfitting", "crewlounge", "rearm", "refuel", "repair", "shipyard", "engineer", "flightcontroller", "stationoperations", "stationMenu", "carriermanagement", "carrierfuel", "voucherredemption" ], "StationEconomy": "$economy_Carrier;", "StationEconomy_Localised":"Private Enterprise", "StationEconomies":[ { "Name":"$economy_Carrier;", "Name_Localised":"Private Enterprise", "Proportion":1.000000 } ], "StarSystem":"HR 1597", "SystemAddress":869487593835, "StarPos":[78.18750,-60.87500,-3.43750], "SystemAllegiance":"Independent", "SystemEconomy":"$economy_Military;", "SystemEconomy_Localised":"Military", "SystemSecondEconomy":"$economy_Refinery;", "SystemSecondEconomy_Localised":"Refinery", "SystemGovernment":"$government_PrisonColony;", "SystemGovernment_Localised":"Prison colony", "SystemSecurity":"$SYSTEM_SECURITY_medium;", "SystemSecurity_Localised":"Medium Security", "Population":446938, "Body":"HR 1597 A 1", "BodyID":3, "BodyType":"Planet", "Powers":[ "A. Lavigny-Duval" ], "PowerplayState":"Exploited", "Factions":[ { "Name":"HR 1597 Empire Party", "FactionState":"None", "Government":"Patronage", "Influence":0.010142, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"Co-operative of Shambogi", "FactionState":"None", "Government":"Cooperative", "Influence":0.041582, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"HR 1597 Crimson Comms Network", "FactionState":"None", "Government":"Corporate", "Influence":0.064909, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":23.330000 }, { "Name":"Social HR 1597 Values Party", "FactionState":"None", "Government":"Democracy", "Influence":0.063895, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":20.280001 }, { "Name":"HR 1597 Crimson Brotherhood", "FactionState":"None", "Government":"Anarchy", "Influence":0.010142, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":67.239998 }, { "Name":"HR 1597 & Co", "FactionState":"War", "Government":"Corporate", "Influence":0.404665, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000, "ActiveStates":[ { "State":"War" } ] }, { "Name":"EDA Kunti League", "FactionState":"War", "Government":"PrisonColony", "Influence":0.404665, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "SquadronFaction":True, "MyReputation":100.000000, "ActiveStates":[ { "State":"Boom" }, { "State":"War" } ] } ], "SystemFaction":{ "Name":"EDA Kunti League", "FactionState":"War" }, "Conflicts":[ { "WarType":"war", "Status":"active", "Faction1":{ "Name":"HR 1597 & Co", "Stake":"Elst Prospect", "WonDays":0 }, "Faction2":{ "Name":"EDA Kunti League", "Stake":"Jean City", "WonDays":1 } } ] },
                { "timestamp": "2020-12-30T02:28:17Z", "event": "Location", "Docked": False, "StarSystem": "HIP 58121", "SystemAddress": 285388835187, "StarPos": [118.18750,-10.21875,61.90625], "SystemAllegiance": "", "SystemEconomy": "$economy_None;", "SystemEconomy_Localised": "None", "SystemSecondEconomy": "$economy_None;", "SystemSecondEconomy_Localised": "None", "SystemGovernment": "$government_None;", "SystemGovernment_Localised": "None", "SystemSecurity": "$GAlAXY_MAP_INFO_state_anarchy;", "SystemSecurity_Localised": "Anarchy", "Population": 0, "Body": "HIP 58121 A 4", "BodyID": 16, "BodyType": "Planet" },
                { "timestamp": "2020-12-07T10:05:58Z", "event": "Location", "Docked": True, "StationName": "Sabine Installation", "StationType": "CraterOutpost", "MarketID": 3516792064, "StationFaction": { "Name": "CD-51 2650 Guardians", "FactionState": "Drought" }, "StationGovernment": "$government_Patronage;", "StationGovernment_Localised": "Patronage", "StationAllegiance": "Empire", "StationServices": [ "dock", "autodock", "commodities", "contacts", "exploration", "missions", "outfitting", "crewlounge", "rearm", "refuel", "repair", "tuning", "engineer", "missionsgenerated", "facilitator", "flightcontroller", "stationoperations", "powerplay", "searchrescue", "stationMenu", "shop" ], "StationEconomy":"$economy_Colony;", "StationEconomy_Localised":"Colony", "StationEconomies":[ { "Name":"$economy_Colony;", "Name_Localised":"Colony", "Proportion":1.000000 } ], "StarSystem":"Arun", "SystemAddress":4482100335314, "StarPos":[105.25000,-46.62500,-10.40625], "SystemAllegiance":"Independent", "SystemEconomy":"$economy_Colony;", "SystemEconomy_Localised":"Colony", "SystemSecondEconomy":"$economy_Extraction;", "SystemSecondEconomy_Localised":"Extraction", "SystemGovernment":"$government_PrisonColony;", "SystemGovernment_Localised":"Prison colony", "SystemSecurity":"$SYSTEM_SECURITY_low;", "SystemSecurity_Localised":"Low Security", "Population":2542, "Body":"Arun B 4 a", "BodyID":43, "BodyType":"Planet", "Factions":[ { "Name":"Progressive Party of LTT 2684", "FactionState":"None", "Government":"Democracy", "Influence":0.044599, "Allegiance":"Federation", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":6.600000, "RecoveringStates":[ { "State":"PirateAttack", "Trend":0 } ] }, { "Name":"Arun Organisation", "FactionState":"None", "Government":"Corporate", "Influence":0.042616, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":0.000000 }, { "Name":"Antai Energy Group", "FactionState":"Retreat", "Government":"Corporate", "Influence":0.154609, "Allegiance":"Federation", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":45.869999, "ActiveStates":[ { "State":"Retreat" } ] }, { "Name":"Arun Gold Partnership", "FactionState":"Lockdown", "Government":"Anarchy", "Influence":0.009911, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand3;", "Happiness_Localised":"Discontented", "MyReputation":0.000000, "ActiveStates":[ { "State":"Lockdown" }, { "State":"Bust" }, { "State":"Drought" } ] }, { "Name":"CD-51 2650 Guardians", "FactionState":"Drought", "Government":"Patronage", "Influence":0.188305, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":15.000000, "ActiveStates":[ { "State":"Drought" } ] }, { "Name":"Friends of Arun", "FactionState":"None", "Government":"Cooperative", "Influence":0.038652, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":0.000000 }, { "Name":"EDA Kunti League", "FactionState":"Boom", "Government":"PrisonColony", "Influence":0.521308, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "SquadronFaction":True, "MyReputation":100.000000, "ActiveStates":[ { "State":"Boom" }, { "State":"CivilLiberty" }, { "State":"PublicHoliday" } ] } ], "SystemFaction":{ "Name":"EDA Kunti League", "FactionState":"Boom" } }
            ),
            Station("Sabine Installation", 4482100335314, "CD-51 2650 Guardians")
        )
    ])
def test_location_sequence(location_events: Tuple, expected_station: Station):
    location_event_processor = LocationEventProcessor()
    pilot_state = PilotState()
    galaxy_state = GalaxyState()
    for location_event in location_events:
        assert not location_event_processor.process(location_event, pilot_state, galaxy_state)
    assert pilot_state.last_docked_station == expected_station


@pytest.mark.parametrize(
    "star_system, last_docked_station, redeem_voucher_event, expected_results",
    [
        # Bounty
        (
            StarSystem("Fuelum", 1000, ("The Fuel Rats Mischief",)),
            Station("Station", 1000, "The Fuel Rats Mischief"),
            {"timestamp": "2020-05-09T04:43:16Z", "event": "RedeemVoucher", "Type": "bounty", "Amount": 42350, "Factions": [ { "Faction": "The Fuel Rats Mischief", "Amount": 42350 } ] },
            [RedeemVoucherEventSummary("Fuelum", {"The Fuel Rats Mischief"}, {}, "bounty", 42350)]
        ),
        (
            StarSystem("Fuelum", 1000, ("The Fuel Rats Mischief", "Findja Empire Assembly")),
            Station("Station", 1000, "The Fuel Rats Mischief"),
            {"timestamp": "2020-05-09T03:42:20Z", "event": "RedeemVoucher", "Type": "bounty", "Amount": 25490, "Factions": [ { "Faction": "Findja Empire Assembly", "Amount": 25490 } ] },
            [RedeemVoucherEventSummary("Fuelum", {"Findja Empire Assembly"}, {"The Fuel Rats Mischief"}, "bounty", 25490)]
        ),
        (
            StarSystem("Findja", 1000, ("The Fuel Rats Mischief",)),
            Station("Station", 1000, "The Fuel Rats Mischief"),
            {"timestamp": "2020-05-09T03:42:31Z", "event": "RedeemVoucher", "Type": "bounty", "Amount": 13338, "Factions":[ { "Faction":"", "Amount":13338 } ], "BrokerPercentage": 25.000000 },
            []
        ),
        (
            StarSystem("CPD-59 314", 1000, ("The Fuel Rats Mischief", "CPD-59 314 Imperial Society")),
            Station("Station", 1000, "The Fuel Rats Mischief"),
            {"timestamp": "2020-10-15T14:45:16Z", "event": "RedeemVoucher", "Type": "bounty", "Amount": 1779467, "Factions": [ { "Faction": "CPD-59 314 Imperial Society", "Amount": 1779467 } ], "BrokerPercentage":25.000000 },
            []
        ),
        (
            StarSystem("Fuelum", 1000, ("The Fuel Rats Mischief", "Rabh Empire Pact", "Kacomam Empire Group", "Trumuye Emperor's Grace", "EDA Kunti League")),
            Station("Station", 1000, "The Fuel Rats Mischief"),
            {"timestamp": "2020-12-13T02:02:04Z", "event": "RedeemVoucher", "Type": "bounty", "Amount": 5924586, "Factions": [ { "Faction": "Rabh Empire Pact", "Amount": 385660 }, { "Faction": "Kacomam Empire Group", "Amount": 666873 }, { "Faction": "Trumuye Emperor's Grace", "Amount": 545094 }, { "Faction": "EDA Kunti League", "Amount": 4326959 } ] },
            [
                RedeemVoucherEventSummary("Fuelum", {"Rabh Empire Pact"}, {"The Fuel Rats Mischief", "Kacomam Empire Group", "Trumuye Emperor's Grace", "EDA Kunti League"}, "bounty", 385660),
                RedeemVoucherEventSummary("Fuelum", {"Kacomam Empire Group"}, {"The Fuel Rats Mischief", "Rabh Empire Pact", "Trumuye Emperor's Grace", "EDA Kunti League"}, "bounty", 666873),
                RedeemVoucherEventSummary("Fuelum", {"Trumuye Emperor's Grace"}, {"The Fuel Rats Mischief", "Rabh Empire Pact", "Kacomam Empire Group", "EDA Kunti League"}, "bounty", 545094),
                RedeemVoucherEventSummary("Fuelum", {"EDA Kunti League"}, {"The Fuel Rats Mischief", "Rabh Empire Pact", "Kacomam Empire Group", "Trumuye Emperor's Grace"}, "bounty", 4326959)
            ]
        ),

        # Combat Bond
        (
            StarSystem("", 1000, ("The Fuel Rats Mischief", "EDA Kunti League")),
            Station("", 1000, "The Fuel Rats Mischief"),
            {"timestamp":"2020-11-27T11:46:17Z", "event":"RedeemVoucher", "Type":"CombatBond", "Amount":1622105, "Faction":"EDA Kunti League" },
            [RedeemVoucherEventSummary("", {"EDA Kunti League"}, {"The Fuel Rats Mischief"}, "CombatBond", 1622105)]
        ),
        (
            StarSystem("", 1000, ("The Fuel Rats Mischief", "CPD-59 314 Imperial Society")),
            Station("", 1000, "The Fuel Rats Mischief"),
            {"timestamp":"2020-10-31T14:56:09Z", "event":"RedeemVoucher", "Type":"CombatBond", "Amount":1177365, "Faction":"CPD-59 314 Imperial Society" },
            [RedeemVoucherEventSummary("", {"CPD-59 314 Imperial Society"}, {"The Fuel Rats Mischief"}, "CombatBond", 1177365)]
        ),
        (
            StarSystem("", 1000, ("The Fuel Rats Mischief",)),
            Station("", 1000, "The Fuel Rats Mischief"),
            {"timestamp":"2020-10-18T11:23:57Z", "event":"RedeemVoucher", "Type":"CombatBond", "Amount":1127126, "Faction":"HR 1597 & Co", "BrokerPercentage":25.000000 },
            [RedeemVoucherEventSummary("", {"HR 1597 & Co"}, set(), "CombatBond", 1502835)]
        ),
        (
            StarSystem("", 1000, ("The Fuel Rats Mischief",)),
            Station("", 1000, "The Fuel Rats Mischief"),
            {"timestamp":"2020-07-17T15:21:20Z", "event":"RedeemVoucher", "Type":"CombatBond", "Amount":46026, "Faction":"", "BrokerPercentage":25.000000 },
            [RedeemVoucherEventSummary("", {""}, set(), "CombatBond", 61368)]
        ),
        (
            StarSystem("", 1000, ("The Fuel Rats Mischief", "HR 1597 & Co")),
            Station("", 1000, "The Fuel Rats Mischief"),
            {"timestamp":"2020-10-18T11:23:57Z", "event":"RedeemVoucher", "Type":"CombatBond", "Amount":1127126, "Faction":"HR 1597 & Co", "BrokerPercentage":25.000000 },
            [RedeemVoucherEventSummary("", {"HR 1597 & Co"}, {"The Fuel Rats Mischief"}, "CombatBond", 1502835)]
        ),
        (
            StarSystem("", 1000, ("The Fuel Rats Mischief",)),
            Station("", 1000, "The Fuel Rats Mischief"),
            {"timestamp":"2020-07-17T15:21:20Z", "event":"RedeemVoucher", "Type":"CombatBond", "Amount":1000, "Faction":"", "BrokerPercentage":0.000000 },
            [RedeemVoucherEventSummary("", {""}, set(), "CombatBond", 1000)]
        ),
        (
            StarSystem("", 1000, ("The Fuel Rats Mischief",)),
            Station("", 1000, "The Fuel Rats Mischief"),
            {"timestamp":"2020-07-17T15:21:20Z", "event":"RedeemVoucher", "Type":"CombatBond", "Amount":1000, "Faction":"", "BrokerPercentage":1.000000 },
            [RedeemVoucherEventSummary("", {""}, set(), "CombatBond", 1010)]
        ),
        (
            StarSystem("", 1000, ("The Fuel Rats Mischief",)),
            Station("", 1000, "The Fuel Rats Mischief"),
            {"timestamp":"2020-07-17T15:21:20Z", "event":"RedeemVoucher", "Type":"CombatBond", "Amount":1000, "Faction":"", "BrokerPercentage":99.000000 },
            [RedeemVoucherEventSummary("", {""}, set(), "CombatBond", 100000)]
        ),
        (
            StarSystem("", 1000, ("The Fuel Rats Mischief",)),
            Station("", 1000, "The Fuel Rats Mischief"),
            {"timestamp":"2020-07-17T15:21:20Z", "event":"RedeemVoucher", "Type":"CombatBond", "Amount":1000, "Faction":"", "BrokerPercentage":100.000000 },
            [RedeemVoucherEventSummary("", {""}, set(), "CombatBond", 1000)]
        ),

        # Scannable (Not sure what this is)
        # (
        #     "The Fuel Rats Mischief",
        #     StarSystem("Fuelum", 1000, ("The Fuel Rats Mischief",)),
        #     Station("", 1000, "The Fuel Rats Mischief"),
        #     { "timestamp":"2020-07-05T15:09:48Z", "event":"RedeemVoucher", "Type":"scannable", "Amount":206078, "Faction":"" },
        #     [RedeemVoucherEventSummary("Fuelum", True, "scannable", 206078)]
        # ),
        # (
        #     "The Fuel Rats Mischief",
        #     StarSystem("Fuelum", 1000, ("The Fuel Rats Mischief",)),
        #     Station("", 1000, "The Dark Wheel"),
        #     { "timestamp":"2020-07-05T15:09:48Z", "event":"RedeemVoucher", "Type":"scannable", "Amount":206078, "Faction":"" },
        #     []
        # ),
        # (
        #     "The Fuel Rats Mischief",
        #     StarSystem("Fuelum", 1000, ("The Fuel Rats Mischief", "The Dark Wheel")),
        #     Station("", 1000, "The Dark Wheel"),
        #     { "timestamp":"2020-07-05T15:09:48Z", "event":"RedeemVoucher", "Type":"scannable", "Amount":206078, "Faction":"" },
        #     [RedeemVoucherEventSummary("Fuelum", False, "scannable", 206078)]
        # ),

        # BGS irrelevant types
        (
            StarSystem("", 1000, ("The Fuel Rats Mischief",)),
            Station("", 1000, "The Fuel Rats Mischief"),
            { "timestamp":"2020-07-05T10:26:31Z", "event":"RedeemVoucher", "Type":"codex", "Amount":5000, "Faction":"" },
            []
        ),
        (
            StarSystem("", 1000, ("The Fuel Rats Mischief",)),
            Station("", 1000, "The Fuel Rats Mischief"),
            { "timestamp":"2020-12-27T07:48:49Z", "event":"RedeemVoucher", "Type":"settlement", "Amount":4352, "Faction":"" },
            []
        ),
    ])
def test_redeem_voucher_single(star_system:StarSystem, last_docked_station: Station, redeem_voucher_event: Dict[str, Any], expected_results: list):
    pilot_state = PilotState()
    pilot_state.last_docked_station = last_docked_station
    pilot_state.system_address = last_docked_station.system_address
    galaxy_state = GalaxyState()
    galaxy_state.systems[star_system.address] = star_system
    expected_pilot_state = copy.deepcopy(pilot_state)
    expected_galaxy_state = copy.deepcopy(galaxy_state)

    redeem_voucher_event_processor:RedeemVoucherEventProcessor = RedeemVoucherEventProcessor()
    results = redeem_voucher_event_processor.process(redeem_voucher_event, pilot_state, galaxy_state)

    assert results == expected_results
    assert pilot_state == expected_pilot_state
    assert galaxy_state == expected_galaxy_state

@pytest.mark.parametrize(
    "docked_event, expected_station",
    [
        (
            { "timestamp":"2020-10-19T11:16:16Z", "event":"Docked", "StationName":"Jean City", "StationType":"Outpost", "StarSystem":"HR 1597", "SystemAddress":869487593835, "MarketID":3223702528, "StationFaction":{ "Name":"HR 1597 & Co" }, "StationGovernment":"$government_Corporate;", "StationGovernment_Localised":"Corporate", "StationAllegiance":"Empire", "StationServices":[ "dock", "autodock", "commodities", "contacts", "exploration", "missions", "rearm", "refuel", "repair", "tuning", "engineer", "missionsgenerated", "flightcontroller", "stationoperations", "powerplay", "searchrescue", "stationMenu" ], "StationEconomy":"$economy_Refinery;", "StationEconomy_Localised":"Refinery", "StationEconomies":[ { "Name":"$economy_Refinery;", "Name_Localised":"Refinery", "Proportion":0.810000 }, { "Name":"$economy_Extraction;", "Name_Localised":"Extraction", "Proportion":0.190000 } ], "DistFromStarLS":170.514980 }, 
            Station("Jean City", 869487593835, "HR 1597 & Co")
        ),
        (
            { "timestamp":"2020-10-19T11:27:21Z", "event":"Docked", "StationName":"Anderson Hub", "StationType":"Outpost", "StarSystem":"Kokobii", "SystemAddress":3657399472850, "MarketID":3223765504, "StationFaction":{ "Name":"San Davokje Transport Company", "FactionState":"War" }, "StationGovernment":"$government_Corporate;", "StationGovernment_Localised":"Corporate", "StationAllegiance":"Empire", "StationServices":[ "dock", "autodock", "commodities", "contacts", "exploration", "missions", "outfitting", "crewlounge", "rearm", "refuel", "repair", "tuning", "engineer", "missionsgenerated", "flightcontroller", "stationoperations", "powerplay", "searchrescue", "stationMenu" ], "StationEconomy":"$economy_HighTech;", "StationEconomy_Localised":"High Tech", "StationEconomies":[ { "Name":"$economy_HighTech;", "Name_Localised":"High Tech", "Proportion":0.510000 }, { "Name":"$economy_Refinery;", "Name_Localised":"Refinery", "Proportion":0.490000 } ], "DistFromStarLS":2990.366866 },
            Station("Anderson Hub", 3657399472850, "San Davokje Transport Company")
        )
    ])
def test_docked_single(docked_event: Dict[str, Any], expected_station: Station):
    docked_event_processor = DockedEventProcessor()
    pilot_state = PilotState()
    galaxy_state = GalaxyState()
    assert not docked_event_processor.process(docked_event, pilot_state, galaxy_state)
    assert pilot_state.last_docked_station == expected_station


@pytest.mark.parametrize(
   "star_system, last_docked_station, sell_exploration_data_event, expected_results",
    [
        (
            StarSystem("HR 1597", 1000, ("EDA Kunti League", "HR 1597 & Co")),
            Station("Elsa Prospect", 1000, "HR 1597 & Co"),
            {"timestamp":"2020-05-15T13:13:38Z", "event":"MultiSellExplorationData", "Discovered":[ { "SystemName":"Shui Wei Sector PO-Q b5-1", "NumBodies":25 }, { "SystemName":"Pera", "NumBodies":22 } ], "BaseValue":47743, "Bonus":0, "TotalEarnings":47743},
            [SellExplorationDataEventSummary("HR 1597", {"HR 1597 & Co"}, {"EDA Kunti League"}, 47743)]
        ),
        (
            StarSystem("HR 1597", 1000, ("EDA Kunti League", "HR 1597 & Co")),
            Station("Elsa Prospect", 1000, "EDA Kunti League"),
            {"timestamp":"2020-05-15T13:13:38Z", "event":"MultiSellExplorationData", "Discovered":[ { "SystemName":"Shui Wei Sector PO-Q b5-1", "NumBodies":25 }, { "SystemName":"Pera", "NumBodies":22 } ], "BaseValue":47743, "Bonus":0, "TotalEarnings":47743},
            [SellExplorationDataEventSummary("HR 1597", {"EDA Kunti League"}, {"HR 1597 & Co"}, 47743)]
        )
    ])
def test_sell_exploration_data_single(star_system: StarSystem, last_docked_station: Station, sell_exploration_data_event: Dict[str, Any], expected_results: List):
    pilot_state = PilotState()
    pilot_state.system_address = star_system.address
    pilot_state.last_docked_station = last_docked_station
    galaxy_state = GalaxyState()
    galaxy_state.systems[star_system.address] = star_system
    expected_pilot_state = copy.deepcopy(pilot_state)
    expected_galaxy_state = copy.deepcopy(galaxy_state)

    sell_exploration_data_event_processor = SellExplorationDataEventProcessor()
    result = sell_exploration_data_event_processor.process(sell_exploration_data_event, pilot_state, galaxy_state)
    assert result == expected_results
    assert pilot_state == expected_pilot_state
    assert galaxy_state == expected_galaxy_state


@pytest.mark.parametrize(
   "star_system, last_docked_station, market_sell_event, expected_results",
    (
        (
            StarSystem("Afli", 1000, ("Soverign Justice League", "Afli Blue Society")),
            Station("Pu City", 1000, "Soverign Justice League"),
            {"timestamp":"2020-12-26T14:44:02Z", "event":"MarketSell", "MarketID":3510023936, "Type":"gold", "Count":756, "SellPrice":59759, "TotalSale":45177804, "AvgPricePaid":4568},
            [MarketSellEventSummary("Afli", {"Soverign Justice League"}, {"Afli Blue Society"}, 756, 59759, 4568)]
        ),
        (
            StarSystem("Afli", 1000, ("Soverign Justice League", "Afli Blue Society")),
            Station("Pu City", 1000, "Afli Blue Society"),
            {"timestamp":"2020-12-26T14:44:02Z", "event":"MarketSell", "MarketID":3510023936, "Type":"gold", "Count":756, "SellPrice":59759, "TotalSale":45177804, "AvgPricePaid":4568},
            [MarketSellEventSummary("Afli", {"Afli Blue Society"}, {"Soverign Justice League"}, 756, 59759, 4568)]
        ),
        (
            StarSystem("Afli", 1000, ("Soverign Justice League", "Afli Blue Society")),
            Station("Pu City", 1000, "Soverign Justice League"),
            {"timestamp":"2020-10-25T13:00:41Z", "event":"MarketSell", "MarketID":3228014336, "Type":"battleweapons", "Type_Localised":"Battle Weapons", "Count":1, "SellPrice":7111, "TotalSale":7111, "AvgPricePaid":0, "IllegalGoods":True, "BlackMarket":True},
            [MarketSellEventSummary("Afli", {"Afli Blue Society"}, {"Soverign Justice League"}, 1, 7111, 0)]
        ),
        (
            StarSystem("Afli", 1000, ("Soverign Justice League", "Afli Blue Society")),
            Station("Pu City", 1000, "Afli Blue Society"),
            {"timestamp":"2020-10-25T13:00:41Z", "event":"MarketSell", "MarketID":3228014336, "Type":"battleweapons", "Type_Localised":"Battle Weapons", "Count":1, "SellPrice":7111, "TotalSale":7111, "AvgPricePaid":0, "IllegalGoods":True, "BlackMarket":True},
            [MarketSellEventSummary("Afli", {"Soverign Justice League"}, {"Afli Blue Society"}, 1, 7111, 0)]
        ),
        (
            StarSystem("Afli", 1000, ("Soverign Justice League", "Afli Blue Society")),
            Station("Pu City", 1000, "Soverign Justice League"),
            {"timestamp":"2020-10-01T13:31:38Z", "event":"MarketSell", "MarketID":3223702528, "Type":"hydrogenfuel", "Type_Localised":"Hydrogen Fuel", "Count":64, "SellPrice":80, "TotalSale":5120, "AvgPricePaid":1080},
            [MarketSellEventSummary("Afli", {"Afli Blue Society"}, {"Soverign Justice League"}, 64, 80, 1080)]
        ),
        (
            StarSystem("Afli", 1000, ("Soverign Justice League", "Afli Blue Society")),
            Station("Pu City", 1000, "Soverign Justice League"),
            {"timestamp":"2020-10-01T13:31:38Z", "event":"MarketSell", "MarketID":3223702528, "Type":"hydrogenfuel", "Type_Localised":"Hydrogen Fuel", "Count":1, "SellPrice":80, "TotalSale":80, "AvgPricePaid":80},
            []
        ),
        (
            StarSystem("Afli", 1000, ("Soverign Justice League", "Afli Blue Society")),
            Station("Pu City", 1000, "Afli Blue Society"),
            {"timestamp":"2020-10-25T13:00:41Z", "event":"MarketSell", "MarketID":3228014336, "Type":"battleweapons", "Type_Localised":"Battle Weapons", "Count":1, "SellPrice":7111, "TotalSale":7111, "AvgPricePaid":10000, "IllegalGoods":True, "BlackMarket":True},
            [MarketSellEventSummary("Afli", {"Afli Blue Society"}, {"Soverign Justice League"}, 1, 7111, 10000)]
        )
    )
)
def test_market_sell_single(star_system: StarSystem, last_docked_station: Station, market_sell_event: Dict[str, Any], expected_results: List):
    pilot_state = PilotState()
    pilot_state.system_address = star_system.address
    pilot_state.last_docked_station = last_docked_station
    galaxy_state = GalaxyState()
    galaxy_state.systems[star_system.address] = star_system
    expected_pilot_state = copy.deepcopy(pilot_state)
    expected_galaxy_state = copy.deepcopy(galaxy_state)

    market_sell_event_processor = MarketSellEventProcessor()
    result = market_sell_event_processor.process(market_sell_event, pilot_state, galaxy_state)
    assert result == expected_results
    assert pilot_state == expected_pilot_state
    assert galaxy_state == expected_galaxy_state


@pytest.mark.parametrize(
   "star_system, station, mission, mission_accepted_event",
    (
        (
            StarSystem("Luchu", 86306249, ["Luchu Purple Hand Gang", "LHS 1832 Labour", "Noblemen of Luchu", "Movement for Luchu for Equality"]),
            Station("Neumann Enterprise", 86306249, "Luchu Purple Hand Gang"),
            Mission(685926938, "Luchu Purple Hand Gang", "++", 86306249),
            { "timestamp":"2020-12-31T13:47:32Z", "event":"MissionAccepted", "Faction":"Luchu Purple Hand Gang", "Name":"Mission_Courier", "LocalisedName":"Courier Job Available", "TargetFaction":"LTT 2337 Empire Party", "DestinationSystem":"LTT 2337", "DestinationStation":"Bowen Terminal", "Expiry":"2021-01-01T13:46:03Z", "Wing":False, "Influence":"++", "Reputation":"+", "Reward":51607, "MissionID":685926938 }
        ),
        (
            StarSystem("Luchu", 86306249, ["Luchu Purple Hand Gang", "LHS 1832 Labour", "Noblemen of Luchu", "Movement for Luchu for Equality"]),
            Station("Neumann Enterprise", 86306249, "Luchu Purple Hand Gang"),
            Mission(685926779, "LHS 1832 Labour", "++", 86306249),
            { "timestamp":"2020-12-31T13:47:10Z", "event":"MissionAccepted", "Faction":"LHS 1832 Labour", "Name":"Chain_HelpFinishTheOrder", "LocalisedName":"Deliver 2 Units of Polymers", "Commodity":"$Polymers_Name;", "Commodity_Localised":"Polymers", "Count":2, "TargetFaction":"Verner Imperial Society", "DestinationSystem":"Beatis", "DestinationStation":"Vlamingh Hub", "Expiry":"2021-01-01T13:46:03Z", "Wing":False, "Influence":"++", "Reputation":"++", "Reward":10045, "MissionID":685926779 }
        )
    )
)
def test_mission_accepted_single(star_system: StarSystem, station: Station, mission: Mission, mission_accepted_event: Dict[str, Any]):
    pilot_state = PilotState()
    pilot_state.system_address = star_system.address
    pilot_state.last_docked_station = station
    galaxy_state = GalaxyState()
    galaxy_state.systems[star_system.address] = star_system
    expected_pilot_state = copy.deepcopy(pilot_state)
    expected_pilot_state.missions[mission.id] = mission
    expected_galaxy_state = copy.deepcopy(galaxy_state)

    mission_accepted_event_processor = MissionAcceptedEventProcessor()
    result = mission_accepted_event_processor.process(mission_accepted_event, pilot_state, galaxy_state)
    assert result == []
    assert pilot_state == expected_pilot_state
    assert galaxy_state == expected_galaxy_state


@pytest.mark.parametrize(
   "star_systems, station, mission, mission_completed_event, expected_results",
    (
        (
            [
                StarSystem("Luchu", 2871051298217, ["Luchu Purple Hand Gang", "LHS 1832 Labour", "Noblemen of Luchu", "Movement for Luchu for Equality", "Luchu Major Industries", "Herci Bridge Limited", "EDA Kunti League"]),
                StarSystem("LTT 2337", 908620436178, ["LTT 2337 United Holdings", "LTT 2337 Empire Party", "Independent LTT 2337 Values Party", "LTT 2337 Flag", "LTT 2337 Jet Brothers", "The Nova Alliance", "EDA Kunti League"])
            ],
            Station("Bowen Terminal", 908620436178, "EDA Kunti League"),
            Mission(685926938, "Luchu Purple Hand Gang", "++", 2871051298217),
            {"timestamp":"2020-12-31T14:11:07Z", "event":"MissionCompleted", "Faction":"Luchu Purple Hand Gang", "Name":"Mission_Courier_name", "MissionID":685926938, "TargetFaction":"LTT 2337 Empire Party", "DestinationSystem":"LTT 2337", "DestinationStation":"Bowen Terminal", "Reward":11763, "FactionEffects":[ { "Faction":"Luchu Purple Hand Gang", "Effects":[ { "Effect":"$MISSIONUTIL_Interaction_Summary_EP_up;", "Effect_Localised":"The economic status of $#MinorFaction; has improved in the $#System; system.", "Trend":"UpGood" } ], "Influence":[ { "SystemAddress":2871051298217, "Trend":"UpGood", "Influence":"++" } ], "ReputationTrend":"UpGood", "Reputation":"+" }, { "Faction":"LTT 2337 Empire Party", "Effects":[  ], "Influence":[  ], "ReputationTrend":"UpGood", "Reputation":"+" } ] },
            [
                MissionCompletedEventSummary("Luchu", {"Luchu Purple Hand Gang"}, {"LHS 1832 Labour", "Noblemen of Luchu", "Movement for Luchu for Equality", "Luchu Major Industries", "Herci Bridge Limited", "EDA Kunti League"}, "++"),
                MissionCompletedEventSummary("LTT 2337", {"LTT 2337 Empire Party"}, {"LTT 2337 United Holdings", "Independent LTT 2337 Values Party", "LTT 2337 Flag", "LTT 2337 Jet Brothers", "The Nova Alliance", "EDA Kunti League"}, "++")
            ]
        ),
        (
            [
                StarSystem("Luchu", 2871051298217, ["Luchu Purple Hand Gang", "LHS 1832 Labour", "Noblemen of Luchu", "Movement for Luchu for Equality", "Luchu Major Industries", "Herci Bridge Limited", "EDA Kunti League"]),
                StarSystem("Trumuye", 11667412755873, ["Antai Energy Group", "Trumuye Emperor's Grace", "Trumuye Incorporated", "League of Trumuye League", "United Trumuye Progressive Party", "EDA Kunti League"])
            ],
            Station("Yakovlev Port", 11667412755873, "EDA Kunti League"),
            Mission(685926706, "LHS 1832 Labour", "+++", 2871051298217),
            # { "timestamp":"2020-12-31T13:46:59Z", "event":"MissionAccepted", "Faction":"LHS 1832 Labour", "Name":"Mission_Delivery_Democracy", "LocalisedName":"Deliver 18 units of Copper in the name of democracy", "Commodity":"$Copper_Name;", "Commodity_Localised":"Copper", "Count":18, "TargetFaction":"Trumuye Incorporated", "DestinationSystem":"Trumuye", "DestinationStation":"Yakovlev Port", "Expiry":"2021-01-01T13:46:03Z", "Wing":false, "Influence":"++", "Reputation":"++", "Reward":50745, "MissionID":685926706 }
            { "timestamp":"2020-12-31T13:52:56Z", "event":"MissionCompleted", "Faction":"LHS 1832 Labour", "Name":"Mission_Delivery_Democracy_name", "MissionID":685926706, "Commodity":"$Copper_Name;", "Commodity_Localised":"Copper", "Count":18, "TargetFaction":"Trumuye Incorporated", "DestinationSystem":"Trumuye", "DestinationStation":"Yakovlev Port", "Reward":1000, "FactionEffects":[ { "Faction":"Trumuye Incorporated", "Effects":[ { "Effect":"$MISSIONUTIL_Interaction_Summary_EP_up;", "Effect_Localised":"The economic status of $#MinorFaction; has improved in the $#System; system.", "Trend":"UpGood" } ], "Influence":[ { "SystemAddress":11667412755873, "Trend":"UpGood", "Influence":"+++++" } ], "ReputationTrend":"UpGood", "Reputation":"++" }, { "Faction":"LHS 1832 Labour", "Effects":[ { "Effect":"$MISSIONUTIL_Interaction_Summary_EP_up;", "Effect_Localised":"The economic status of $#MinorFaction; has improved in the $#System; system.", "Trend":"UpGood" } ], "Influence":[ { "SystemAddress":2871051298217, "Trend":"UpGood", "Influence":"+++" } ], "ReputationTrend":"UpGood", "Reputation":"++" } ] },
            [
                MissionCompletedEventSummary("Trumuye", {"Trumuye Incorporated"}, {"Antai Energy Group", "Trumuye Emperor's Grace", "League of Trumuye League", "United Trumuye Progressive Party", "EDA Kunti League"}, "+++++"),
                MissionCompletedEventSummary("Luchu", {"LHS 1832 Labour"}, {"Luchu Purple Hand Gang", "Noblemen of Luchu", "Movement for Luchu for Equality", "Luchu Major Industries", "Herci Bridge Limited", "EDA Kunti League"}, "+++++")
            ]
        ),
        (
            [
                StarSystem("Otegine", 5370319620984, ["Pilots' Federation Administration"]),
                StarSystem("Dromi", 1213084977515, ["Pilots' Federation Administration"])
            ],
            Station("Aldrich Station", 5370319620984, "Pilots' Federation Administration"),
            Mission(570789967, "Pilots' Federation Administration", "None", 5370319620984),
            { "timestamp":"2020-04-25T15:25:27Z", "event":"MissionCompleted", "Faction":"Pilots' Federation Administration", "Name":"Mission_Delivery_name", "MissionID":570789967, "Commodity":"$ConductiveFabrics_Name;", "Commodity_Localised":"Conductive Fabrics", "Count":4, "TargetFaction":"Pilots' Federation Administration", "DestinationSystem":"Dromi", "DestinationStation":"Mawson Dock", "Reward":24310, "FactionEffects":[ { "Faction":"Pilots' Federation Administration", "Effects":[  ], "Influence":[  ], "ReputationTrend":"UpGood", "Reputation":"+" } ] },
            []
        ),
        (
            [
                StarSystem("Gebel", 3107576582874, ["EG Union", "Gebel Silver Advanced Org", "Gebel Empire League", "Gebel Freedom Party", "Gebel Industries" ,"Workers of Gebel Labour", "Pilots' Federation Local Branch"]),
                StarSystem("LHS 3802", 2870245991865, ["LHS 2802 Partnership", "HDS 3215 Defense Party", "LHS 3802 Rats", "LHS 3802 Commodities", "Gebel Empire League", "LHS 3802 Law Party", "LHS 3802 Democrats"])
            ],
            Station("Riess Hub", 3107576582874, "EG Union"),
            Mission(572416943, "EG Union", "++", 3107576582874),
            { "timestamp":"2020-04-29T13:54:30Z", "event":"MissionCompleted", "Faction":"EG Union", "Name":"Mission_Assassinate_name", "MissionID":572416943, "TargetType":"$MissionUtil_FactionTag_PirateLord;", "TargetType_Localised":"Known Pirate", "TargetFaction":"LHS 3802 Rats", "NewDestinationSystem":"Gebel", "DestinationSystem":"LHS 3802", "NewDestinationStation":"Riess Hub", "DestinationStation":"Tokubei Terminal", "Target":"Mauduit", "Reward":10000, "FactionEffects":[ { "Faction":"EG Union", "Effects":[ { "Effect":"$MISSIONUTIL_Interaction_Summary_EP_up;", "Effect_Localised":"The economic status of $#MinorFaction; has improved in the $#System; system.", "Trend":"UpGood" } ], "Influence":[ { "SystemAddress":3107576582874, "Trend":"UpGood", "Influence":"+" } ], "ReputationTrend":"UpGood", "Reputation":"+++" }, { "Faction":"LHS 3802 Rats", "Effects":[ { "Effect":"$MISSIONUTIL_Interaction_Summary_EP_down;", "Effect_Localised":"The economic status of $#MinorFaction; has declined in the $#System; system.", "Trend":"DownBad" } ], "Influence":[ { "SystemAddress":2870245991865, "Trend":"DownBad", "Influence":"+" } ], "ReputationTrend":"DownBad", "Reputation":"+" } ] },
            [
                MissionCompletedEventSummary("Gebel", {"EG Union"}, {"Gebel Silver Advanced Org", "Gebel Empire League", "Gebel Freedom Party", "Gebel Industries" ,"Workers of Gebel Labour", "Pilots' Federation Local Branch"}, "++"),
                MissionCompletedEventSummary("LHS 3802", {"LHS 2802 Partnership", "HDS 3215 Defense Party", "LHS 3802 Commodities", "Gebel Empire League", "LHS 3802 Law Party", "LHS 3802 Democrats", }, {"LHS 3802 Rats"}, "++")
            ]
        ),
        (
            [
                StarSystem("Kunti", 9468121064873, ["EDA Kunti League", "Kunti Central Limited", "LTT 2337 Empire Party", "Workers of Kunti Republic Party", "New Kunti Nationalists", "Kunti Central Limited", "Kunti Dynamic Industry", "Dragons of Kunti"])
            ],
            Station("Syromyatnikov Terminal", 9468121064873, "EDA Kunti League"),
            Mission(716512290, "EDA Kunti League", "++", 9468121064873),
            { "timestamp":"2021-02-21T06:59:50Z", "event":"MissionCompleted", "Faction":"EDA Kunti League", "Name":"Mission_Delivery_Investment_name", "MissionID":716512290, "Commodity":"$FoodCartridges_Name;", "Commodity_Localised":"Food Cartridges", "Count":48, "TargetFaction":"Kunti Dynamic Industry", "DestinationSystem":"Kunti", "DestinationStation":"Syromyatnikov Terminal", "Reward":26204, "FactionEffects":[ { "Faction":"Kunti Dynamic Industry", "Effects":[ { "Effect":"$MISSIONUTIL_Interaction_Summary_EP_up;", "Effect_Localised":"The economic status of $#MinorFaction; has improved in the $#System; system.", "Trend":"UpGood" } ], "Influence":[  ], "ReputationTrend":"UpGood", "Reputation":"++" }, { "Faction":"EDA Kunti League", "Effects":[ { "Effect":"$MISSIONUTIL_Interaction_Summary_EP_up;", "Effect_Localised":"The economic status of $#MinorFaction; has improved in the $#System; system.", "Trend":"UpGood" } ], "Influence":[ { "SystemAddress":9468121064873, "Trend":"UpGood", "Influence":"+++" } ], "ReputationTrend":"UpGood", "Reputation":"++" } ] },
            [
                MissionCompletedEventSummary("Kunti", {"EDA Kunti League"}, {"Kunti Central Limited", "LTT 2337 Empire Party", "Workers of Kunti Republic Party", "New Kunti Nationalists", "Kunti Central Limited", "Kunti Dynamic Industry", "Dragons of Kunti"}, "+++"),
                # MissionCompletedEventSummary("Kunti", {"Kunti Dynamic Industry"}, {"EDA Kunti League", "Kunti Central Limited", "LTT 2337 Empire Party", "Workers of Kunti Republic Party", "New Kunti Nationalists", "Kunti Central Limited", "Dragons of Kunti"}, "+++")
            ]
        ),
        (
            [
                StarSystem("LHS 1832", 672028108201, ["EDA Kunti League", "Federal Defense League"])
            ],
            Station("Coney Gateway", 672028108201, "EDA Kunti League"),
            Mission(718812242, "EDA Kunti League", "++", 672028108201),
            { "timestamp":"2021-02-25T11:49:52Z", "event":"MissionCompleted", "Faction":"Federal Defense League", "Name":"Mission_Massacre_Conflict_CivilWar_name", "MissionID":718812242, "TargetFaction":"EDA Kunti League", "KillCount":81, "DestinationSystem":"LHS 1832", "DestinationStation":"Coney Gateway", "Reward":40320868, "FactionEffects":[ { "Faction":"Federal Defense League", "Effects":[ { "Effect":"$MISSIONUTIL_Interaction_Summary_EP_up;", "Effect_Localised":"The economic status of $#MinorFaction; has improved in the $#System; system.", "Trend":"UpGood" } ], "Influence":[  ], "ReputationTrend":"UpGood", "Reputation":"++" }, { "Faction":"EDA Kunti League", "Effects":[ { "Effect":"$MISSIONUTIL_Interaction_Summary_EP_down;", "Effect_Localised":"The economic status of $#MinorFaction; has declined in the $#System; system.", "Trend":"DownBad" } ], "Influence":[  ], "ReputationTrend":"DownBad", "Reputation":"+" } ] },
            [
                MissionCompletedEventSummary("LHS 1832", {"Federal Defense League"}, {"EDA Kunti League"}, "++"),
            ]
        )

        # Testing TODOS:
        # 1. Mission with no destination system or faction, e.g. donation
    )
)
def test_mission_completed_single(star_systems: List[StarSystem], station: Station, mission: Mission, mission_completed_event: Dict[str, Any], expected_results: List[MissionCompletedEventSummary]):
    pilot_state = PilotState()
    pilot_state.last_docked_station = station
    pilot_state.missions[mission.id] = mission
    galaxy_state = GalaxyState()
    for star_system in star_systems:
        galaxy_state.systems[star_system.address] = star_system
    expected_pilot_state = copy.deepcopy(pilot_state)
    del expected_pilot_state.missions[mission.id]
    expected_galaxy_state = copy.deepcopy(galaxy_state)

    mission_completed_event_processor = MissionCompletedEventProcessor()
    result = mission_completed_event_processor.process(mission_completed_event, pilot_state, galaxy_state)
    assert result == expected_results
    assert pilot_state == expected_pilot_state
    assert galaxy_state == expected_galaxy_state


@pytest.mark.parametrize(
   "missions, mission_abandoned_event, expected_missions",
    (
        (
            [
            ],
            {"timestamp":"2020-05-17T04:08:53Z", "event":"MissionAbandoned", "Name":"MISSION_Scan_name", "MissionID":579156136 },
            [
            ]
        ),
        (
            [
                Mission(579156136, "Pilots' Federation Administration", "None", 5370319620984)
            ],
            {"timestamp":"2020-05-17T04:08:53Z", "event":"MissionAbandoned", "Name":"MISSION_Scan_name", "MissionID":579156136 },
            [
            ]
        ),
        (
            [
                Mission(579156136, "Pilots' Federation Administration", "None", 5370319620984),
                Mission(685926706, "LHS 1832 Labour", "+++", 2871051298217),
            ],
            {"timestamp":"2020-05-17T04:08:53Z", "event":"MissionAbandoned", "Name":"MISSION_Scan_name", "MissionID":579156136 },
            [
                Mission(685926706, "LHS 1832 Labour", "+++", 2871051298217)
            ]
        ),
        (
            [
                Mission(685926706, "LHS 1832 Labour", "+++", 2871051298217),
            ],
            {"timestamp":"2020-05-17T04:08:53Z", "event":"MissionAbandoned", "Name":"MISSION_Scan_name", "MissionID":579156136 },
            [
                Mission(685926706, "LHS 1832 Labour", "+++", 2871051298217)
            ]
        )
    )
)
def test_mission_abandoned(missions: Iterable[Mission], mission_abandoned_event:str, expected_missions:Iterable[Mission]):
    pilot_state = PilotState()
    pilot_state.missions.update((mission.id, mission) for mission in missions)
    galaxy_state = GalaxyState()
    expected_pilot_state = copy.deepcopy(pilot_state)
    expected_pilot_state.missions.clear()
    expected_pilot_state.missions.update((mission.id, mission) for mission in expected_missions)
    expected_galaxy_state = copy.deepcopy(galaxy_state)
    result = MissionAbandonedEventProcessor().process(mission_abandoned_event, pilot_state, galaxy_state)
    assert result == []
    assert pilot_state == expected_pilot_state
    assert galaxy_state == expected_galaxy_state


@pytest.mark.parametrize(
   "missions, star_systems, mission_abandoned_event, expected_results, expected_missions",
    (
        (
            [],
            [],
            {"timestamp":"2020-05-17T04:08:53Z", "event":"MissionFailed", "Name":"MISSION_Scan_name", "MissionID":579156136 },
            [],
            []
        ),
        (
            [
                Mission(579156136, "Pilots' Federation Administration", "None", 5791537031962098456136)
            ],
            [
                StarSystem("Gebel", 5791537031962098456136, ["EG Union", "Gebel Silver Advanced Org", "Gebel Empire League", "Gebel Freedom Party", "Gebel Industries" ,"Workers of Gebel Labour", "Pilots' Federation Local Branch"]),
            ],
            {"timestamp":"2020-05-17T04:08:53Z", "event":"MissionFailed", "Name":"MISSION_Scan_name", "MissionID":579156136 },
            [
                MissionFailedEventSummary("Gebel", "Pilots' Federation Local Branch", ["EG Union", "Gebel Silver Advanced Org", "Gebel Empire League", "Gebel Freedom Party", "Gebel Industries" ,"Workers of Gebel Labour"])
            ],
            [
            ]
        ),
        (
            [
                Mission(579156136, "Pilots' Federation Administration", "None", 5791537031962098456136),
                Mission(685926706, "LHS 1832 Labour", "+++", 2871051298217),
            ],
            [
                StarSystem("Gebel", 5791537031962098456136, ["EG Union", "Gebel Silver Advanced Org", "Gebel Empire League", "Gebel Freedom Party", "Gebel Industries" ,"Workers of Gebel Labour", "Pilots' Federation Local Branch"]),
            ],
            {"timestamp":"2020-05-17T04:08:53Z", "event":"MissionFailed", "Name":"MISSION_Scan_name", "MissionID":579156136 },
            [
                MissionFailedEventSummary("Gebel", "Pilots' Federation Local Branch", ["EG Union", "Gebel Silver Advanced Org", "Gebel Empire League", "Gebel Freedom Party", "Gebel Industries" ,"Workers of Gebel Labour"])
            ],
            [
                Mission(685926706, "LHS 1832 Labour", "+++", 2871051298217)
            ]
        ),
        (
            [
                Mission(685926706, "LHS 1832 Labour", "+++", 2871051298217),
            ],
            [],
            {"timestamp":"2020-05-17T04:08:53Z", "event":"MissionFailed", "Name":"MISSION_Scan_name", "MissionID":579156136 },
            [],
            [
                Mission(685926706, "LHS 1832 Labour", "+++", 2871051298217)
            ]
        )
    )
)
def test_mission_failed(missions: Iterable[Mission], star_systems: Iterable[StarSystem], mission_abandoned_event: str, expected_results: Iterable[EventSummary],  expected_missions: Iterable[Mission]):
    pilot_state = PilotState()
    pilot_state.missions.update((mission.id, mission) for mission in missions)
    galaxy_state = GalaxyState()
    galaxy_state.systems.update((star_system.address, star_system) for star_system in star_systems)
    expected_pilot_state = copy.deepcopy(pilot_state)
    expected_pilot_state.missions.clear()
    expected_pilot_state.missions.update((mission.id, mission) for mission in expected_missions)
    expected_galaxy_state = copy.deepcopy(galaxy_state)
    result = MissionFailedEventProcessor().process(mission_abandoned_event, pilot_state, galaxy_state)
    assert result == expected_results
    assert pilot_state == expected_pilot_state
    assert galaxy_state == expected_galaxy_state


@pytest.mark.parametrize(
    "star_system, murder_event, expected_results",
    (
        (
            StarSystem("Gebel", 5791537031962098456136, ["EG Union", "Gebel Silver Advanced Org", "Gebel Empire League", "Gebel Freedom Party", "Gebel Industries" ,"Workers of Gebel Labour", "Pilots' Federation Local Branch"]),
            { "timestamp":"2020-09-28T15:35:22Z", "event":"CommitCrime", "CrimeType":"murder", "Faction":"Pilots' Federation Local Branch", "Victim":"Nick Coates", "Bounty":5000 },
            [
                MurderEventSummary("Gebel", "Pilots' Federation Local Branch", ["EG Union", "Gebel Silver Advanced Org", "Gebel Empire League", "Gebel Freedom Party", "Gebel Industries" ,"Workers of Gebel Labour"])
            ]
        ),
    )
)
def test_murder(star_system: StarSystem, murder_event: str, expected_results: Iterable[MurderEventSummary]):
    pilot_state = PilotState()
    pilot_state.system_address = star_system.address
    galaxy_state = GalaxyState()
    galaxy_state.systems[star_system.address] = star_system
    expected_pilot_state = copy.deepcopy(pilot_state)
    expected_galaxy_state = copy.deepcopy(galaxy_state)
    result = CommitCrimeEventProcessor().process(murder_event, pilot_state, galaxy_state)
    assert result == expected_results
    assert pilot_state == expected_pilot_state
    assert galaxy_state == expected_galaxy_state
