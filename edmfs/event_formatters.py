from abc import abstractmethod, ABC
from itertools import groupby, accumulate
from typing import Dict
import operator

class EventFormatter(ABC):
    @abstractmethod
    def process(self, event_summaries: list) -> str:
        pass

class RedeemVoucherEventFormatter(EventFormatter):
    def process(self, event_summaries: iter) -> str:
        result = ""
        _redeem_voucher_order = (
            "bounty",
            "CombatBond"
        )      
        _voucher_type_lookup:Dict[str, str] = {
            #"scannable" : "Scan Data",
            "bounty" : "Bounty Vouchers",
            "CombatBond" : "Combat Bonds"
        }          
        for voucher_type, event_summaries_by_type in groupby(sorted(event_summaries, key=lambda x: _redeem_voucher_order.index(x.voucher_type)), key=lambda x: x.voucher_type):
            result += f"{sum(map(lambda es: es.amount, event_summaries_by_type)):,} CR of {_voucher_type_lookup.get(voucher_type, voucher_type)}\n"
        return result

class SellExplorationDataEventFormatter(EventFormatter):
    def process(self, event_summaries: iter) -> str:
        return f"{sum(map(lambda es: es.amount, event_summaries)):,} CR of Cartography Data\n"

class MarketSellEventFormatter(EventFormatter):
    def process(self, event_summaries: iter) -> str:
        total_sell_price = sum(map(lambda x: x.sell_price_per_unit * x.count, event_summaries))
        total_buy_price = sum(map(lambda x: x.average_buy_price_per_unit * x.count, event_summaries))
        total_count = sum(map(lambda x: x.count, event_summaries))
        return f"{total_count:,} T trade at {(total_sell_price - total_buy_price) / total_count:,.0f} CR average profit per T\n"

# TODO: Move to an IoC setup
_default_event_formatters:Dict[str, EventFormatter] = {
    "RedeemVoucherEventSummary" : RedeemVoucherEventFormatter(),
    "SellExplorationDataEventSummary" : SellExplorationDataEventFormatter(),
    "MarketSellEventSummary": SellExplorationDataEventFormatter()
}
