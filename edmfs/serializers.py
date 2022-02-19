import json
import logging
from typing import Dict, Callable

from .event_summaries import EventSummary, RedeemVoucherEventSummary, SellExplorationDataEventSummary, MarketBuyEventSummary, MarketSellEventSummary, MissionCompletedEventSummary, MissionFailedEventSummary, MurderEventSummary
from .state import Mission
from .tracker import Tracker


class TrackerFileRepository:
    def _serialize_event_summary(self, event_summary: EventSummary) -> Dict:
        return {
            "pro": list(event_summary.pro),
            "anti": list(event_summary.anti),
            "system_name": event_summary.system_name,
        }

    def _serialize_redeem_voucher_event_summary(self, redeem_voucher_event_summary: RedeemVoucherEventSummary) -> Dict:
        return {
            **self._serialize_event_summary(redeem_voucher_event_summary),
            **{
                "voucher_type": redeem_voucher_event_summary.voucher_type,
                "amount": redeem_voucher_event_summary.amount
            }
        }

    def _serialize_sell_exploration_data_event_summary(self, sell_exploration_data_event_summary: SellExplorationDataEventSummary) -> Dict:
        return {
            **self._serialize_event_summary(sell_exploration_data_event_summary),
            **{
                "amount": sell_exploration_data_event_summary.amount
            }
        }

    def _serialize_market_sell_event_summary(self, market_sell_event_summary: MarketSellEventSummary) -> Dict:
        return {
            **self._serialize_event_summary(market_sell_event_summary),
            **{
                "count": market_sell_event_summary.count,
                "sell_price_per_unit": market_sell_event_summary.sell_price_per_unit,
                "average_buy_price_per_unit": market_sell_event_summary.average_buy_price_per_unit,
                "demand_bracket": market_sell_event_summary.demand_bracket
            }
        }

    def _serialize_market_buy_event_summary(self, market_buy_event_summary: MarketBuyEventSummary) -> Dict:
        return {
            **self._serialize_event_summary(market_buy_event_summary),
            **{
                "count": market_buy_event_summary.count,
                "buy_price_per_unit": market_buy_event_summary.buy_price_per_unit,
                "supply_bracket": market_buy_event_summary.supply_bracket
            }
        }

    def _serialize_mission_completed_event_summary(self, mission_completed_event_summary: MissionCompletedEventSummary) -> Dict:
        return {
            **self._serialize_event_summary(mission_completed_event_summary),
            **{
                "influence": mission_completed_event_summary.influence
            }
        }

    _event_summary_serializers = {
        "RedeemVoucherEventSummary": _serialize_redeem_voucher_event_summary,
        "SellExplorationDataEventSummary": _serialize_sell_exploration_data_event_summary,
        "MarketBuyEventSummary": _serialize_market_buy_event_summary,
        "MarketSellEventSummary": _serialize_market_sell_event_summary,
        "MissionCompletedEventSummary": _serialize_mission_completed_event_summary,
        "MissionFailedEventSummary": _serialize_event_summary,
        "MurderEventSummary": _serialize_event_summary
    }

    def _serialize_event_summary_v1(self, event_summary: EventSummary) -> Dict:
        return {
            "type": type(event_summary).__name__,
            "event_summary": self._event_summary_serializers[type(event_summary).__name__](self, event_summary)
        }

    def _serialize_mission_v1(self, mission: Mission) -> Dict:
        return {
            "id": mission.id,
            "minor_faction": mission.minor_faction,
            "influence": mission.influence,
            "system_address": mission.system_address
        }

    def _serialize_tracker_v1(self, tracker: Tracker) -> Dict:
        # Do not save the current system or last docked station from PilotState. Elite will set these when restarted.
        result = {
            "minor_factions": list(tracker.minor_factions),
            "show_anti": tracker.show_anti,
            "pilot_state": {
                "missions": [self._serialize_mission_v1(mission) for mission in tracker._pilot_state.missions.values()]
            },
            "event_summaries": [self._serialize_event_summary_v1(event_summary) for event_summary in tracker._event_summaries]
        }
        return result

    def serialize(self, tracker: Tracker) -> str:
        return json.dumps({
            "version": 1,
            "tracker": self._serialize_tracker_v1(tracker)
        }, indent=4)

    def _deserialize_redeem_voucher_event_summary(self, deserialized_event_summary) -> EventSummary:
        return RedeemVoucherEventSummary(deserialized_event_summary["system_name"], deserialized_event_summary["pro"],
            deserialized_event_summary["anti"], deserialized_event_summary["voucher_type"], deserialized_event_summary["amount"])

    def _deserialize_sell_exploration_data_event_summary(self, deserialized_event_summary) -> EventSummary:
        return SellExplorationDataEventSummary(deserialized_event_summary["system_name"], deserialized_event_summary["pro"],
            deserialized_event_summary["anti"], deserialized_event_summary["amount"])

    def _deserialize_market_buy_event_summary(self, deserialized_event_summary) -> EventSummary:
        return MarketBuyEventSummary(deserialized_event_summary["system_name"], deserialized_event_summary["pro"],
            deserialized_event_summary["anti"], deserialized_event_summary["count"], deserialized_event_summary["buy_price_per_unit"],
            deserialized_event_summary["supply_bracket"])

    def _deserialize_market_sell_event_summary(self, deserialized_event_summary) -> EventSummary:
        return MarketSellEventSummary(deserialized_event_summary["system_name"], deserialized_event_summary["pro"],
            deserialized_event_summary["anti"], deserialized_event_summary["count"], deserialized_event_summary["sell_price_per_unit"],
            deserialized_event_summary["average_buy_price_per_unit"], deserialized_event_summary.get("demand_bracket", 0))

    def _deserialize_mission_completed_event_summary(self, deserialized_event_summary) -> EventSummary:
        return MissionCompletedEventSummary(deserialized_event_summary["system_name"], deserialized_event_summary["pro"],
            deserialized_event_summary["anti"], deserialized_event_summary["influence"])

    def _deserialize_mission_failed_event_summary(self, deserialized_event_summary) -> EventSummary:
        return MissionFailedEventSummary(deserialized_event_summary["system_name"], deserialized_event_summary["pro"],
            deserialized_event_summary["anti"])

    def _deserialize_murder_event_summary(self, deserialized_event_summary) -> EventSummary:
        return MurderEventSummary(deserialized_event_summary["system_name"], deserialized_event_summary["pro"],
            deserialized_event_summary["anti"])

    def _deserialize_event_summary_v1(self, deserialied_event_summary) -> EventSummary:
        return self._event_summary_deserializers[deserialied_event_summary["type"]](self, deserialied_event_summary["event_summary"])

    _event_summary_deserializers = {
        "RedeemVoucherEventSummary": _deserialize_redeem_voucher_event_summary,
        "SellExplorationDataEventSummary": _deserialize_sell_exploration_data_event_summary,
        "MarketBuyEventSummary": _deserialize_market_buy_event_summary,
        "MarketSellEventSummary": _deserialize_market_sell_event_summary,
        "MissionCompletedEventSummary": _deserialize_mission_completed_event_summary,
        "MissionFailedEventSummary": _deserialize_mission_failed_event_summary,
        "MurderEventSummary": _deserialize_murder_event_summary
    }

    def _deserialize_mission_v1(self, deserialized_mission) -> Mission:
        return Mission(deserialized_mission["id"], deserialized_mission["minor_faction"],
            deserialized_mission["influence"], deserialized_mission["system_address"])

    def _deserialize_tracker_v1(self, deserialized_tracker: dict, logger: logging.Logger, star_system_resolver: Callable, get_last_market: Callable[[str], Dict[str, Dict]]) -> Tracker:
        tracker = Tracker(deserialized_tracker["minor_factions"], deserialized_tracker.get("show_anti", True), logger, star_system_resolver=star_system_resolver, get_last_market=get_last_market)
        tracker.pilot_state.missions.update([(mission["id"], self._deserialize_mission_v1(mission)) for mission in deserialized_tracker["pilot_state"]["missions"]])
        # Consider moving these into tracker
        tracker._event_summaries.extend([self._deserialize_event_summary_v1(event_summary) for event_summary in deserialized_tracker["event_summaries"]])
        tracker._update_activity()
        return tracker

    _deserializers = {
        1: _deserialize_tracker_v1
    }

    def deserialize(self, serialized_tracker: str, logger: logging.Logger, star_system_resolver: Callable, get_last_market: Callable[[str], Dict[str, Dict]]) -> Tracker:
        deserialized_tracker = json.loads(serialized_tracker)
        return self._deserializers[deserialized_tracker["version"]](self, deserialized_tracker["tracker"], logger, star_system_resolver, get_last_market)
