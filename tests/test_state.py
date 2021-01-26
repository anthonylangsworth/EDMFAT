import pytest

from edmfs.state import StarSystem, PilotState, Station, GalaxyState, Mission

def test_StarSystem_init():
    SYSTEM_NAME = "Deneb"
    ADDRESS = 89562036
    MINOR_FACTIONS = set(["EDA Kunti League", "Kunti Dragons"])
    star_system_state:StarSystem = StarSystem(SYSTEM_NAME, ADDRESS, MINOR_FACTIONS)
    assert(star_system_state.name == SYSTEM_NAME)
    assert(star_system_state.address == ADDRESS)
    assert(star_system_state.minor_factions == MINOR_FACTIONS)

def test_pilot_state_init():
    pilot_state:PilotState = PilotState()
    assert(pilot_state.last_docked_station == None)
    assert(pilot_state.missions == {})

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
    assert galaxy_state.systems == {}

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
    assert GalaxyState(resolver, star_systems).get_system(system_address) == expected_star_system

def test_galaxy_state_init_args():
    SYSTEMS = {1234: StarSystem("Sol", 1234, ["a", "b"])}
    galaxy_state = GalaxyState(None, SYSTEMS)
    assert galaxy_state.systems == SYSTEMS

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