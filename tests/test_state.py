import pytest
from typing import Dict

from edmfs.event_processors import UnknownStarSystemError
from edmfs.state import StarSystem, PilotState, Station, GalaxyState, Mission, ResolvingDict

def test_StarSystem_init():
    SYSTEM_NAME = "Deneb"
    ADDRESS = 89562036
    MINOR_FACTIONS = set(["EDA Kunti League", "Kunti Dragons"])
    star_system_state:StarSystem = StarSystem(SYSTEM_NAME, ADDRESS, MINOR_FACTIONS)
    assert star_system_state.name == SYSTEM_NAME
    assert star_system_state.address == ADDRESS
    assert star_system_state.minor_factions == MINOR_FACTIONS

def test_pilot_state_init():
    pilot_state = PilotState()
    assert pilot_state.last_docked_station == None
    assert pilot_state.missions == {}

def test_pilot_state_init_args():
    SYSTEM_ADDRESS = 98367212
    STATION = Station("Pu City", 98367212, set(["Afli Patron's Principles", "Afli Imperial Society"]))
    MISSIONS = dict()
    pilot_state = PilotState(SYSTEM_ADDRESS, STATION, MISSIONS)
    assert pilot_state.system_address == SYSTEM_ADDRESS
    assert pilot_state.last_docked_station == STATION
    assert pilot_state.missions == MISSIONS

def test_station_init():
    NAME = "Syromyatnikov Terminal"
    SYSTEM_ADDRESS = 927490167
    CONTROLLING_MINOR_FACTION = "EDA Kunti League"
    station:Station = Station(NAME, SYSTEM_ADDRESS, CONTROLLING_MINOR_FACTION)
    assert station.name == NAME
    assert station.system_address == SYSTEM_ADDRESS
    assert station.controlling_minor_faction == CONTROLLING_MINOR_FACTION

def test_galaxy_state_init():
    galaxy_state = GalaxyState()
    assert galaxy_state.systems == ResolvingDict(None)

def test_galaxy_state_init_args():
    SYSTEMS = {1234: StarSystem("Sol", 1234, ["a", "b"])}
    galaxy_state = GalaxyState(None, SYSTEMS)
    assert galaxy_state.systems == ResolvingDict(None, SYSTEMS)

@pytest.mark.parametrize(
    "resolver, star_systems, system_address, expected_star_system",
    [
        (None, {}, 1234, None),
        (None, {1234:StarSystem("a", 1234, [])}, 1234, StarSystem("a", 1234, [])),
        (None, {1234:StarSystem("a", 1234, [])}, 5678, None),
        ((lambda x: StarSystem("b", 5678, []) if x == 5678 else None), {}, 5678, StarSystem("b", 5678, [])),
        ((lambda x: StarSystem("b", 5678, []) if x == 5678 else None), {1234:StarSystem("a", 1234, [])}, 1987, None),
        ((lambda x: StarSystem("b", 5678, []) if x == 5678 else None), {1234:StarSystem("a", 1234, [])}, 1234, StarSystem("a", 1234, [])),
        ((lambda x: StarSystem("b", 5678, []) if x == 5678 else None), {}, 1234, None),
        ((lambda x: StarSystem("b", 5678, []) if x == 5678 else None), {1234:StarSystem("a", 1234, [])}, 5678, StarSystem("b", 5678, [])),
    ]
)
def test_galaxy_state_get_system(resolver, star_systems, system_address, expected_star_system):
    galaxy_state = GalaxyState(resolver, star_systems)
    assert galaxy_state.systems.get(system_address, None) == expected_star_system

@pytest.mark.parametrize(
    "commodity_name, expected_result",
    [
        ("Platinum", {"BuyPrice":30908, "SellPrice":30906, "MeanPrice":58263, "StockBracket":0, "DemandBracket":0, "Stock":0}),
        ("Animal Meat", {"BuyPrice":0, "SellPrice":1864, "MeanPrice":1539, "StockBracket":0, "DemandBracket":3, "Stock":0}),
        ("Classified Experimental Equipment", {"BuyPrice":4002, "SellPrice":4001, "MeanPrice":11423, "StockBracket":0, "DemandBracket":0, "Stock":0}),
        ("Not A Commodity", None)
    ]
)
def test_galaxy_state_get_last_market_entry(commodity_name:str, expected_result:Dict):
    market_entry = GalaxyState().get_last_market_entry(commodity_name, "tests/market_files/market.json")
    if expected_result:
        assert market_entry["Name_Localised"] == commodity_name
        for key in expected_result:
            assert market_entry[key] == expected_result[key]
    else:
        assert not market_entry

def raise_error(x):
    raise UnknownStarSystemError(x)

def test_galaxy_state_get_system_error():
    galaxy_state = GalaxyState(raise_error) 
    try:
        galaxy_state.systems.get(1, None)
        assert False
    except UnknownStarSystemError:
        assert True

def test_mission_init():
    ID = 564728
    MINOR_FACTION = "The Dark Wheel"
    INFLUENCE = "+++"
    SYSTEM_ADDRESS = 86306249
    mission = Mission(ID, MINOR_FACTION, INFLUENCE, SYSTEM_ADDRESS)
    assert mission.minor_faction == MINOR_FACTION
    assert mission.id == ID
    assert mission.influence == INFLUENCE
    assert mission.system_address == SYSTEM_ADDRESS
