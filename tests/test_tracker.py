from edmfs.tracker import Tracker, StarSystemState, PilotState, Station

def test_Tracker_init():
    MINOR_FACTION = "EDA Kunti League"
    tracker:Tracker = Tracker(MINOR_FACTION)
    assert(tracker.minor_faction == MINOR_FACTION)

def test_StarSystemState_init():
    SYSTEM_NAME = "Deneb"
    ADDRESS = 89562036
    MINOR_FACTIONS = ("EDA Kunti League", "Kunti Dragons")
    star_system_state:StarSystemState = StarSystemState(SYSTEM_NAME, ADDRESS, MINOR_FACTIONS)
    assert(star_system_state.name == SYSTEM_NAME)
    assert(star_system_state.address == ADDRESS)
    assert(star_system_state.minor_factions == MINOR_FACTIONS)

def test_PilotState_init():
    LAST_DOCKED_STATION = "Hughes Enterprise"
    MISSIONS = [] # TODO
    pilot_state:PilotState = PilotState(LAST_DOCKED_STATION, MISSIONS)
    assert(pilot_state.last_docked_station == LAST_DOCKED_STATION)
    assert(pilot_state.missions == MISSIONS)

def test_Station_init():
    NAME = "Syromyatnikov Terminal"
    SYSTEM_ADDRESS = 927490167
    CONTROLLING_MINOR_FACTION = "EDA Kunti League"
    station:Station = Station(NAME, SYSTEM_ADDRESS, CONTROLLING_MINOR_FACTION)
    assert(station.name == NAME)
    assert(station.system_address == SYSTEM_ADDRESS)
    assert(station.controlling_minor_faction == CONTROLLING_MINOR_FACTION)