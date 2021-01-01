import copy
from typing import Dict, Any
import pytest

from edmfs.event_processors import LocationEventProcessor, RedeemVoucherEventProcessor
from edmfs.state import PilotState, GalaxyState, Station, StarSystem
from edmfs.event_summaries import RedeemVoucherEventSummary

def test_location_event_processor_init():
    location_event_procesor:LocationEventProcessor = LocationEventProcessor()
    assert(location_event_procesor.eventName == "Location")

@pytest.mark.parametrize(
    "location_event, expected_station",
    [
        ({ "timestamp":"2020-12-30T01:04:56Z", "event":"Location", "Docked":True, "StationName":"Q3H-7HT", "StationType":"FleetCarrier", "MarketID":3703794688, "StationFaction":{ "Name":"FleetCarrier" }, "StationGovernment":"$government_Carrier;", "StationGovernment_Localised":"Private Ownership ", "StationServices":[ "dock", "autodock", "commodities", "contacts", "outfitting", "crewlounge", "rearm", "refuel", "repair", "shipyard", "engineer", "flightcontroller", "stationoperations", "stationMenu", "carriermanagement", "carrierfuel", "voucherredemption" ], "StationEconomy":"$economy_Carrier;", "StationEconomy_Localised":"Private Enterprise", "StationEconomies":[ { "Name":"$economy_Carrier;", "Name_Localised":"Private Enterprise", "Proportion":1.000000 } ], "StarSystem":"HR 1597", "SystemAddress":869487593835, "StarPos":[78.18750,-60.87500,-3.43750], "SystemAllegiance":"Independent", "SystemEconomy":"$economy_Military;", "SystemEconomy_Localised":"Military", "SystemSecondEconomy":"$economy_Refinery;", "SystemSecondEconomy_Localised":"Refinery", "SystemGovernment":"$government_PrisonColony;", "SystemGovernment_Localised":"Prison colony", "SystemSecurity":"$SYSTEM_SECURITY_medium;", "SystemSecurity_Localised":"Medium Security", "Population":446938, "Body":"HR 1597 A 1", "BodyID":3, "BodyType":"Planet", "Powers":[ "A. Lavigny-Duval" ], "PowerplayState":"Exploited", "Factions":[ { "Name":"HR 1597 Empire Party", "FactionState":"None", "Government":"Patronage", "Influence":0.010142, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"Co-operative of Shambogi", "FactionState":"None", "Government":"Cooperative", "Influence":0.041582, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"HR 1597 Crimson Comms Network", "FactionState":"None", "Government":"Corporate", "Influence":0.064909, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":23.330000 }, { "Name":"Social HR 1597 Values Party", "FactionState":"None", "Government":"Democracy", "Influence":0.063895, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":20.280001 }, { "Name":"HR 1597 Crimson Brotherhood", "FactionState":"None", "Government":"Anarchy", "Influence":0.010142, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":67.239998 }, { "Name":"HR 1597 & Co", "FactionState":"War", "Government":"Corporate", "Influence":0.404665, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000, "ActiveStates":[ { "State":"War" } ] }, { "Name":"EDA Kunti League", "FactionState":"War", "Government":"PrisonColony", "Influence":0.404665, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "SquadronFaction":True, "MyReputation":100.000000, "ActiveStates":[ { "State":"Boom" }, { "State":"War" } ] } ], "SystemFaction":{ "Name":"EDA Kunti League", "FactionState":"War" }, "Conflicts":[ { "WarType":"war", "Status":"active", "Faction1":{ "Name":"HR 1597 & Co", "Stake":"Elst Prospect", "WonDays":0 }, "Faction2":{ "Name":"EDA Kunti League", "Stake":"Jean City", "WonDays":1 } } ] }, Station("Q3H-7HT", 869487593835, "FleetCarrier")),
        ({ "timestamp":"2020-12-30T02:28:17Z", "event":"Location", "Docked":False, "StarSystem":"HIP 58121", "SystemAddress":285388835187, "StarPos":[118.18750,-10.21875,61.90625], "SystemAllegiance":"", "SystemEconomy":"$economy_None;", "SystemEconomy_Localised":"None", "SystemSecondEconomy":"$economy_None;", "SystemSecondEconomy_Localised":"None", "SystemGovernment":"$government_None;", "SystemGovernment_Localised":"None", "SystemSecurity":"$GAlAXY_MAP_INFO_state_anarchy;", "SystemSecurity_Localised":"Anarchy", "Population":0, "Body":"HIP 58121 A 4", "BodyID":16, "BodyType":"Planet" }, None),
        ({ "timestamp":"2020-12-07T10:05:58Z", "event":"Location", "Docked":True, "StationName":"Sabine Installation", "StationType":"CraterOutpost", "MarketID":3516792064, "StationFaction":{ "Name":"CD-51 2650 Guardians", "FactionState":"Drought" }, "StationGovernment":"$government_Patronage;", "StationGovernment_Localised":"Patronage", "StationAllegiance":"Empire", "StationServices":[ "dock", "autodock", "commodities", "contacts", "exploration", "missions", "outfitting", "crewlounge", "rearm", "refuel", "repair", "tuning", "engineer", "missionsgenerated", "facilitator", "flightcontroller", "stationoperations", "powerplay", "searchrescue", "stationMenu", "shop" ], "StationEconomy":"$economy_Colony;", "StationEconomy_Localised":"Colony", "StationEconomies":[ { "Name":"$economy_Colony;", "Name_Localised":"Colony", "Proportion":1.000000 } ], "StarSystem":"Arun", "SystemAddress":4482100335314, "StarPos":[105.25000,-46.62500,-10.40625], "SystemAllegiance":"Independent", "SystemEconomy":"$economy_Colony;", "SystemEconomy_Localised":"Colony", "SystemSecondEconomy":"$economy_Extraction;", "SystemSecondEconomy_Localised":"Extraction", "SystemGovernment":"$government_PrisonColony;", "SystemGovernment_Localised":"Prison colony", "SystemSecurity":"$SYSTEM_SECURITY_low;", "SystemSecurity_Localised":"Low Security", "Population":2542, "Body":"Arun B 4 a", "BodyID":43, "BodyType":"Planet", "Factions":[ { "Name":"Progressive Party of LTT 2684", "FactionState":"None", "Government":"Democracy", "Influence":0.044599, "Allegiance":"Federation", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":6.600000, "RecoveringStates":[ { "State":"PirateAttack", "Trend":0 } ] }, { "Name":"Arun Organisation", "FactionState":"None", "Government":"Corporate", "Influence":0.042616, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":0.000000 }, { "Name":"Antai Energy Group", "FactionState":"Retreat", "Government":"Corporate", "Influence":0.154609, "Allegiance":"Federation", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":45.869999, "ActiveStates":[ { "State":"Retreat" } ] }, { "Name":"Arun Gold Partnership", "FactionState":"Lockdown", "Government":"Anarchy", "Influence":0.009911, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand3;", "Happiness_Localised":"Discontented", "MyReputation":0.000000, "ActiveStates":[ { "State":"Lockdown" }, { "State":"Bust" }, { "State":"Drought" } ] }, { "Name":"CD-51 2650 Guardians", "FactionState":"Drought", "Government":"Patronage", "Influence":0.188305, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":15.000000, "ActiveStates":[ { "State":"Drought" } ] }, { "Name":"Friends of Arun", "FactionState":"None", "Government":"Cooperative", "Influence":0.038652, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":0.000000 }, { "Name":"EDA Kunti League", "FactionState":"Boom", "Government":"PrisonColony", "Influence":0.521308, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "SquadronFaction":True, "MyReputation":100.000000, "ActiveStates":[ { "State":"Boom" }, { "State":"CivilLiberty" }, { "State":"PublicHoliday" } ] } ], "SystemFaction":{ "Name":"EDA Kunti League", "FactionState":"Boom" } }, Station("Sabine Installation", 4482100335314, "CD-51 2650 Guardians"))
    ])
def test_location_single(location_event:Dict[str, Any], expected_station:Station):
    #TODO: Generalise beyond a station to PilotState and GalaxyState
    MINOR_FACTION:str = "EDA Kunti League"
    location_event_processor:LocationEventProcessor = LocationEventProcessor()
    pilot_state:PilotState = PilotState()
    galaxy_state:GalaxyState = GalaxyState()
    assert(not location_event_processor.process(location_event, MINOR_FACTION, pilot_state, galaxy_state))
    assert(pilot_state.last_docked_station == expected_station)

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

def test_redeem_voucher_event_processor_init():
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
            [RedeemVoucherEventSummary("", True, "bounty", 1622105)]
        ),
        (
            "EDA Kunti League", 
            StarSystem("", 1000, ("The Fuel Rats Mischief", "CPD-59 314 Imperial Society")), 
            Station("", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-10-31T14:56:09Z", "event":"RedeemVoucher", "Type":"CombatBond", "Amount":1177365, "Faction":"CPD-59 314 Imperial Society" }, 
            [RedeemVoucherEventSummary("", False, "bounty", 1177365)]
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
            [ RedeemVoucherEventSummary("", True, "bounty", 1127126)]
        ),

        # Codex (not relevant for BGS)
        (
            "The Fuel Rats Mischief", 
            StarSystem("", 1000, ("The Fuel Rats Mischief",)), 
            Station("", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-07-05T10:26:31Z", "event":"RedeemVoucher", "Type":"codex", "Amount":5000, "Faction":"" }, 
            []
        ),

        # Scannable (Cartography)
        (
            "The Fuel Rats Mischief", 
            StarSystem("Fuelum", 1000, ("The Fuel Rats Mischief",)), 
            Station("", 1000, "The Fuel Rats Mischief"), 
            { "timestamp":"2020-07-05T15:09:48Z", "event":"RedeemVoucher", "Type":"scannable", "Amount":206078, "Faction":"" }, 
            [RedeemVoucherEventSummary("Fuelum", True, "scannable", 206078)]
        ),
        (
            "The Fuel Rats Mischief", 
            StarSystem("Fuelum", 1000, ("The Fuel Rats Mischief",)), 
            Station("", 1000, "The Dark Wheel"), 
            { "timestamp":"2020-07-05T15:09:48Z", "event":"RedeemVoucher", "Type":"scannable", "Amount":206078, "Faction":"" }, 
            []
        ),
        (
            "The Fuel Rats Mischief", 
            StarSystem("Fuelum", 1000, ("The Fuel Rats Mischief", "The Dark Wheel")), 
            Station("", 1000, "The Dark Wheel"), 
            { "timestamp":"2020-07-05T15:09:48Z", "event":"RedeemVoucher", "Type":"scannable", "Amount":206078, "Faction":"" }, 
            [RedeemVoucherEventSummary("Fuelum", False, "scannable", 206078)]
        )                 
    ])
def test_redeem_voucher_event_processor_single(minor_faction:str, star_system:StarSystem, last_docked_station:Station, redeem_voucher_event:Dict[str, Any], expected_results:list):
    pilot_state = PilotState()
    pilot_state.last_docked_station = last_docked_station
    galaxy_state = GalaxyState()
    galaxy_state.systems[star_system.address] = star_system
    expected_pilot_state = copy.copy(pilot_state)
    expected_galaxy_state = copy.copy(galaxy_state)

    redeem_voucher_event_processor:RedeemVoucherEventProcessor = RedeemVoucherEventProcessor()
    results = redeem_voucher_event_processor.process(redeem_voucher_event, minor_faction, pilot_state, galaxy_state)

    assert(results == expected_results)
    assert(pilot_state == expected_pilot_state)
    assert(galaxy_state == expected_galaxy_state)
