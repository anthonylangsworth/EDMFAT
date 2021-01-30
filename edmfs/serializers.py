import json

from .tracker import Tracker

def serialize_tracker_v1(tracker:Tracker):
    result = {
        "version": 1,
        "tracker": {
            "pilot_state": {
                "missions": [mission for mission in tracker._pilot_state.missions]
            },
            "event_summaries": [event_summary for event_summary in tracker._event_summaries]
        }
    }
    return result

def serialize_tracker(tracker:Tracker) -> str:
    return json.dumps(serialize_tracker_v1)