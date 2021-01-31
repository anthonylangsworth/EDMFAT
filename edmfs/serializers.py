import json
from typing import Dict

from .event_summaries import EventSummary
from .state import Mission
from .tracker import Tracker

def serialize_event_summary_v1(event_summary:EventSummary) -> Dict:
    

    return {
        "type": type(event_summary)
        "event_summary": 
    }

def serialize_mission_v1(mission:Mission) -> Dict:
    return {
        "id": mission.id,
        "minor_faction": mission.minor_faction,
        "influence": mission.influence,
        "system_address": mission.system_address
    }

def serialize_tracker_v1(tracker:Tracker) -> Dict:
    result = {
        "version": 1,
        "tracker": {
            "pilot_state": {
                "missions": [serialize_mission_v1(mission) for mission in tracker._pilot_state.missions]
            },
            "event_summaries": [event_summary for event_summary in tracker._event_summaries]
        }
    }
    return result

def serialize_tracker(tracker:Tracker) -> str:
    return json.dumps({
        "version": 1,
        "tracker": serialize_tracker_v1(tracker)
    })
