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
        for voucher_type, event_summaries_by_type in groupby(event_summaries, key=lambda x: x.voucher_type):
            result += f"{sum(map(lambda es: es.amount, event_summaries_by_type)):,} CR of {_voucher_type_lookup.get(voucher_type, voucher_type)}\n"
        return result

class SellExplorationDataEventFormatter(EventFormatter):
    def process(self, event_summaries: iter) -> str:
        return f"{sum(map(lambda es: es.amount, event_summaries)):,} CR of Cartography Data\n"

# TODO: Move to an IoC setup
_default_event_formatters:Dict[str, EventFormatter] = {
    "RedeemVoucherEventSummary" : RedeemVoucherEventFormatter(),
    "SellExplorationDataEventSummary" : SellExplorationDataEventFormatter()
}

_voucher_type_lookup:Dict[str, str] = {
    #"scannable" : "Scan Data",
    "bounty" : "Bounty Vouchers",
    "CombatBond" : "Combat Bonds"
}