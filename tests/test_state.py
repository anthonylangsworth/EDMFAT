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
    assert(station.name == NAME)
    assert(station.system_address == SYSTEM_ADDRESS)
    assert(station.controlling_minor_faction == CONTROLLING_MINOR_FACTION)

def test_galaxy_state_init():
    galaxy_state = GalaxyState()
    assert(galaxy_state.systems == {})

def test_galaxy_state_init_args():
    SYSTEMS = {1234: StarSystem("Sol", 1234, ["a", "b"])}
    galaxy_state = GalaxyState(SYSTEMS)
    assert(galaxy_state.systems == SYSTEMS)

def test_mission_init():
    ID = 564728
    MINOR_FACTION = "The Dark Wheel"
    INFLUENCE = "+++"
    SYSTEM_ADDRESS = 86306249
    mission = Mission(ID, MINOR_FACTION, INFLUENCE, SYSTEM_ADDRESS)
    assert(mission.id == ID)
    assert(mission.minor_faction == MINOR_FACTION)
    assert(mission.influence == INFLUENCE)
    assert(mission.system_address == SYSTEM_ADDRESS)