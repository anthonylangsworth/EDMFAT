from edmfs.event_summarizers import RedeemVoucherEventSummary

def test_redeem_voucher_event_summary_init():
    SYSTEM_NAME:str = "HR 1597"
    SUPPORTS:bool = True
    VOUCHER_TYPE:str = "bounty"
    AMOUNT:int = 512546
    redeem_voucher_event_summary:RedeemVoucherEventSummary = RedeemVoucherEventSummary(SYSTEM_NAME, SUPPORTS, VOUCHER_TYPE, AMOUNT)
    assert(redeem_voucher_event_summary.system_name == SYSTEM_NAME)
    assert(redeem_voucher_event_summary.supports == SUPPORTS)
    assert(redeem_voucher_event_summary.voucher_type == VOUCHER_TYPE)
    assert(redeem_voucher_event_summary.amount == AMOUNT)