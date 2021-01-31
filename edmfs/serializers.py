import json
from typing import Dict

from .event_summaries import EventSummary, RedeemVoucherEventSummary, SellExplorationDataEventSummary, MarketSellEventSummary, MissionCompletedEventSummary
from .state import Mission
from .tracker import Tracker

def serialize_event_summary(event_summary:EventSummary) -> Dict:
    return {
        "minor_faction": redeem_voucher_event_summary.minor_faction,
        "supports": redeem_voucher_event_summary.supports,
        "system_name": redeem_voucher_event_summary.system_name,
    }

def serialize_redeem_voucher_event_summary(redeem_voucher_event_summary:RedeemVoucherEventSummary) -> Dict:
    return {
        **serialize_event_summary(redeem_voucher_event_summary),
        **{
            "voucher_type": redeem_voucher_event_summary.voucher_type,
        }
    }

def serialize_sell_exploration_data_event_summary(sell_exploration_data_event_summary:SellExplorationDataEventSummary) -> Dict:
    return {
        **serialize_event_summary(redeem_voucher_event_summary),
        **{
            "amount": sell_exploration_data_event_summary.amount
        }
    }    

def serialize_market_sell_event_summary(market_sell_event_summary:SellExplorationDataEventSummary) -> Dict:
    return {
        **serialize_event_summary(redeem_voucher_event_summary),
        **{
            "amount": sell_exploration_data_event_summary.amount
        }
    }    


def serialize_event_summary_v1(event_summary:EventSummary) -> Dict:
    event_summary_serializers = {
        "RedeemVoucherEventSummary": serialize_redeem_voucher_event_summary,
        "SellExplorationDataEventSummary": serialize_sell_exploration_data_event_summary,
        "MarketSellEventSummary": None,
        "MissionCompletedEventSummary": None
    }

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
    }, indent=4)
