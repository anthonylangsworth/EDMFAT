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
            "1 INF++ mission(s)\n"
            "2 INF+++ mission(s)\n"            
            "12,801,574 CR of Bounty Vouchers")
        ),
        (
            "EDA Kunti League", 
            "Journal.200913212207.01.log", 
            ("Kunti - ANTI\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "Shambogi - ANTI\n"
            "965,956 CR of Bounty Vouchers\n"
            "\n"
            "Shambogi - PRO\n"
            "7 INF++ mission(s)\n"
            "1 INF+++ mission(s)\n"
            "139,652 CR of Bounty Vouchers")
        ),
        (
            "EDA Kunti League", 
            "Journal.201018213100.01.log", 
            ("9 G. Carinae - ANTI\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "Kanates - PRO\n"
            "3 INF+++ mission(s)\n"
            "1 INF++++ mission(s)\n"
            "436,046 CR of Bounty Vouchers\n"
            "61,635 CR of Cartography Data\n"
            "\n"
            "Kutjara - ANTI\n"
            "1 INF++++ mission(s)")
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
            "Journal.201212203015.01.log",
            ("Antai - PRO\n"
            "2,840 T trade at 2,506 CR average profit per T")
        ),
        (
            "Green Party of Dulos", 
            "Journal.200630212114.01.log",
            ("Dulos - ANTI\n"
            "28 T trade at 44 CR average profit per T\n"
            "\n"
            "Dulos - PRO\n"
            "1 INF+++ mission(s)")
        ),
        (
            "EDA Kunti League", 
            "Journal.210102190919.01.log",
            ("Groanomana - PRO\n"
             "18,704,140 CR of Bounty Vouchers\n"
             "\n"
             "HR 1597 - PRO\n"
             "7,622,618 CR of Bounty Vouchers")
        ),
        (
            "EDA Kunti League", 
            "Journal.210105181410.01.log",
            ("Anek Wango - ANTI\n"
            "1 INF+ mission(s)\n"
            "1 INF++ mission(s)\n"
            "\n"
            "LHS 1832 - ANTI\n"
            "1 INF+ mission(s)\n"
            "1 INF++ mission(s)\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "LHS 1832 - PRO\n"
            "1 INF++ mission(s)\n"
            "194,136 CR of Bounty Vouchers\n"
            "12,039 CR of Cartography Data\n"
            "\n"
            "LPM 229 - ANTI\n"
            "1 INF+ mission(s)\n"
            "2 INF++ mission(s)\n"
            "\n"
            "LTT 2337 - ANTI\n"
            "2 INF+ mission(s)\n"
            "1 INF++ mission(s)\n"
            "6 T trade at -198 CR average profit per T\n"
            "\n"
            "LTT 2337 - PRO\n"
            "5 T trade at 265 CR average profit per T")
        )
    ])
def test_journal_file(minor_faction:str, journal_file_name:str, expected_activity:str):
    with open("tests/journal_files/" + journal_file_name) as journal_file:
        events = [json.loads(line) for line in journal_file.readlines()]

    tracker = Tracker(minor_faction)
    for event in events:
        tracker.on_event(event)
    assert(tracker.activity == expected_activity)


"""Anek Wango - ANTI
1 INF+ mission(s)
1 INF++ mission(s)

LHS 1832 - ANTI
1 INF+ mission(s)
1 INF++ mission(s)
1 INF+++ mission(s)

LHS 1832 - PRO
1 INF++ mission(s)
194,136 CR of Bounty Vouchers
12,039 CR of Cartography Data

LPM 229 - ANTI
1 INF+ mission(s)
2 INF++ mission(s)

LTT 2337 - ANTI
2 INF+ mission(s)
1 INF++ mission(s)
6 T trade at -198 CR average profit per T

LTT 2337 - PRO
5 T trade at 265 CR average profit per T"""