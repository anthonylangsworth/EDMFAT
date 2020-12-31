class EventSummary():
    def __init__(self, system_name:str, supports:bool):
        self._system_name:str = system_name
        self._supports:str = supports

    @property
    def system_name(self) -> str:
        return self._system_name

    @property
    def supports(self) -> bool:
        return self._supports

    def __eq__(self, other):
        if not isinstance(other, EventSummary):
            return NotImplemented

        return self._system_name == other._system_name \
            and self._supports == other._supports

class RedeemVoucherEventSummary(EventSummary):
    def __init__(self, system_name:str, supports:bool, voucher_type:str, amount:int):
        super(RedeemVoucherEventSummary, self).__init__(system_name, supports)
        self._voucher_type:str = voucher_type
        self._amount:int = amount
    
    @property
    def voucher_type(self) -> str:
        return self._voucher_type

    @property
    def amount(self) -> int:
        return self._amount

    def __eq__(self, other):
        if not isinstance(other, RedeemVoucherEventSummary):
            return NotImplemented

        return super(RedeemVoucherEventSummary, self).__eq__(other) \
            and self._system_name == other._system_name \
            and self._supports == other._supports        