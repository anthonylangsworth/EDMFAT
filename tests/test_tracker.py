import pytest
import copy
import json
import itertools
import logging
import io

from edmfs.state import PilotState, GalaxyState, Station
from edmfs.tracker import Tracker
    
def test_tracker_init():
    MINOR_FACTIONS = ["EDA Kunti League"]
    tracker = Tracker(MINOR_FACTIONS)
    assert(tracker.minor_factions == set(MINOR_FACTIONS))
    assert(tracker.pilot_state == PilotState())
    assert(tracker.galaxy_state == GalaxyState())
    assert(tracker.activity == "")

@pytest.mark.parametrize(
    "minor_factions, journal_file_name, expected_activity",
    [
        (
            {"HR 1597 & Co"}, 
            "Journal.201019220908.01.log", 
            ("HR 1597 - ANTI HR 1597 & Co\n"
            "1,852,906 CR of Bounty Vouchers\n"
            "\n"
            "HR 1597 - PRO HR 1597 & Co\n"
            "1 INF++ mission(s)\n"
            "2 INF+++ mission(s)\n"            
            "12,801,574 CR of Bounty Vouchers")
        ),
        (
            {"EDA Kunti League"}, 
            "Journal.200913212207.01.log", 
            ("Kunti - ANTI EDA Kunti League\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "Shambogi - ANTI EDA Kunti League\n"
            "965,956 CR of Bounty Vouchers\n"
            "\n"
            "Shambogi - PRO EDA Kunti League\n"
            "7 INF++ mission(s)\n"
            "1 INF+++ mission(s)\n"
            "139,652 CR of Bounty Vouchers")
        ),
        (
            {"EDA Kunti League"}, 
            "Journal.201018213100.01.log", 
            ("9 G. Carinae - ANTI EDA Kunti League\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "Kanates - PRO EDA Kunti League\n"
            "3 INF+++ mission(s)\n"
            "1 INF++++ mission(s)\n"
            "436,046 CR of Bounty Vouchers\n"
            "61,635 CR of Cartography Data\n"
            "\n"
            "Kutjara - ANTI EDA Kunti League\n"
            "1 INF++++ mission(s)")
        ),
        (
            {"EDA Kunti League"}, 
            "Journal.210101234033.01.log",
            ("HR 1597 - PRO EDA Kunti League\n"
            "559,467 CR of Combat Bonds\n"
            "\n"
            "LTT 2337 - PRO EDA Kunti League\n"
            "718,360 CR of Bounty Vouchers\n"
            "141,361 CR of Cartography Data\n"
            "\n"
            "Shambogi - PRO EDA Kunti League\n"
            "50,765 CR of Cartography Data")
        ),
        (
            {"EDA Kunti League"}, 
            "Journal.201212203015.01.log",
            ("Antai - PRO EDA Kunti League\n"
            "2,840 T trade at 2,506 CR average profit per T")
        ),
        (
            {"Green Party of Dulos"}, 
            "Journal.200630212114.01.log",
            ("Dulos - ANTI Green Party of Dulos\n"
            "28 T trade at 44 CR average profit per T\n"
            "\n"
            "Dulos - PRO Green Party of Dulos\n"
            "1 INF+++ mission(s)")
        ),
        (
            {"EDA Kunti League"}, 
            "Journal.210102190919.01.log",
            ("Groanomana - PRO EDA Kunti League\n"
             "18,704,140 CR of Bounty Vouchers\n"
             "\n"
             "HR 1597 - PRO EDA Kunti League\n"
             "7,622,618 CR of Bounty Vouchers")
        ),
        (
            {"EDA Kunti League"}, 
            "Journal.210105181410.01.log",
            ("Anek Wango - ANTI EDA Kunti League\n"
            "1 INF+ mission(s)\n"
            "1 INF++ mission(s)\n"
            "\n"
            "LHS 1832 - ANTI EDA Kunti League\n"
            "1 INF+ mission(s)\n"
            "1 INF++ mission(s)\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "LHS 1832 - PRO EDA Kunti League\n"
            "1 INF++ mission(s)\n"
            "194,136 CR of Bounty Vouchers\n"
            "12,039 CR of Cartography Data\n"
            "\n"
            "LPM 229 - ANTI EDA Kunti League\n"
            "1 INF+ mission(s)\n"
            "2 INF++ mission(s)\n"
            "\n"
            "LTT 2337 - ANTI EDA Kunti League\n"
            "2 INF+ mission(s)\n"
            "1 INF++ mission(s)\n"
            "6 T trade at -198 CR average profit per T\n"
            "\n"
            "LTT 2337 - PRO EDA Kunti League\n"
            "5 T trade at 265 CR average profit per T")
        ),
        (
            {"EDA Kunti League"}, 
            "Journal.210105214916.01.log",
            ("LHS 1832 - ANTI EDA Kunti League\n"
            "1 INF+ mission(s)\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "Shongbon - ANTI EDA Kunti League\n"
            "1 INF+++ mission(s)")
        ),
        (
            {
                "EDA Kunti League",
                "LHS 1832 Labour"
            }, 
            "Journal.210105214916.01.log",
            ("LHS 1832 - ANTI EDA Kunti League\n"
            "1 INF+ mission(s)\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "Shongbon - ANTI EDA Kunti League\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "LHS 1832 - ANTI LHS 1832 Labour\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "LHS 1832 - PRO LHS 1832 Labour\n"
            "1 INF+ mission(s)")
        ),
        (
            [
                "LHS 1832 Labour",
                "EDA Kunti League"
            ], 
            "Journal.210105214916.01.log",
            ("LHS 1832 - ANTI EDA Kunti League\n"
            "1 INF+ mission(s)\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "Shongbon - ANTI EDA Kunti League\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "LHS 1832 - ANTI LHS 1832 Labour\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "LHS 1832 - PRO LHS 1832 Labour\n"
            "1 INF+ mission(s)")
        ),
        (
            [
                "EDA Kunti League"
            ], 
            "LesPaul58_Journal.210117142551.01.log",
            ("Arun - ANTI EDA Kunti League\n"
            "1 INF+++++ mission(s)\n"
            "\n"
            "LHS 1832 - ANTI EDA Kunti League\n"    
            "2 T trade at 51,622 CR average profit per T\n"
            "\n"
            "Trumuye - ANTI EDA Kunti League\n"
            "7 INF++ mission(s)\n"
            "3 INF+++ mission(s)\n"
            "8 INF+++++ mission(s)")
        ),
        (
            {
                "EDA Kunti League"
            }, 
            "696613390.log",
            ("Trumuye - ANTI EDA Kunti League\n"
            "1 INF+++ mission(s)")
        ),
        (
            {
                "EDA Kunti League"
            }, 
            "696609571.log",
            ("Trumuye - ANTI EDA Kunti League\n"
            "1 INF++ mission(s)")
        ),
        (
            {
                "EDA Kunti League"
            },
            "Journal.210122183958.01.log",
            ("")
        )
    ])
def test_journal_file(minor_factions:str, journal_file_name:str, expected_activity:str):
    with open("tests/journal_files/" + journal_file_name) as journal_file:
        events = [json.loads(line) for line in journal_file.readlines()]

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    with io.StringIO() as stream:
        logger.addHandler(logging.StreamHandler(stream))

        tracker = Tracker(minor_factions, logger)
        for event in events:
            tracker.on_event(event)
        assert tracker.activity == expected_activity, f"{print(tracker.activity)}\ndoes not match:\n{print(expected_activity)}"
        print(stream.getvalue())

@pytest.mark.parametrize(
    "journal_file_name",
    [
        None,
        "Journal.201019220908.01.log"
    ]
)
def test_tracker_clear_activity(journal_file_name):
    events = []
    if(journal_file_name):
        with open("tests/journal_files/" + journal_file_name) as journal_file:
            events = [json.loads(line) for line in journal_file.readlines()]

    MINOR_FACTIONS = set(["EDA Kunti League"])
    tracker = Tracker(MINOR_FACTIONS)
    for event in events:
        tracker.on_event(event)
    tracker.clear_activity()
    assert(tracker.activity == "")
    assert(tracker._event_summaries == [])