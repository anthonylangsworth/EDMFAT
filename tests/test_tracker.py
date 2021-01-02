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
            ("HR 1597 - ANTI\n"
            "1,916,227 CR of Bounty Vouchers\n"
            "\n"
            "HR 1597 - PRO\n"
            "12,801,574 CR of Bounty Vouchers")
        ),
        (
            "Maxwell Corp. of Eta-1 Pictoris", 
            "Journal.200913212207.01.log", 
            ("Erh Lohra - ANTI\n"
            "106,428 CR of Bounty Vouchers\n"
            "\n"
            "Eta-1 Pictoris - ANTI\n"
            "12,150 CR of Bounty Vouchers\n"
            "\n"
            "Eta-1 Pictoris - PRO\n"
            "1,882,292 CR of Bounty Vouchers\n"
            "\n"
            "Shambogi - ANTI\n"
            "1,105,608 CR of Bounty Vouchers\n"
            "\n"
            "Verner - ANTI\n"
            "74,922 CR of Bounty Vouchers")
        ),
        (
            "HR 1597 & Co", 
            "Journal.201018213100.01.log", 
            ("HR 1597 - ANTI\n"
            "1,662,746 CR of Bounty Vouchers\n"
            "\n"
            "HR 1597 - PRO\n"
            "1,127,126 CR of Combat Bonds\n"
            "\n"
            "Kanates - ANTI\n"
            "436,046 CR of Bounty Vouchers\n"
            "61,635 CR of Cartography Data")
        ),
        (
            "EDA Kunti League", 
            "Journal.210101234033.01.log",
            ("HR 1597 - PRO\n"
            "559,467 CR of Combat Bonds\n"
            "\n"
            "LTT 2337 - PRO\n"
            "718,360 CR of Bounty Vouchers\n"
            "141,361 CR of Cartography Data\n"
            "\n"
            "Shambogi - PRO\n"
            "50,765 CR of Cartography Data")
        ),
        (
            "EDA Kunti League", 
            "Journal.210102125854.01.log",
            ("Shambogi - ANTI\n"
            "1,209,935 CR of Combat Bonds\n"
            "54,881 CR of Cartography Data\n"
            "\n"
            "Shambogi - PRO\n"
            "374,299 CR of Bounty Vouchers")
        )
    ])
def test_journal_file(minor_faction:str, journal_file_name:str, expected_activity:str):
    with open("tests/journal_files/" + journal_file_name) as journal_file:
        events = [json.loads(line) for line in journal_file.readlines()]

    tracker = Tracker(minor_faction)
    for event in events:
        tracker.on_event(event)
    assert(tracker.activity == expected_activity)
