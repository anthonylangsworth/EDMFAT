import pytest
import copy
import json

from edmfs.state import PilotState, GalaxyState, Station
from edmfs.tracker import Tracker
    
def test_tracker_init():
    MINOR_FACTION = "EDA Kunti League"
    tracker = Tracker(MINOR_FACTION)
    assert(tracker.minor_faction == MINOR_FACTION)
    assert(tracker.pilot_state == PilotState())
    assert(tracker.galaxy_state == GalaxyState())
    assert(tracker.activity == "")

@pytest.mark.parametrize(
    "minor_faction, journal_file_name, expected_activity",
    [
        (
            "HR 1597 & Co", 
            "Journal.201019220908.01.log", 
            ("RedeemVoucherEventSummary('unknown', True, 'bounty', 233160)\n"
            "RedeemVoucherEventSummary('unknown', True, 'bounty', 12568414)")
        )
    ])
def test_journal_file(minor_faction:str, journal_file_name:str, expected_activity:str):
    with open("tests/" + journal_file_name) as journal_file:
        events = [json.loads(line) for line in journal_file.readlines()]

    tracker = Tracker(minor_faction)
    for event in events:
        tracker.on_event(event)
    assert(tracker.activity == expected_activity)
