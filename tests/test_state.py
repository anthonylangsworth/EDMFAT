import pytest

from edmfs.state import StarSystem, PilotState, Station, GalaxyState

def test_StarSystem_init():
    SYSTEM_NAME = "Deneb"
    ADDRESS = 89562036
    MINOR_FACTIONS = ("EDA Kunti League", "Kunti Dragons")
    star_system_state:StarSystem = StarSystem(SYSTEM_NAME, ADDRESS, MINOR_FACTIONS)
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

def test_GalaxyState_init():
    galaxy_state = GalaxyState()
    assert(galaxy_state.systems == {})
