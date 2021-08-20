import pytest
import copy
import json
import itertools
import logging
import io
from typing import List

from edmfs.state import PilotState, GalaxyState, Station
from edmfs.tracker import Tracker
    
def test_tracker_init():
    MINOR_FACTIONS = ("EDA Kunti League",)
    tracker = Tracker(MINOR_FACTIONS)
    assert(tracker.minor_factions == MINOR_FACTIONS)
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
            ""
        ),
        (
            {
                "EDA Kunti League"
            },
            "Journal.210125173739.01.log",
            (
                "San Davokje - ANTI EDA Kunti League\n"
                "80 T trade at 3,477 CR average profit per T\n"
                "\n"
                "San Davokje - PRO EDA Kunti League\n1 INF++++ mission(s)"
            )
        ),
        (
            {
                "EDA Kunti League"
            },
            "Journal.210125115425.01.log",
            (
                "HR 1597 - PRO EDA Kunti League\n"
                "5 T trade at 3,734 CR average profit per T"
            )
        ),
        (
            {
                "Yuri Grom"
            },
            "Journal.210120211308.01.log",
            ("Eta-1 Pictoris - ANTI Yuri Grom\n"
            "26 clean ship kill(s)")
        ),
        (
            {"Atfero Blue General & Co"},
            "Journal.200509115806.01.log",
            ("Atfero - ANTI Atfero Blue General & Co\n"
            "2 INF+ mission(s)\n"
            "3 INF++ mission(s)\n"
            "77 T trade at 1,048 CR average profit per T\n"
            "1 failed mission(s)\n"
            "\n"
            "Atfero - PRO Atfero Blue General & Co\n"
            "4 INF+ mission(s)\n"
            "1 INF++ mission(s)")
        ),
        (
            {"EDA Kunti League"},
            "Journal.210212124540.01.log",
            ("Anek Wango - ANTI EDA Kunti League\n"
            "1,168 T trade at -1,000 CR average profit per T\n"
            "\n"
            "Herci - PRO EDA Kunti League\n"
            "2,930,517 CR of Combat Bonds\n"
            "\n"
            "Trumuye - ANTI EDA Kunti League\n"
            "3,136 T trade at -1,000 CR average profit per T")
        ),
        (
            {"EDA Kunti League"},
            "Journal.210221171753.01.log",
            ("Kunti - PRO EDA Kunti League\n"
            "1 INF+ mission(s)\n"
            "1 INF++ mission(s)\n"
            "2 INF+++ mission(s)\n"
            "2 INF++++ mission(s)\n"
            "1 INF+++++ mission(s)\n"
            "348,491 CR of Bounty Vouchers\n"
            "10,402 CR of Cartography Data\n"
            "\n"
            "LTT 2337 - ANTI EDA Kunti League\n"
            "1 INF+++++ mission(s)")
        ),
        (
            {"Federal Defense League"},
            "Journal.210225200231.01.log",
            ("LHS 1832 - PRO Federal Defense League\n"
            "2 INF++ mission(s)\n"
            "11,772,015 CR of Combat Bonds")
        ),
        (
            {"EDA Kunti League"},
            "Journal.210817213224.01.log",
            ("")    
        ),
        (
            {"EDA Kunti League"},
            "Journal.210818120219.01.log",
            ("")
        )
    ])
def test_journal_file(minor_factions:List[str], journal_file_name:str, expected_activity:str):
    tracker = Tracker(minor_factions)
    with open("tests/journal_files/" + journal_file_name) as journal_file:
        for line in journal_file.readlines():
            tracker.on_event(json.loads(line))

    # Sanity checks
    assert len([event_summary for event_summary in tracker._event_summaries if not set(event_summary.pro).isdisjoint(set(event_summary.anti))]) == 0 # No overlaps
    # assert len([event_summary for event_summary in tracker._event_summaries if len(event_summary.pro) == 0]) == 0  # No empty pro (can happen if system is not found)
    # assert len([event_summary for event_summary in tracker._event_summaries if len(event_summary.anti) == 0]) == 0  # No empty anti (can happen if system is not found)

    # tracker._update_activity()
    assert tracker.activity == expected_activity
    #print(stream.getvalue())

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

@pytest.mark.parametrize(
    "journal_file_name, minor_factions_and_expected_activty",
    [
        (
            "Journal.210125173739.01.log",
            [
                (
                    {"EDA Kunti League"},
                    (
                        "San Davokje - ANTI EDA Kunti League\n"
                        "80 T trade at 3,477 CR average profit per T\n"
                        "\n"
                        "San Davokje - PRO EDA Kunti League\n"
                        "1 INF++++ mission(s)"
                    )
                ),
                (
                    {"San Davokje Empire Party"},
                    (
                        "San Davokje - ANTI San Davokje Empire Party\n"
                        "1 INF++++ mission(s)\n"
                        "\n"
                        "San Davokje - PRO San Davokje Empire Party\n"
                        "80 T trade at 3,477 CR average profit per T"
                    )
                )
            ]
        )
    ]
)
def test_tracker_change_minor_factions(journal_file_name:str, minor_factions_and_expected_activty:List):
    tracker = Tracker([])
    with open("tests/journal_files/" + journal_file_name) as journal_file:
        for line in journal_file.readlines():
            tracker.on_event(json.loads(line))
    for minor_factions, expected_activity in minor_factions_and_expected_activty:
        tracker.minor_factions = minor_factions
        assert tracker.activity == expected_activity