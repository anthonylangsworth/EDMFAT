import pytest
import json
from typing import List

from edmfs.tracker import Tracker,_get_dummy_logger
from edmfs.serializers import TrackerFileRepository

@pytest.mark.parametrize(
    "minor_factions, journal_file_name",
    [
        ({"HR 1597 & Co"}, "Journal.201019220908.01.log"),
        ({"EDA Kunti League"}, "Journal.200913212207.01.log"), 
        ({"EDA Kunti League"}, "Journal.201018213100.01.log"), 
        ({"EDA Kunti League"}, "Journal.210101234033.01.log"),
        ({"EDA Kunti League"}, "Journal.201212203015.01.log"),
        ({"Green Party of Dulos"}, "Journal.200630212114.01.log"),
        ({"EDA Kunti League"}, "Journal.210102190919.01.log"),
        ({"EDA Kunti League"}, "Journal.210105181410.01.log"),
        ({"EDA Kunti League"}, "Journal.210105214916.01.log"),
        ({"EDA Kunti League", "LHS 1832 Labour"}, "Journal.210105214916.01.log"),
        ({"LHS 1832 Labour", "EDA Kunti League"}, "Journal.210105214916.01.log"),
        ({"EDA Kunti League"}, "LesPaul58_Journal.210117142551.01.log"),
        ({"EDA Kunti League"}, "Journal.210122183958.01.log"),
        ({"EDA Kunti League"}, "Journal.210125173739.01.log"),
        ({"EDA Kunti League"}, "Journal.210125115425.01.log")
    ]
)
def test_serialize_tracker(minor_factions:str, journal_file_name:str):
    tracker = Tracker(minor_factions)
    with open("tests/journal_files/" + journal_file_name) as journal_file:
        for line in journal_file.readlines():
            tracker.on_event(json.loads(line))
    repository = TrackerFileRepository()
    serialized_tracker = repository.serialize(tracker)
    new_tracker = repository.deserialize(serialized_tracker, None, None)

    assert tracker.minor_factions == new_tracker.minor_factions
    assert tracker.pilot_state.missions == new_tracker.pilot_state.missions
    assert tracker._event_summaries == new_tracker._event_summaries