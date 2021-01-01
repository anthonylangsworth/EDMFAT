import pytest
import copy

from edmfs.state import PilotState, GalaxyState, Station
from edmfs.tracker import Tracker
    
def test_tracker_init():
    MINOR_FACTION = "EDA Kunti League"
    tracker:Tracker = Tracker(MINOR_FACTION)
    assert(tracker.minor_faction == MINOR_FACTION)
    assert(tracker.pilot_state == PilotState())
    assert(tracker.galaxy_state == GalaxyState())
    assert(tracker.activity == "")

@pytest.mark.parametrize(
    "minor_faction, events, expected_activity",
    [
        (
            "The Fuel Rats Mischief", 
            (
                
                { "timestamp":"2020-12-30T01:04:56Z", "event":"Location", "Docked":True, "StationName":"Q3H-7HT", "StationType":"FleetCarrier", "MarketID":3703794688, "StationFaction":{ "Name":"FleetCarrier" }, "StationGovernment":"$government_Carrier;", "StationGovernment_Localised":"Private Ownership ", "StationServices":[ "dock", "autodock", "commodities", "contacts", "outfitting", "crewlounge", "rearm", "refuel", "repair", "shipyard", "engineer", "flightcontroller", "stationoperations", "stationMenu", "carriermanagement", "carrierfuel", "voucherredemption" ], "StationEconomy":"$economy_Carrier;", "StationEconomy_Localised":"Private Enterprise", "StationEconomies":[ { "Name":"$economy_Carrier;", "Name_Localised":"Private Enterprise", "Proportion":1.000000 } ], "StarSystem":"HR 1597", "SystemAddress":869487593835, "StarPos":[78.18750,-60.87500,-3.43750], "SystemAllegiance":"Independent", "SystemEconomy":"$economy_Military;", "SystemEconomy_Localised":"Military", "SystemSecondEconomy":"$economy_Refinery;", "SystemSecondEconomy_Localised":"Refinery", "SystemGovernment":"$government_PrisonColony;", "SystemGovernment_Localised":"Prison colony", "SystemSecurity":"$SYSTEM_SECURITY_medium;", "SystemSecurity_Localised":"Medium Security", "Population":446938, "Body":"HR 1597 A 1", "BodyID":3, "BodyType":"Planet", "Powers":[ "A. Lavigny-Duval" ], "PowerplayState":"Exploited", "Factions":[ { "Name":"HR 1597 Empire Party", "FactionState":"None", "Government":"Patronage", "Influence":0.010142, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"Co-operative of Shambogi", "FactionState":"None", "Government":"Cooperative", "Influence":0.041582, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"HR 1597 Crimson Comms Network", "FactionState":"None", "Government":"Corporate", "Influence":0.064909, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":23.330000 }, { "Name":"Social HR 1597 Values Party", "FactionState":"None", "Government":"Democracy", "Influence":0.063895, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":20.280001 }, { "Name":"HR 1597 Crimson Brotherhood", "FactionState":"None", "Government":"Anarchy", "Influence":0.010142, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":67.239998 }, { "Name":"HR 1597 & Co", "FactionState":"War", "Government":"Corporate", "Influence":0.404665, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000, "ActiveStates":[ { "State":"War" } ] }, { "Name":"EDA Kunti League", "FactionState":"War", "Government":"PrisonColony", "Influence":0.404665, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "SquadronFaction":True, "MyReputation":100.000000, "ActiveStates":[ { "State":"Boom" }, { "State":"War" } ] } ], "SystemFaction":{ "Name":"EDA Kunti League", "FactionState":"War" }, "Conflicts":[ { "WarType":"war", "Status":"active", "Faction1":{ "Name":"HR 1597 & Co", "Stake":"Elst Prospect", "WonDays":0 }, "Faction2":{ "Name":"EDA Kunti League", "Stake":"Jean City", "WonDays":1 } } ] },
                { "timestamp":"2020-12-30T02:28:17Z", "event":"Location", "Docked":False, "StarSystem":"HIP 58121", "SystemAddress":285388835187, "StarPos":[118.18750,-10.21875,61.90625], "SystemAllegiance":"", "SystemEconomy":"$economy_None;", "SystemEconomy_Localised":"None", "SystemSecondEconomy":"$economy_None;", "SystemSecondEconomy_Localised":"None", "SystemGovernment":"$government_None;", "SystemGovernment_Localised":"None", "SystemSecurity":"$GAlAXY_MAP_INFO_state_anarchy;", "SystemSecurity_Localised":"Anarchy", "Population":0, "Body":"HIP 58121 A 4", "BodyID":16, "BodyType":"Planet" },
                { "timestamp":"2020-12-31T13:17:13Z", "event":"Commander", "FID":"F5367298", "Name":"Akton" }
            ), 
            ""
        )
    ])
def test_location_sequence(minor_faction:str, events:tuple, expected_activity:str):
    tracker:Tracker = Tracker(minor_faction)
    for event in events:
        tracker.on_event(event)
    assert(tracker.activity == expected_activity)
