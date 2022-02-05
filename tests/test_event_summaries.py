from edmfs.event_summaries import RedeemVoucherEventSummary, SellExplorationDataEventSummary, MarketSellEventSummary, MarketBuyEventSummary, MissionCompletedEventSummary, SellOrganicDataEventSummary


def test_redeem_voucher_event_summary_init():
    SYSTEM_NAME = "HR 1597"
    PRO = ("HR 1597 & Co",)
    ANTI = ()
    VOUCHER_TYPE = "bounty"
    AMOUNT = 512546
    redeem_voucher_event_summary = RedeemVoucherEventSummary(SYSTEM_NAME, PRO, ANTI, VOUCHER_TYPE, AMOUNT)
    assert(redeem_voucher_event_summary.system_name == SYSTEM_NAME)
    assert(redeem_voucher_event_summary.pro == PRO)
    assert(redeem_voucher_event_summary.anti == ANTI)
    assert(redeem_voucher_event_summary.voucher_type == VOUCHER_TYPE)
    assert(redeem_voucher_event_summary.amount == AMOUNT)


def test_sell_exploration_data_event_summary_init():
    SYSTEM_NAME = "Shambogi"
    PRO = ("Anti Energy Company",)
    ANTI = ()
    AMOUNT = 512546
    sell_exploration_data_event_summary: SellExplorationDataEventSummary = SellExplorationDataEventSummary(SYSTEM_NAME, PRO, ANTI, AMOUNT)
    assert(sell_exploration_data_event_summary.system_name == SYSTEM_NAME)
    assert(sell_exploration_data_event_summary.pro == PRO)
    assert(sell_exploration_data_event_summary.anti == ANTI)
    assert(sell_exploration_data_event_summary.amount == AMOUNT)


def test_market_sell_event_summary_init():
    SYSTEM_NAME = "Alpha Centauri"
    PRO = ("Hutton Orbital Truckers",)
    ANTI = ("The Dark Wheel",)
    COUNT = 100
    SELL_PRICE_PER_UNIT = 10
    AVERAGE_BUY_PRICE_PER_UNIT = 5
    DEMAND_BRACKET = 1.2
    market_sell_event_summary: MarketSellEventSummary = MarketSellEventSummary(SYSTEM_NAME, PRO, ANTI, COUNT, SELL_PRICE_PER_UNIT, AVERAGE_BUY_PRICE_PER_UNIT, DEMAND_BRACKET)
    assert(market_sell_event_summary.system_name == SYSTEM_NAME)
    assert(market_sell_event_summary.pro == PRO)
    assert(market_sell_event_summary.anti == ANTI)
    assert(market_sell_event_summary.count == COUNT)
    assert(market_sell_event_summary.sell_price_per_unit == SELL_PRICE_PER_UNIT)
    assert(market_sell_event_summary.average_buy_price_per_unit == AVERAGE_BUY_PRICE_PER_UNIT)
    assert(market_sell_event_summary.demand_bracket == DEMAND_BRACKET)


def test_market_buy_event_summary_init():
    SYSTEM_NAME = "Alpha Centauri"
    PRO = ("Hutton Orbital Truckers",)
    ANTI = ("The Dark Wheel",)
    COUNT = 100
    BUY_PRICE_PER_UNIT = 7
    SUPPLY_BRACKET = 2
    market_buy_event_summary = MarketBuyEventSummary(SYSTEM_NAME, PRO, ANTI, COUNT, BUY_PRICE_PER_UNIT, SUPPLY_BRACKET)
    assert(market_buy_event_summary.system_name == SYSTEM_NAME)
    assert(market_buy_event_summary.pro == PRO)
    assert(market_buy_event_summary.anti == ANTI)
    assert(market_buy_event_summary.count == COUNT)
    assert(market_buy_event_summary.buy_price_per_unit == BUY_PRICE_PER_UNIT)
    assert(market_buy_event_summary.supply_bracket == SUPPLY_BRACKET)


def test_mission_completed_event_summary_init():
    SYSTEM_NAME = "Sol"
    PRO = ("Mother Gaia",)
    ANTI = ()
    INFLUENCE = "++"
    mission_completed_event_summary = MissionCompletedEventSummary(SYSTEM_NAME, PRO, ANTI, INFLUENCE)
    assert(mission_completed_event_summary.system_name == SYSTEM_NAME)
    assert(mission_completed_event_summary.pro == PRO)
    assert(mission_completed_event_summary.anti == ANTI)
    assert(mission_completed_event_summary.influence == INFLUENCE)


def test_sell_organic_data_event_summary_init():
    SYSTEM_NAME = "Sol"
    PRO = ("Mother Gaia",)
    ANTI = ()
    VALUE = 1234
    mission_completed_event_summary = SellOrganicDataEventSummary(SYSTEM_NAME, PRO, ANTI, VALUE)
    assert(mission_completed_event_summary.system_name == SYSTEM_NAME)
    assert(mission_completed_event_summary.pro == PRO)
    assert(mission_completed_event_summary.anti == ANTI)
    assert(mission_completed_event_summary.value == VALUE)
