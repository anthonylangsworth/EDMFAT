import pytest
from typing import List

from edmfs.event_formatters import RedeemVoucherEventFormatter, SellExplorationDataEventFormatter, MarketSellEventFormatter, MissionCompletedEventFormatter, MissionFailedEventFormatter
from edmfs.event_summaries import RedeemVoucherEventSummary, SellExplorationDataEventSummary, MarketSellEventSummary, MissionCompletedEventSummary, MissionFailedEventSummary

@pytest.mark.parametrize(
    "event_summaries, expected_activity",
    [
        (
            [
                RedeemVoucherEventSummary("HR 1597", {"HR 1597 & Co"}, {}, "bounty", 100),
                RedeemVoucherEventSummary("HR 1597", {"HR 1597 & Co"}, {}, "bounty", 2000)
            ],
            ["2,100 CR of Bounty Vouchers"]
        ),
        (
            [
                RedeemVoucherEventSummary("HR 1597", {"HR 1597 & Co"}, {}, "bounty", 100),
                RedeemVoucherEventSummary("HR 1597", {"HR 1597 & Co"}, {}, "CombatBond", 300)
            ],
            [
                "100 CR of Bounty Vouchers",
                "300 CR of Combat Bonds"
            ]
        )
    ]
)
def test_redeem_voucher(event_summaries: List[RedeemVoucherEventSummary], expected_activity: str):
    redeem_voucher_event_formatter = RedeemVoucherEventFormatter()
    assert(redeem_voucher_event_formatter.process(event_summaries) == expected_activity)

@pytest.mark.parametrize(
    "event_summaries, expected_activity",
    [
        (
            [
                SellExplorationDataEventSummary("Shambogi", {"Antai Energy Company"}, {}, 100),
                SellExplorationDataEventSummary("Shambogi", {"Antai Energy Company"}, {}, 2000)
            ],
            ["2,100 CR of Cartography Data"]
        )
    ]
)
def test_sell_exploration_data(event_summaries: List[SellExplorationDataEventSummary], expected_activity: str):
    sell_exploration_data_event_formatter = SellExplorationDataEventFormatter()
    assert(sell_exploration_data_event_formatter.process(event_summaries) == expected_activity)

@pytest.mark.parametrize(
    "event_summaries, expected_activity",
    [
        (
            [
                MarketSellEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, 1000, 100, 50),
                MarketSellEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, 1000, 200, 100)
            ],
            ["2,000 T trade at 75 CR average profit per T"]
        )
    ]
)
def test_market_sell(event_summaries: List[MarketSellEventFormatter], expected_activity: str):
    market_sell_event_formatter = MarketSellEventFormatter()
    assert(market_sell_event_formatter.process(event_summaries) == expected_activity)

@pytest.mark.parametrize(
    "event_summaries, expected_activity",
    [
        (
            [
                MissionCompletedEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, "+")
            ],
            ["1 INF+ mission(s)"]
        ),        
        (
            [
                MissionCompletedEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, "+"),
                MissionCompletedEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, "+"),
                MissionCompletedEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, "++"),
                MissionCompletedEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, "+++")
            ],
            [
                "2 INF+ mission(s)",
                "1 INF++ mission(s)",
                "1 INF+++ mission(s)"
            ]
        )
    ]
)
def test_mission_completed(event_summaries: List[MissionCompletedEventSummary], expected_activity: str):
    mission_completed_event_formatter = MissionCompletedEventFormatter()
    assert(mission_completed_event_formatter.process(event_summaries) == expected_activity)


@pytest.mark.parametrize(
    "event_summaries, expected_activity",
    [
        (
            [
                MissionFailedEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {})
            ],
            ["1 failed mission(s)"]
        ),        
        (
            [
                MissionFailedEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}),
                MissionFailedEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}),
                MissionFailedEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}),
                MissionFailedEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {})
            ],
            ["4 failed mission(s)"]
        )
    ]
)
def test_mission_failed(event_summaries: List[MissionFailedEventSummary], expected_activity: str):
    mission_completed_event_formatter = MissionFailedEventFormatter()
    assert(mission_completed_event_formatter.process(event_summaries) == expected_activity)