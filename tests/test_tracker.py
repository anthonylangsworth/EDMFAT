from edmfs.tracker import Tracker, StarSystemState, PilotState, Station

def test_Tracker_init():
    MINOR_FACTION = "EDA Kunti League"
    tracker:Tracker = Tracker(MINOR_FACTION)
    assert(tracker.minor_faction == MINOR_FACTION)
    assert(tracker.pilot_state != None)
    assert(tracker.pilot_state.last_docked_station == None)

def test_StarSystemState_init():
    SYSTEM_NAME = "Deneb"
    ADDRESS = 89562036
    MINOR_FACTIONS = ("EDA Kunti League", "Kunti Dragons")
    star_system_state:StarSystemState = StarSystemState(SYSTEM_NAME, ADDRESS, MINOR_FACTIONS)
    assert(star_system_state.name == SYSTEM_NAME)
    assert(star_system_state.address == ADDRESS)
    assert(star_system_state.minor_factions == MINOR_FACTIONS)

def test_PilotState_init():
    pilot_state:PilotState = PilotState()
    assert(pilot_state.last_docked_station == None)
    assert(pilot_state.missions == [])

def test_Station_init():
    NAME = "Syromyatnikov Terminal"
    SYSTEM_ADDRESS = 927490167
    CONTROLLING_MINOR_FACTION = "EDA Kunti League"
    station:Station = Station(NAME, SYSTEM_ADDRESS, CONTROLLING_MINOR_FACTION)
    assert(station.name == NAME)
    assert(station.system_address == SYSTEM_ADDRESS)
    assert(station.controlling_minor_faction == CONTROLLING_MINOR_FACTION)

def test_location():
    MINOR_FACTION = "EDA Kunti League"
    tracker:Tracker = Tracker(MINOR_FACTION)
    tracker.on_event({ "timestamp":"2020-12-30T01:04:56Z", "event":"Location", "Docked":True, "StationName":"Q3H-7HT", "StationType":"FleetCarrier", "MarketID":3703794688, "StationFaction":{ "Name":"FleetCarrier" }, "StationGovernment":"$government_Carrier;", "StationGovernment_Localised":"Private Ownership ", "StationServices":[ "dock", "autodock", "commodities", "contacts", "outfitting", "crewlounge", "rearm", "refuel", "repair", "shipyard", "engineer", "flightcontroller", "stationoperations", "stationMenu", "carriermanagement", "carrierfuel", "voucherredemption" ], "StationEconomy":"$economy_Carrier;", "StationEconomy_Localised":"Private Enterprise", "StationEconomies":[ { "Name":"$economy_Carrier;", "Name_Localised":"Private Enterprise", "Proportion":1.000000 } ], "StarSystem":"HR 1597", "SystemAddress":869487593835, "StarPos":[78.18750,-60.87500,-3.43750], "SystemAllegiance":"Independent", "SystemEconomy":"$economy_Military;", "SystemEconomy_Localised":"Military", "SystemSecondEconomy":"$economy_Refinery;", "SystemSecondEconomy_Localised":"Refinery", "SystemGovernment":"$government_PrisonColony;", "SystemGovernment_Localised":"Prison colony", "SystemSecurity":"$SYSTEM_SECURITY_medium;", "SystemSecurity_Localised":"Medium Security", "Population":446938, "Body":"HR 1597 A 1", "BodyID":3, "BodyType":"Planet", "Powers":[ "A. Lavigny-Duval" ], "PowerplayState":"Exploited", "Factions":[ { "Name":"HR 1597 Empire Party", "FactionState":"None", "Government":"Patronage", "Influence":0.010142, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"Co-operative of Shambogi", "FactionState":"None", "Government":"Cooperative", "Influence":0.041582, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000 }, { "Name":"HR 1597 Crimson Comms Network", "FactionState":"None", "Government":"Corporate", "Influence":0.064909, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":23.330000 }, { "Name":"Social HR 1597 Values Party", "FactionState":"None", "Government":"Democracy", "Influence":0.063895, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":20.280001 }, { "Name":"HR 1597 Crimson Brotherhood", "FactionState":"None", "Government":"Anarchy", "Influence":0.010142, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":67.239998 }, { "Name":"HR 1597 & Co", "FactionState":"War", "Government":"Corporate", "Influence":0.404665, "Allegiance":"Empire", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "MyReputation":100.000000, "ActiveStates":[ { "State":"War" } ] }, { "Name":"EDA Kunti League", "FactionState":"War", "Government":"PrisonColony", "Influence":0.404665, "Allegiance":"Independent", "Happiness":"$Faction_HappinessBand2;", "Happiness_Localised":"Happy", "SquadronFaction":True, "MyReputation":100.000000, "ActiveStates":[ { "State":"Boom" }, { "State":"War" } ] } ], "SystemFaction":{ "Name":"EDA Kunti League", "FactionState":"War" }, "Conflicts":[ { "WarType":"war", "Status":"active", "Faction1":{ "Name":"HR 1597 & Co", "Stake":"Elst Prospect", "WonDays":0 }, "Faction2":{ "Name":"EDA Kunti League", "Stake":"Jean City", "WonDays":1 } } ] })
    assert(tracker.pilot_state.last_docked_station != None)
    assert(tracker.pilot_state.last_docked_station.name == "Q3H-7HT")