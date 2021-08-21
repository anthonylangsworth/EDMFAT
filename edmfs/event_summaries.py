from typing import Iterable


class EventSummary():
    def __init__(self, system_name: str, pro: Iterable, anti: Iterable):
        self._system_name = system_name
        self._pro = set(pro)
        self._anti = set(anti)

    @property
    def system_name(self) -> str:
        return self._system_name

    @property
    def pro(self) -> tuple:
        return tuple(self._pro)

    @property
    def anti(self) -> tuple:
        return tuple(self._anti)

    def __eq__(self, other):
        if not isinstance(other, EventSummary):
            return NotImplemented

        return (self._system_name == other._system_name
            and self._pro == other._pro
            and self._anti == other._anti)


class RedeemVoucherEventSummary(EventSummary):
    def __init__(self, system_name:str, pro: iter, anti: iter, voucher_type: str, amount: int):
        super(RedeemVoucherEventSummary, self).__init__(system_name, pro, anti)
        self._voucher_type:str = voucher_type
        self._amount:int = amount
    
    @property
    def voucher_type(self) -> str:
        return self._voucher_type

    @property
    def amount(self) -> int:
        return self._amount

    def __eq__(self, other) -> bool:
        if not isinstance(other, RedeemVoucherEventSummary):
            return NotImplemented

        return super(RedeemVoucherEventSummary, self).__eq__(other) \
            and self._voucher_type == other._voucher_type \
            and self._amount == other._amount        

    def __repr__(self) -> str:
        return f"RedeemVoucherEventSummary('{self._system_name}', '{self._pro}', {self._anti}, '{self._voucher_type}', {self._amount})" 


class SellExplorationDataEventSummary(EventSummary):
    def __init__(self, system_name:str, pro: iter, anti: iter, amount: int):
        super(SellExplorationDataEventSummary, self).__init__(system_name, pro, anti)
        self._amount:int = amount
    
    @property
    def amount(self) -> int:
        return self._amount

    def __eq__(self, other) -> bool:
        if not isinstance(other, SellExplorationDataEventSummary):
            return NotImplemented

        return super(SellExplorationDataEventSummary, self).__eq__(other) \
            and self._amount == other._amount        

    def __repr__(self) -> str:
        return f"SellExplorationDataEventSummary('{self._system_name}', '{self._pro}', {self._anti}, {self._amount})" 


class MarketSellEventSummary(EventSummary):
    def __init__(self, system_name:str, pro: iter, anti: iter, count: int, sell_price_per_unit: int, average_buy_price_per_unit: int):
        super(MarketSellEventSummary, self).__init__(system_name, pro, anti)
        self._count:int = count
        self._sell_price_per_unit:int = sell_price_per_unit
        self._average_buy_price_per_unit:int = average_buy_price_per_unit
    
    @property
    def count(self) -> int:
        return self._count

    @property
    def sell_price_per_unit(self) -> int:
        return self._sell_price_per_unit

    @property
    def average_buy_price_per_unit(self) -> int:
        return self._average_buy_price_per_unit

    def __eq__(self, other) -> bool:
        if not isinstance(other, MarketSellEventSummary):
            return NotImplemented

        return (super(MarketSellEventSummary, self).__eq__(other)
            and self._count == other._count
            and self._sell_price_per_unit == other._sell_price_per_unit
            and self._average_buy_price_per_unit == other._average_buy_price_per_unit)

    def __repr__(self) -> str:
        return f"MarketSellEventSummary('{self._system_name}', '{self._pro}', {self._anti}, {self._count}, {self._sell_price_per_unit}, {self._average_buy_price_per_unit})" 


class MissionCompletedEventSummary(EventSummary):
    def __init__(self, system_name:str, pro: iter, anti: iter, influence: str):
        super(MissionCompletedEventSummary, self).__init__(system_name, pro, anti)
        self._influence:str = influence

    @property
    def influence(self) -> str:
        return self._influence

    def __eq__(self, other) -> bool:
        if not isinstance(other, MissionCompletedEventSummary):
            return NotImplemented

        return (super(MissionCompletedEventSummary, self).__eq__(other)
            and self._influence == other._influence)

    def __repr__(self) -> str:
        return f"MissionCompletedEventSummary('{self._system_name}', '{self._pro}', {self._anti}, '{self._influence}')" 


class MissionFailedEventSummary(EventSummary):
    def __init__(self, system_name:str, pro: iter, anti: iter):
        super().__init__(system_name, pro, anti)

    def __eq__(self, other) -> bool:
        return isinstance(other, MissionFailedEventSummary)

    def __repr__(self) -> str:
        return f"MissionFailedEventSummary('{self._system_name}', '{self._pro}', '{self._anti}')" 


class MurderEventSummary(EventSummary):
    def __init__(self, system_name:str, pro: iter, anti: iter):
        super().__init__(system_name, pro, anti)

    def __eq__(self, other) -> bool:
        return isinstance(other, MurderEventSummary)

    def __repr__(self) -> str:
        return f"MurderEventSummary('{self._system_name}', '{self._pro}', '{self._anti}')" 


class SellOrganicDataEventSummary(EventSummary):
    def __init__(self, system_name:str, pro: iter, anti: iter, value: int):
        super().__init__(system_name, pro, anti)
        self._value: int = value

    @property
    def value(self) -> int:
        return self._value

    def __eq__(self, other) -> bool:
        if not isinstance(other, SellOrganicDataEventSummary):
            return NotImplemented

        return (super(SellOrganicDataEventSummary, self).__eq__(other)
            and self._value == other._value)

    def __repr__(self) -> str:
        return f"SellOrganicDataEventSummary('{self._system_name}', '{self._pro}', '{self._anti}', {self._value})" 


_default_event_summary_order = (
    "MissionCompletedEventSummary",
    "RedeemVoucherEventSummary",
    "SellExplorationDataEventSummary",
    "MarketSellEventSummary",
    "MissionFailedEventSummary",
    "MurderEventSummary",
    "SellOrganicDataEventSummary"
)