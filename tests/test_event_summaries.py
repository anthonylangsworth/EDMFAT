from edmfs.event_summaries import RedeemVoucherEventSummary, SellExplorationDataEventSummary, MarketSellEventSummary, MissionCompletedEventSummary

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

def test_sell_exploration_data_event_summary_init():
    SYSTEM_NAME:str = "Shambogi"
    SUPPORTS:bool = True
    AMOUNT:int = 512546
    sell_exploration_data_event_summary:SellExplorationDataEventSummary = SellExplorationDataEventSummary(SYSTEM_NAME, SUPPORTS, AMOUNT)
    assert(sell_exploration_data_event_summary.system_name == SYSTEM_NAME)
    assert(sell_exploration_data_event_summary.supports == SUPPORTS)
    assert(sell_exploration_data_event_summary.amount == AMOUNT)

def test_market_sell_event_summary_init():
    SYSTEM_NAME:str = "Alpha Centauri"
    SUPPORTS:bool = True
    COUNT:int = 100
    SELL_PRICE_PER_UNIT:int = 10
    AVERAGE_BUY_PRICE_PER_UNIT:int = 5
    market_sell_event_summary:MarketSellEventSummary = MarketSellEventSummary(SYSTEM_NAME, SUPPORTS, COUNT, SELL_PRICE_PER_UNIT, AVERAGE_BUY_PRICE_PER_UNIT)
    assert(market_sell_event_summary.system_name == SYSTEM_NAME)
    assert(market_sell_event_summary.supports == SUPPORTS)
    assert(market_sell_event_summary.count == COUNT)
    assert(market_sell_event_summary.sell_price_per_unit == SELL_PRICE_PER_UNIT)
    assert(market_sell_event_summary.average_buy_price_per_unit == AVERAGE_BUY_PRICE_PER_UNIT)

def test_mission_completed_event_summary_init():
    SYSTEM_NAME = "Sol"
    SUPPORTS = True
    INFLUENCE = "++"
    mission_completed_event_summary = MissionCompletedEventSummary(SYSTEM_NAME, SUPPORTS, INFLUENCE)
    assert(mission_completed_event_summary.system_name == SYSTEM_NAME)
    assert(mission_completed_event_summary.supports == SUPPORTS)
    assert(mission_completed_event_summary.influence == INFLUENCE)
