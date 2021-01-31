import json
from typing import Dict

from .event_summaries import EventSummary, RedeemVoucherEventSummary, SellExplorationDataEventSummary, MarketSellEventSummary, MissionCompletedEventSummary
from .state import Mission
from .tracker import Tracker

def _serialize_event_summary(event_summary:EventSummary) -> Dict:
    return {
        "minor_faction": event_summary.minor_faction,
        "supports": event_summary.supports,
        "system_name": event_summary.system_name,
    }

def _serialize_redeem_voucher_event_summary(redeem_voucher_event_summary:RedeemVoucherEventSummary) -> Dict:
    return {
        **_serialize_event_summary(redeem_voucher_event_summary),
        **{
            "voucher_type": redeem_voucher_event_summary.voucher_type,
        }
    }

def _serialize_sell_exploration_data_event_summary(sell_exploration_data_event_summary:SellExplorationDataEventSummary) -> Dict:
    return {
        **_serialize_event_summary(sell_exploration_data_event_summary),
        **{
            "amount": sell_exploration_data_event_summary.amount
        }
    }    

def _serialize_market_sell_event_summary(market_sell_event_summary:MarketSellEventSummary) -> Dict:
    return {
        **_serialize_event_summary(market_sell_event_summary),
        **{
            "count": market_sell_event_summary.count,
            "sell_price_per_unit": market_sell_event_summary.sell_price_per_unit,
            "average_buy_price_per_unit": market_sell_event_summary.average_buy_price_per_unit
        }
    }    

def _serialize_mission_completed_event_summary(mission_completed_event_summary:MissionCompletedEventSummary) -> Dict:
    return {
        **_serialize_event_summary(mission_completed_event_summary),
        **{
            "influence": mission_completed_event_summary.count
        }
    }    

_event_summary_serializers = {
    "RedeemVoucherEventSummary": _serialize_redeem_voucher_event_summary,
    "SellExplorationDataEventSummary": _serialize_sell_exploration_data_event_summary,
    "MarketSellEventSummary": _serialize_market_sell_event_summary,
    "MissionCompletedEventSummary": _serialize_mission_completed_event_summary
}

def _serialize_event_summary_v1(event_summary:EventSummary) -> Dict:
    return {
        "type": type(event_summary),
        "event_summary": _event_summary_serializers[type(event_summary)]
    }

def _serialize_mission_v1(mission:Mission) -> Dict:
    return {
        "id": mission.id,
        "minor_faction": mission.minor_faction,
        "influence": mission.influence,
        "system_address": mission.system_address
    }

def _serialize_tracker_v1(tracker:Tracker) -> Dict:
    result = {
        "version": 1,
        "tracker": {
            "pilot_state": {
                "missions": [_serialize_mission_v1(mission) for mission in tracker._pilot_state.missions]
            },
            "event_summaries": [_serialize_event_summary_v1(event_summary) for event_summary in tracker._event_summaries]
        }
    }
    return result

def serialize_tracker(tracker:Tracker) -> str:
    return json.dumps({
        "version": 1,
        "tracker": _serialize_tracker_v1(tracker)
    }, indent=4)
