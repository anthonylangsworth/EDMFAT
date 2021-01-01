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
        for voucher_type, event_summaries_by_type in groupby(event_summaries, key=lambda x: x.voucher_type):
            result += voucher_type + "\n" + accumulate(map(lambda es: es.amount, event_summaries_by_type), operator.add)
        return result

# TODO: Move to an IoC setup
_default_event_formatters:Dict[str, EventFormatter] = {
    "RedeemVoucherEventSummary" : RedeemVoucherEventFormatter()
}