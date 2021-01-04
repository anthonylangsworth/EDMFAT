import copy
from typing import Dict, Any
import pytest

from edmfs.event_processors import _supports_minor_faction, _get_location, LocationEventProcessor, RedeemVoucherEventProcessor, DockedEventProcessor, SellExplorationDataEventProcessor, MarketSellEventProcessor, NoLastDockedStationError, UnknownStarSystemError, MissionCompletedEventProcessor
from edmfs.state import PilotState, GalaxyState, Station, Mission, StarSystem
from edmfs.event_summaries import RedeemVoucherEventSummary, SellExplorationDataEventSummary, MarketSellEventSummary, MissionCompletedEventSummary

@pytest.mark.parametrize(
    "event_minor_faction, supported_minor_faction, system_minor_factions, expected_result",
    (
        ("a", "a", "a, b", True),
        ("a", "b", "a, b", False),
        ("c", "b", "a, b", None),

        # Should not happen but included for predictability
        ("a", "a", "", True),
        ("a", "b", "", None),
        ("a", "b", "c, d", None),
        ("a", "a", "c, d", True)
    )
)
def test_supports_minor_faction(event_minor_faction: str, supported_minor_faction:str, system_minor_factions:iter, expected_result):
    assert(_supports_minor_faction(event_minor_faction, supported_minor_faction, system_minor_factions) == expected_result)

@pytest.mark.parametrize(
    "pilot_state, galaxy_state, expected_star_system, expected_station",
    (
        (
            PilotState(Station("Pu City", 98367212, set(["Afli Patron's Principles", "Afli Imperial Society"]))),
            GalaxyState({98367212:StarSystem("Afli", 98367212, [])}),
            StarSystem("Afli", 98367212, []),
            Station("Pu City", 98367212, set(["Afli Patron's Principles", "Afli Imperial Society"]))
        ),
    )
)
def test_get_location(pilot_state: PilotState, galaxy_state: GalaxyState, expected_star_system:StarSystem, expected_station:Station):
    star_system, station = _get_location(pilot_state, galaxy_state)
    assert(star_system == expected_star_system)
    assert(station == expected_station)

def test_get_location_no_system():
    pilot_state = PilotState(Station("Pu City", 654789, set(["Afli Patron's Principles", "Afli Imperial Society"])))
    galaxy_state = GalaxyState({200:StarSystem("Afli", 200, [])})
    try:
        _get_location(pilot_state, galaxy_state)
        assert(False)
    except UnknownStarSystemError:
        pass

def test_get_location_no_station():
    pilot_state = PilotState()
    galaxy_state = GalaxyState({654789:StarSystem("Afli", 654789, [])})
    try:
        _get_location(pilot_state, galaxy_state)
        assert(False)
    except NoLastDockedStationError:
        pass    

def test_location_init():
    location_event_procesor:LocationEventProcessor = LocationEventProcessor()
    assert(location_event_procesor.eventName == "Location")

