import pytest

from edmfs.event_formatters import RedeemVoucherEventFormatter, SellExplorationDataEventFormatter
from edmfs.event_summaries import RedeemVoucherEventSummary, SellExplorationDataEventSummary

@pytest.mark.parametrize(
    "event_summaries, expected_activity",
    [
        (
            [
                RedeemVoucherEventSummary("HR 1597", True, "bounty", 100),
                RedeemVoucherEventSummary("HR 1597", True, "bounty", 2000)
            ],
            "2,100 CR of Bounty Vouchers\n"
        ),
        (
            [
                RedeemVoucherEventSummary("HR 1597", True, "bounty", 100),
                #RedeemVoucherEventSummary("HR 1597", True, "scannable", 200),
                RedeemVoucherEventSummary("HR 1597", True, "CombatBond", 300)
            ],
            ("100 CR of Bounty Vouchers\n"
             #"200 CR of Cartography Data\n"
             "300 CR of Combat Bonds\n")
        )
    ]
)
def test_redeem_voucher_default(event_summaries: list, expected_activity: str):
    redeem_voucher_event_formatter = RedeemVoucherEventFormatter()
    assert(redeem_voucher_event_formatter.process(event_summaries) == expected_activity)

@pytest.mark.parametrize(
    "event_summaries, expected_activity",
    [
        (
            [
                SellExplorationDataEventSummary("Shambogi", True, 100),
                SellExplorationDataEventSummary("Shambogi", False, 2000)
            ],
            "2,100 CR of Cartography Data\n"
        )
    ]
)
def test_sell_exploration_data_default(event_summaries: list, expected_activity: str):
    sell_exploration_data_event_formatter = SellExplorationDataEventFormatter()
    assert(sell_exploration_data_event_formatter.process(event_summaries) == expected_activity)