@pytest.mark.parametrize(
    "location_event, expected_station, expected_system",
    [
        (
            { "timestamp":"2020-12-30T01:04:56Z", "event":"Location", "Docked":True, "StationName":"Q3H-7HT", "StationType":"FleetCarrier", "MarketID":3703794688, "StationFaction":{ "Name":"FleetCarrier" }, "StationGovernment":"$government_Carrier;", "StationGovernment_Localised":"Private Ownership ", "StationServices":[ "dock", "autodock", "commodities", "contacts", "outfitting", "crewlounge", "rearm", "refuel", "repair", "shipyard", "engineer", "flightcontroller", "stationoperations", "stationMenu", "carriermanagement", "carrierfuel", "voucherredemption" ], "StationEconomy":"$economy_Carrier;", "StationEconomy_Localised":"Private Enterprise", "StationEconomies":[ { "Name":"$economy_Carrier;", "Name_Localised":"Private Enterprise", "Proportion":1.000000 } ], "StarSystem":"HR 1597", "SystemAddress":869487593835, "StarPos":[78.18750,-60.87500,-3.43750], "SystemAllegiance":"Independent", "SystemEconomy":"$economy_Military;", "SystemEconomy_Localised":"Military", "SystemSecondEconomy":"$economy_Refinery;", "SystemSecondEconomy_Localised":"Refinery", "SystemGovernment":"$government_PrisonColony;", "SystemGovernment_Localised":"Prison colony", "SystemSecurity":"$SYSTEM_SECURITY_medium;", "SystemSecurity_Localised":"Medium Security", "Population":446938, "Body":"HR 1597 A 1", "BodyID":3, "BodyType":"Planet", "Powers":[ "A. Lavigny-Duval" ], "PowerplayState":"Exploited", "Factions":[ { "Name":"HR 1597 Empire Party", "FactionState":"None", "Government":"Patronage", "Influence":0.010142, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"Co-operative of Shambogi", "FactionState":"None", "Government":"Cooperative", "Influence":0.041582, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"HR 1597 Crimson Comms Network", "FactionState":"None", "Government":"Corporate", "Influence":0.064909, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":23.330000 }, { "Name":"Social HR 1597 Values Party", "FactionState":"None", "Government":"Democracy", "Influence":0.063895, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":20.280001 }, { "Name":"HR 1597 Crimson Brotherhood", "FactionState":"None", "Government":"Anarchy", "Influence":0.010142, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":67.239998 }, { "Name":"HR 1597 & Co", "FactionState":"War", "Government":"Corporate", "Influence":0.404665, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000, "ActiveStates":[ { "State":"War" } ] }, { "Name":"EDA Kunti League", "FactionState":"War", "Government":"PrisonColony", "Influence":0.404665, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "SquadronFaction":True, "MyReputation":100.000000, "ActiveStates":[ { "State":"Boom" }, { "State":"War" } ] } ], "SystemFaction":{ "Name":"EDA Kunti League", "FactionState":"War" }, "Conflicts":[ { "WarType":"war", "Status":"active", "Faction1":{ "Name":"HR 1597 & Co", "Stake":"Elst Prospect", "WonDays":0 }, "Faction2":{ "Name":"EDA Kunti League", "Stake":"Jean City", "WonDays":1 } } ] }, 
            Station("Q3H-7HT", 869487593835, "FleetCarrier"),
            StarSystem("HR 1597", 869487593835, ["HR 1597 Empire Party", "Co-operative of Shambogi", "HR 1597 Crimson Comms Network", "Social HR 1597 Values Party", "HR 1597 Crimson Brotherhood", "HR 1597 & Co", "EDA Kunti League"])
        ),
        (
            { "timestamp":"2020-12-30T02:28:17Z", "event":"Location", "Docked":False, "StarSystem":"HIP 58121", "SystemAddress":285388835187, "StarPos":[118.18750,-10.21875,61.90625], "SystemAllegiance":"", "SystemEconomy":"$economy_None;", "SystemEconomy_Localised":"None", "SystemSecondEconomy":"$economy_None;", "SystemSecondEconomy_Localised":"None", "SystemGovernment":"$government_None;", "SystemGovernment_Localised":"None", "SystemSecurity":"$GAlAXY_MAP_INFO_state_anarchy;", "SystemSecurity_Localised":"Anarchy", "Population":0, "Body":"HIP 58121 A 4", "BodyID":16, "BodyType":"Planet" }, 
            None,
            None # No factions on a fleet carrier
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
def test_location_single(location_event:Dict[str, Any], expected_station:Station, expected_system:StarSystem):
    MINOR_FACTION = "EDA Kunti League"
    location_event_processor = LocationEventProcessor()
    pilot_state = PilotState()
    galaxy_state = GalaxyState()

    assert(not location_event_processor.process(location_event, MINOR_FACTION, pilot_state, galaxy_state))

    expected_pilot_state = PilotState()
    if expected_station:
        expected_pilot_state.last_docked_station = expected_station
    assert(pilot_state == expected_pilot_state)

    expected_galaxy_state = GalaxyState()
    if expected_system:
        expected_galaxy_state.systems[expected_system.address] = expected_system
    assert(galaxy_state == expected_galaxy_state)

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
                { "timestamp":"2020-12-30T01:04:56Z", "event":"Location", "Docked":True, "StationName":"Q3H-7HT", "StationType":"FleetCarrier", "MarketID":3703794688, "StationFaction":{ "Name":"FleetCarrier" }, "StationGovernment":"$government_Carrier;", "StationGovernment_Localised":"Private Ownership ", "StationServices":[ "dock", "autodock", "commodities", "contacts", "outfitting", "crewlounge", "rearm", "refuel", "repair", "shipyard", "engineer", "flightcontroller", "stationoperations", "stationMenu", "carriermanagement", "carrierfuel", "voucherredemption" ], "StationEconomy":"$economy_Carrier;", "StationEconomy_Localised":"Private Enterprise", "StationEconomies":[ { "Name":"$economy_Carrier;", "Name_Localised":"Private Enterprise", "Proportion":1.000000 } ], "StarSystem":"HR 1597", "SystemAddress":869487593835, "StarPos":[78.18750,-60.87500,-3.43750], "SystemAllegiance":"Independent", "SystemEconomy":"$economy_Military;", "SystemEconomy_Localised":"Military", "SystemSecondEconomy":"$economy_Refinery;", "SystemSecondEconomy_Localised":"Refinery", "SystemGovernment":"$government_PrisonColony;", "SystemGovernment_Localised":"Prison colony", "SystemSecurity":"$SYSTEM_SECURITY_medium;", "SystemSecurity_Localised":"Medium Security", "Population":446938, "Body":"HR 1597 A 1", "BodyID":3, "BodyType":"Planet", "Powers":[ "A. Lavigny-Duval" ], "PowerplayState":"Exploited", "Factions":[ { "Name":"HR 1597 Empire Party", "FactionState":"None", "Government":"Patronage", "Influence":0.010142, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"Co-operative of Shambogi", "FactionState":"None", "Government":"Cooperative", "Influence":0.041582, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"HR 1597 Crimson Comms Network", "FactionState":"None", "Government":"Corporate", "Influence":0.064909, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":23.330000 }, { "Name":"Social HR 1597 Values Party", "FactionState":"None", "Government":"Democracy", "Influence":0.063895, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":20.280001 }, { "Name":"HR 1597 Crimson Brotherhood", "FactionState":"None", "Government":"Anarchy", "Influence":0.010142, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":67.239998 }, { "Name":"HR 1597 & Co", "FactionState":"War", "Government":"Corporate", "Influence":0.404665, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000, "ActiveStates":[ { "State":"War" } ] }, { "Name":"EDA Kunti League", "FactionState":"War", "Government":"PrisonColony", "Influence":0.404665, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "SquadronFaction":True, "MyReputation":100.000000, "ActiveStates":[ { "State":"Boom" }, { "State":"War" } ] } ], "SystemFaction":{ "Name":"EDA Kunti League", "FactionState":"War" }, "Conflicts":[ { "WarType":"war", "Status":"active", "Faction1":{ "Name":"HR 1597 & Co", "Stake":"Elst Prospect", "WonDays":0 }, "Faction2":{ "Name":"EDA Kunti League", "Stake":"Jean City", "WonDays":1 } } ] },
                { "timestamp":"2020-12-30T02:28:17Z", "event":"Location", "Docked":False, "StarSystem":"HIP 58121", "SystemAddress":285388835187, "StarPos":[118.18750,-10.21875,61.90625], "SystemAllegiance":"", "SystemEconomy":"$economy_None;", "SystemEconomy_Localised":"None", "SystemSecondEconomy":"$economy_None;", "SystemSecondEconomy_Localised":"None", "SystemGovernment":"$government_None;", "SystemGovernment_Localised":"None", "SystemSecurity":"$GAlAXY_MAP_INFO_state_anarchy;", "SystemSecurity_Localised":"Anarchy", "Population":0, "Body":"HIP 58121 A 4", "BodyID":16, "BodyType":"Planet" },
                { "timestamp":"2020-12-07T10:05:58Z", "event":"Location", "Docked":True, "StationName":"Sabine Installation", "StationType":"CraterOutpost", "MarketID":3516792064, "StationFaction":{ "Name":"CD-51 2650 Guardians", "FactionState":"Drought" }, "StationGovernment":"$government_Patronage;", "StationGovernment_Localised":"Patronage", "StationAllegiance":"Empire", "StationServices":[ "dock", "autodock", "commodities", "contacts", "exploration", "missions", "outfitting", "crewlounge", "rearm", "refuel", "repair", "tuning", "engineer", "missionsgenerated", "facilitator", "flightcontroller", "stationoperations", "powerplay", "searchrescue", "stationMenu", "shop" ], "StationEconomy":"$economy_Colony;", "StationEconomy_Localised":"Colony", "StationEconomies":[ { "Name":"$economy_Colony;", "Name_Localised":"Colony", "Proportion":1.000000 } ], "StarSystem":"Arun", "SystemAddress":4482100335314, "StarPos":[105.25000,-46.62500,-10.40625], "SystemAllegiance":"Independent", "SystemEconomy":"$economy_Colony;", "SystemEconomy_Localised":"Colony", "SystemSecondEconomy":"$economy_Extraction;", "SystemSecondEconomy_Localised":"Extraction", "SystemGovernment":"$government_PrisonColony;", "SystemGovernment_Localised":"Prison colony", "SystemSecurity":"$SYSTEM_SECURITY_low;", "SystemSecurity_Localised":"Low Security", "Population":2542, "Body":"Arun B 4 a", "BodyID":43, "BodyType":"Planet", "Factions":[ { "Name":"Progressive Party of LTT 2684", "FactionState":"None", "Government":"Democracy", "Influence":0.044599, "Allegiance":"Federation", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":6.600000, "RecoveringStates":[ { "State":"PirateAttack", "Trend":0 } ] }, { "Name":"Arun Organisation", "FactionState":"None", "Government":"Corporate", "Influence":0.042616, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":0.000000 }, { "Name":"Antai Energy Group", "FactionState":"Retreat", "Government":"Corporate", "Influence":0.154609, "Allegiance":"Federation", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":45.869999, "ActiveStates":[ { "State":"Retreat" } ] }, { "Name":"Arun Gold Partnership", "FactionState":"Lockdown", "Government":"Anarchy", "Influence":0.009911, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand3;", "Happiness_Localised":"Discontented", "MyReputation":0.000000, "ActiveStates":[ { "State":"Lockdown" }, { "State":"Bust" }, { "State":"Drought" } ] }, { "Name":"CD-51 2650 Guardians", "FactionState":"Drought", "Government":"Patronage", "Influence":0.188305, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":15.000000, "ActiveStates":[ { "State":"Drought" } ] }, { "Name":"Friends of Arun", "FactionState":"None", "Government":"Cooperative", "Influence":0.038652, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":0.000000 }, { "Name":"EDA Kunti League", "FactionState":"Boom", "Government":"PrisonColony", "Influence":0.521308, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "SquadronFaction":True, "MyReputation":100.000000, "ActiveStates":[ { "State":"Boom" }, { "State":"CivilLiberty" }, { "State":"PublicHoliday" } ] } ], "SystemFaction":{ "Name":"EDA Kunti League", "FactionState":"Boom" } }
            ),
            Station("Sabine Installation", 4482100335314, "CD-51 2650 Guardians")
        )
    ])
def test_location_sequence(location_events:tuple, expected_station:Station):
    #TODO: Generalise beyond a station to PilotState and GalaxyState
    MINOR_FACTION:str = "EDA Kunti League"
    location_event_processor:LocationEventProcessor = LocationEventProcessor()
    pilot_state:PilotState = PilotState()
    galaxy_state:GalaxyState = GalaxyState()
    for location_event in location_events:
        assert(not location_event_processor.process(location_event, MINOR_FACTION, pilot_state, galaxy_state))
    assert(pilot_state.last_docked_station == expected_station)    

def test_redeem_voucher_init():
    redeem_voucher_event_procesor:RedeemVoucherEventProcessor = RedeemVoucherEventProcessor()
    assert(redeem_voucher_event_procesor.eventName == "RedeemVoucher")
    
@pytest.mark.parametrize(
    "minor_faction, star_system, last_docked_station, redeem_voucher_event, expected_results",
    [     
        # Bounty 
        (
            "The Fuel Rats Mischief", 
            StarSystem("Fuelum", 1000, ("The Fuel Rats Mischief",)), 
            Station("Station", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-05-09T04:43:16Z", "event":"RedeemVoucher", "Type":"bounty", "Amount":42350, "Factions":[ { "Faction":"The Fuel Rats Mischief", "Amount":42350 } ] }, 
            [ RedeemVoucherEventSummary("Fuelum", True, "bounty", 42350)]
        ),
        (
            "The Fuel Rats Mischief", 
            StarSystem("Fuelum", 1000, ("The Fuel Rats Mischief", "Findja Empire Assembly")), 
            Station("Station", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-05-09T03:42:20Z", "event":"RedeemVoucher", "Type":"bounty", "Amount":25490, "Factions":[ { "Faction":"Findja Empire Assembly", "Amount":25490 } ] }, 
            [RedeemVoucherEventSummary("Fuelum", False, "bounty", 25490)]
        ),
        (
            "The Fuel Rats Mischief", 
            StarSystem("Findja", 1000, ("The Fuel Rats Mischief",)), 
            Station("Station", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-05-09T03:42:31Z", "event":"RedeemVoucher", "Type":"bounty", "Amount":13338, "Factions":[ { "Faction":"", "Amount":13338 } ], "BrokerPercentage":25.000000 }, 
            []
        ),
        (
            "CPD-59 314 Imperial Society", 
            StarSystem("CPD-59 314", 1000, ("The Fuel Rats Mischief", "CPD-59 314 Imperial Society")), 
            Station("Station", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-10-15T14:45:16Z", "event":"RedeemVoucher", "Type":"bounty", "Amount":1779467, "Factions":[ { "Faction":"CPD-59 314 Imperial Society", "Amount":1779467 } ], "BrokerPercentage":25.000000 }, 
            [ RedeemVoucherEventSummary("CPD-59 314", True, "bounty", 1779467)]
        ),
        (
            "The Fuel Rats Mischief", 
            StarSystem("Fuelum", 1000, ("The Fuel Rats Mischief", "Rabh Empire Pact", "Kacomam Empire Group", "Trumuye Emperor's Grace", "EDA Kunti League")), 
            Station("Station", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-12-13T02:02:04Z", "event":"RedeemVoucher", "Type":"bounty", "Amount":5924586, "Factions":[ { "Faction":"Rabh Empire Pact", "Amount":385660 }, { "Faction":"Kacomam Empire Group", "Amount":666873 }, { "Faction":"Trumuye Emperor's Grace", "Amount":545094 }, { "Faction":"EDA Kunti League", "Amount":4326959 } ] }, 
            [
                RedeemVoucherEventSummary("Fuelum", False, "bounty", 385660),
                RedeemVoucherEventSummary("Fuelum", False, "bounty", 666873),
                RedeemVoucherEventSummary("Fuelum", False, "bounty", 545094),    
                RedeemVoucherEventSummary("Fuelum", False, "bounty", 4326959)    
            ]
        ),
        (
            "Rabh Empire Pact", 
            StarSystem("Fuelum", 1000, ("The Fuel Rats Mischief", "Rabh Empire Pact", "Kacomam Empire Group", "Trumuye Emperor's Grace", "EDA Kunti League")), 
            Station("", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-12-13T02:02:04Z", "event":"RedeemVoucher", "Type":"bounty", "Amount":5924586, "Factions":[ { "Faction":"Rabh Empire Pact", "Amount":385660 }, { "Faction":"Kacomam Empire Group", "Amount":666873 }, { "Faction":"Trumuye Emperor's Grace", "Amount":545094 }, { "Faction":"EDA Kunti League", "Amount":4326959 } ] }, 
            [
                RedeemVoucherEventSummary("Fuelum", True, "bounty", 385660),
                RedeemVoucherEventSummary("Fuelum", False, "bounty", 666873),
                RedeemVoucherEventSummary("Fuelum", False, "bounty", 545094),    
                RedeemVoucherEventSummary("Fuelum", False, "bounty", 4326959)    
            ]
        ),

        # Combat Bond
        (
            "EDA Kunti League", 
            StarSystem("", 1000, ("The Fuel Rats Mischief", "EDA Kunti League")), 
            Station("", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-11-27T11:46:17Z", "event":"RedeemVoucher", "Type":"CombatBond", "Amount":1622105, "Faction":"EDA Kunti League" }, 
            [RedeemVoucherEventSummary("", True, "CombatBond", 1622105)]
        ),
        (
            "EDA Kunti League", 
            StarSystem("", 1000, ("The Fuel Rats Mischief", "CPD-59 314 Imperial Society")), 
            Station("", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-10-31T14:56:09Z", "event":"RedeemVoucher", "Type":"CombatBond", "Amount":1177365, "Faction":"CPD-59 314 Imperial Society" }, 
            []
        ),
        (
            "EDA Kunti League", 
            StarSystem("", 1000, ("The Fuel Rats Mischief",)), 
            Station("", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-10-18T11:23:57Z", "event":"RedeemVoucher", "Type":"CombatBond", "Amount":1127126, "Faction":"HR 1597 & Co", "BrokerPercentage":25.000000 }, 
            []
        ),
        (
            "EDA Kunti League", 
            StarSystem("", 1000, ("The Fuel Rats Mischief",)), 
            Station("", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-07-17T15:21:20Z", "event":"RedeemVoucher", "Type":"CombatBond", "Amount":46026, "Faction":"", "BrokerPercentage":25.000000 }, 
            []
        ),
        (
            "HR 1597 & Co", 
            StarSystem("", 1000, ("The Fuel Rats Mischief", "HR 1597 & Co")), 
            Station("", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-10-18T11:23:57Z", "event":"RedeemVoucher", "Type":"CombatBond", "Amount":1127126, "Faction":"HR 1597 & Co", "BrokerPercentage":25.000000 }, 
            [ RedeemVoucherEventSummary("", True, "CombatBond", 1127126)]
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
            "The Fuel Rats Mischief", 
            StarSystem("", 1000, ("The Fuel Rats Mischief",)), 
            Station("", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-07-05T10:26:31Z", "event":"RedeemVoucher", "Type":"codex", "Amount":5000, "Faction":"" }, 
            []
        ),
        (
            "The Fuel Rats Mischief", 
            StarSystem("", 1000, ("The Fuel Rats Mischief",)), 
            Station("", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-12-27T07:48:49Z", "event":"RedeemVoucher", "Type":"settlement", "Amount":4352, "Faction":"" }, 
            []
        ),        
    ])
def test_redeem_voucher_single(minor_faction:str, star_system:StarSystem, last_docked_station:Station, redeem_voucher_event:Dict[str, Any], expected_results:list):
    pilot_state = PilotState()
    pilot_state.last_docked_station = last_docked_station
    galaxy_state = GalaxyState()
    galaxy_state.systems[star_system.address] = star_system
    expected_pilot_state = copy.deepcopy(pilot_state)
    expected_galaxy_state = copy.deepcopy(galaxy_state)

    redeem_voucher_event_processor:RedeemVoucherEventProcessor = RedeemVoucherEventProcessor()
    results = redeem_voucher_event_processor.process(redeem_voucher_event, minor_faction, pilot_state, galaxy_state)

    assert(results == expected_results)
    assert(pilot_state == expected_pilot_state)
    assert(galaxy_state == expected_galaxy_state)

def test_docked_init():
    docked_event_processor = DockedEventProcessor()
    assert(docked_event_processor.eventName == "Docked")

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
def test_docked_single(docked_event:Dict[str, Any], expected_station:Station):
    MINOR_FACTION = "EDA Kunti League"
    docked_event_processor = DockedEventProcessor()
    pilot_state:PilotState = PilotState()
    galaxy_state:GalaxyState = GalaxyState()
    assert(not docked_event_processor.process(docked_event, MINOR_FACTION, pilot_state, galaxy_state))
    assert(pilot_state.last_docked_station == expected_station)

def test_sell_exploration_data_init():
    sell_exploration_event_processor = SellExplorationDataEventProcessor()
    assert(sell_exploration_event_processor.eventName == "SellExplorationData")

@pytest.mark.parametrize(
   "minor_faction, star_system, last_docked_station, sell_exploration_data_event, expected_results",
    [     
        (
            "HR 1597 & Co",
            StarSystem("HR 1597", 1000, ("EDA Kunti League", "HR 1597 & Co")), 
            Station("Elsa Prospect", 1000, "HR 1597 & Co"), 
            { "timestamp":"2020-05-15T13:13:38Z", "event":"MultiSellExplorationData", "Discovered":[ { "SystemName":"Shui Wei Sector PO-Q b5-1", "NumBodies":25 }, { "SystemName":"Pera", "NumBodies":22 } ], "BaseValue":47743, "Bonus":0, "TotalEarnings":47743 },
            [ SellExplorationDataEventSummary("HR 1597", True, 47743)]
        ),
        (
            "HR 1597 & Co",
            StarSystem("HR 1597", 1000, ("EDA Kunti League", "HR 1597 & Co")), 
            Station("Elsa Prospect", 1000, "EDA Kunti League"), 
            { "timestamp":"2020-05-15T13:13:38Z", "event":"MultiSellExplorationData", "Discovered":[ { "SystemName":"Shui Wei Sector PO-Q b5-1", "NumBodies":25 }, { "SystemName":"Pera", "NumBodies":22 } ], "BaseValue":47743, "Bonus":0, "TotalEarnings":47743 },
            [ SellExplorationDataEventSummary("HR 1597", False, 47743)]
        ),
        (
            "The Dark Wheel",
            StarSystem("HR 1597", 1000, ("EDA Kunti League", "HR 1597 & Co")), 
            Station("Elsa Prospect", 1000, "EDA Kunti League"), 
            { "timestamp":"2020-05-15T13:13:38Z", "event":"MultiSellExplorationData", "Discovered":[ { "SystemName":"Shui Wei Sector PO-Q b5-1", "NumBodies":25 }, { "SystemName":"Pera", "NumBodies":22 } ], "BaseValue":47743, "Bonus":0, "TotalEarnings":47743 },
            [ ]
        )
    ])
def test_sell_exploration_data_single(minor_faction:str, star_system:StarSystem, last_docked_station:Station, sell_exploration_data_event:Dict[str, Any], expected_results:list):
    pilot_state = PilotState()
    pilot_state.last_docked_station = last_docked_station
    galaxy_state = GalaxyState()
    galaxy_state.systems[star_system.address] = star_system
    expected_pilot_state = copy.deepcopy(pilot_state)
    expected_galaxy_state = copy.deepcopy(galaxy_state)

    sell_exploration_data_event_processor = SellExplorationDataEventProcessor()
    result = sell_exploration_data_event_processor.process(sell_exploration_data_event, minor_faction, pilot_state, galaxy_state)
    assert(result == expected_results)
    assert(pilot_state == expected_pilot_state)
    assert(galaxy_state == expected_galaxy_state)

def test_market_sell_init():
    market_sell_event_processor = MarketSellEventProcessor()
    assert(market_sell_event_processor.eventName == "MarketSell")

@pytest.mark.parametrize(
   "minor_faction, star_system, last_docked_station, market_sell_event, expected_results",
    (
        (
            "Soverign Justice League",
            StarSystem("Afli", 1000, ("Soverign Justice League", "Afli Blue Society")), 
            Station("Pu City", 1000, "Soverign Justice League"), 
            { "timestamp":"2020-12-26T14:44:02Z", "event":"MarketSell", "MarketID":3510023936, "Type":"gold", "Count":756, "SellPrice":59759, "TotalSale":45177804, "AvgPricePaid":4568 },
            [ MarketSellEventSummary("Afli", True, 756, 59759, 4568)]
        ),
        (
            "Afli Blue Society",
            StarSystem("Afli", 1000, ("Soverign Justice League", "Afli Blue Society")), 
            Station("Pu City", 1000, "Soverign Justice League"), 
            { "timestamp":"2020-12-26T14:44:02Z", "event":"MarketSell", "MarketID":3510023936, "Type":"gold", "Count":756, "SellPrice":59759, "TotalSale":45177804, "AvgPricePaid":4568 },
            [ MarketSellEventSummary("Afli", False, 756, 59759, 4568)]
        ),
        (
            "Soverign Justice League",
            StarSystem("Afli", 1000, ("Soverign Justice League", "Afli Blue Society")), 
            Station("Pu City", 1000, "Soverign Justice League"), 
            { "timestamp":"2020-10-25T13:00:41Z", "event":"MarketSell", "MarketID":3228014336, "Type":"battleweapons", "Type_Localised":"Battle Weapons", "Count":1, "SellPrice":7111, "TotalSale":7111, "AvgPricePaid":0, "IllegalGoods":True, "BlackMarket":True },
            [ MarketSellEventSummary("Afli", False, 1, 7111, 0)]
        ),
        (
            "Afli Blue Society",
            StarSystem("Afli", 1000, ("Soverign Justice League", "Afli Blue Society")), 
            Station("Pu City", 1000, "Soverign Justice League"), 
            { "timestamp":"2020-10-25T13:00:41Z", "event":"MarketSell", "MarketID":3228014336, "Type":"battleweapons", "Type_Localised":"Battle Weapons", "Count":1, "SellPrice":7111, "TotalSale":7111, "AvgPricePaid":0, "IllegalGoods":True, "BlackMarket":True },
            [ MarketSellEventSummary("Afli", True, 1, 7111, 0)]
        ),
        (
            "Soverign Justice League",
            StarSystem("Afli", 1000, ("Soverign Justice League", "Afli Blue Society")), 
            Station("Pu City", 1000, "Soverign Justice League"), 
            { "timestamp":"2020-10-01T13:31:38Z", "event":"MarketSell", "MarketID":3223702528, "Type":"hydrogenfuel", "Type_Localised":"Hydrogen Fuel", "Count":64, "SellPrice":80, "TotalSale":5120, "AvgPricePaid":1080 },
            [ MarketSellEventSummary("Afli", False, 64, 80, 1080)]
        ),
        (
            "Kunti Dragons",
            StarSystem("Afli", 1000, ("Soverign Justice League", "Afli Blue Society")), 
            Station("Pu City", 1000, "Soverign Justice League"), 
            { "timestamp":"2020-12-26T14:44:02Z", "event":"MarketSell", "MarketID":3510023936, "Type":"gold", "Count":756, "SellPrice":59759, "TotalSale":45177804, "AvgPricePaid":4568 },
            [ ]
        )        
    )
)
def test_market_sell_single(minor_faction:str, star_system:StarSystem, last_docked_station:Station, market_sell_event:Dict[str, Any], expected_results:list):
    pilot_state = PilotState()
    pilot_state.last_docked_station = last_docked_station
    galaxy_state = GalaxyState()
    galaxy_state.systems[star_system.address] = star_system
    expected_pilot_state = copy.deepcopy(pilot_state)
    expected_galaxy_state = copy.deepcopy(galaxy_state)

    market_sell_event_processor = MarketSellEventProcessor()
    result = market_sell_event_processor.process(market_sell_event, minor_faction, pilot_state, galaxy_state)
    assert(result == expected_results)
    assert(pilot_state == expected_pilot_state)
    assert(galaxy_state == expected_galaxy_state)

@pytest.mark.parametrize(
   "minor_faction, star_systems, station, mission, mission_completed_event, expected_results",
    (
        (
            "EDA Kunti League",
            [
                StarSystem("Luchu", 2871051298217, ["Luchu Purple Hand Gang", "LHS 1832 Labour", "Noblemen of Luchu", "Movement for Luchu for Equality", "Luchu Major Industries", "Herci Bridge Limited", "EDA Kunti League"]),
                StarSystem("LTT 2337", 908620436178, ["LTT 2337 United Holdings", "LTT 2337 Empire Party", "Independent LTT 2337 Values Party", "LTT 2337 Flag", "LTT 2337 Jet Brothers", "The Nova Alliance", "EDA Kunti League"])
            ],
            Station("Bowen Terminal", 908620436178, "EDA Kunti League"),
            Mission(685926938, "Luchu Purple Hand Gang", "++", 2871051298217, "LTT 2337 Empire Party", "LTT 2337"), 
            { "timestamp":"2020-12-31T14:11:07Z", "event":"MissionCompleted", "Faction":"Luchu Purple Hand Gang", "Name":"Mission_Courier_name", "MissionID":685926938, "TargetFaction":"LTT 2337 Empire Party", "DestinationSystem":"LTT 2337", "DestinationStation":"Bowen Terminal", "Reward":11763, "FactionEffects":[ { "Faction":"Luchu Purple Hand Gang", "Effects":[ { "Effect":"$MISSIONUTIL_Interaction_Summary_EP_up;", "Effect_Localised":"The economic status of $#MinorFaction; has improved in the $#System; system.", "Trend":"UpGood" } ], "Influence":[ { "SystemAddress":2871051298217, "Trend":"UpGood", "Influence":"++" } ], "ReputationTrend":"UpGood", "Reputation":"+" }, { "Faction":"LTT 2337 Empire Party", "Effects":[  ], "Influence":[  ], "ReputationTrend":"UpGood", "Reputation":"+" } ] },
            [
                MissionCompletedEventSummary("Luchu", False, "++")
            ]
        ),
        (
            "EDA Kunti League",
            [
                StarSystem("Luchu", 2871051298217, ["Luchu Purple Hand Gang", "LHS 1832 Labour", "Noblemen of Luchu", "Movement for Luchu for Equality", "Luchu Major Industries", "Herci Bridge Limited", "EDA Kunti League"]),
                StarSystem("Trumuye", 11667412755873, ["Antai Energy Group", "Trumuye Emperor's Grace", "Trumuye Incorporated", "League of Trumuye League", "United Trumuye Progressive Party", "EDA Kunti League"])
            ],
            Station("Yakovlev Port", 11667412755873, "EDA Kunti League"),
            Mission(685926706, "LHS 1832 Labour", "+++", 2871051298217, "Trumuye Incorporated", "Trumuye"),
            # { "timestamp":"2020-12-31T13:46:59Z", "event":"MissionAccepted", "Faction":"LHS 1832 Labour", "Name":"Mission_Delivery_Democracy", "LocalisedName":"Deliver 18 units of Copper in the name of democracy", "Commodity":"$Copper_Name;", "Commodity_Localised":"Copper", "Count":18, "TargetFaction":"Trumuye Incorporated", "DestinationSystem":"Trumuye", "DestinationStation":"Yakovlev Port", "Expiry":"2021-01-01T13:46:03Z", "Wing":false, "Influence":"++", "Reputation":"++", "Reward":50745, "MissionID":685926706 }
            { "timestamp":"2020-12-31T13:52:56Z", "event":"MissionCompleted", "Faction":"LHS 1832 Labour", "Name":"Mission_Delivery_Democracy_name", "MissionID":685926706, "Commodity":"$Copper_Name;", "Commodity_Localised":"Copper", "Count":18, "TargetFaction":"Trumuye Incorporated", "DestinationSystem":"Trumuye", "DestinationStation":"Yakovlev Port", "Reward":1000, "FactionEffects":[ { "Faction":"Trumuye Incorporated", "Effects":[ { "Effect":"$MISSIONUTIL_Interaction_Summary_EP_up;", "Effect_Localised":"The economic status of $#MinorFaction; has improved in the $#System; system.", "Trend":"UpGood" } ], "Influence":[ { "SystemAddress":11667412755873, "Trend":"UpGood", "Influence":"+++++" } ], "ReputationTrend":"UpGood", "Reputation":"++" }, { "Faction":"LHS 1832 Labour", "Effects":[ { "Effect":"$MISSIONUTIL_Interaction_Summary_EP_up;", "Effect_Localised":"The economic status of $#MinorFaction; has improved in the $#System; system.", "Trend":"UpGood" } ], "Influence":[ { "SystemAddress":2871051298217, "Trend":"UpGood", "Influence":"+++" } ], "ReputationTrend":"UpGood", "Reputation":"++" } ] },
            [
                MissionCompletedEventSummary("Trumuye", False, "+++++"),
                MissionCompletedEventSummary("Luchu", False, "+++")
            ]
        )
    )
)
def test_mission_completed_single(minor_faction:str, star_systems:list, station:Station, mission:Mission, mission_completed_event:Dict[str, Any], expected_results:list):
    pilot_state = PilotState()
    pilot_state.last_docked_station = station
    pilot_state.missions[mission.id] = mission
    galaxy_state = GalaxyState()
    for star_system in star_systems:
        galaxy_state.systems[star_system.address] = star_system
    expected_pilot_state = copy.deepcopy(pilot_state)
    expected_galaxy_state = copy.deepcopy(galaxy_state)

    mission_completed_event_processor = MissionCompletedEventProcessor()
    result = mission_completed_event_processor.process(mission_completed_event, minor_faction, pilot_state, galaxy_state)
    assert(result == expected_results)    
    assert(pilot_state == expected_pilot_state)
    assert(galaxy_state == expected_galaxy_state)