import pytest
from typing import List

from edmfs.event_formatters import RedeemVoucherEventFormatter, SellExplorationDataEventFormatter, MarketBuyEventFormatter, \
    MarketSellEventFormatter, MissionCompletedEventFormatter, MissionFailedEventFormatter, MurderEventFormatter, SellOrganicDataEventFormatter
from edmfs.event_summaries import RedeemVoucherEventSummary, SellExplorationDataEventSummary, MarketBuyEventSummary, \
    MarketSellEventSummary, MissionCompletedEventSummary, MissionFailedEventSummary, MurderEventSummary, SellOrganicDataEventSummary


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
                MarketSellEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, 1000, 100, 50, 2),
            ],
            ["1 market sell(s). Total: 1,000 T and 50,000 CR profit. Average: 50 CR/T profit at bracket 2.0"]
        ),
        (
            [
                MarketSellEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, 1000, 100, 50, 3),
                MarketSellEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, 1000, 200, 100, 0)
            ],
            ["2 market sell(s). Total: 2,000 T and 150,000 CR profit. Average: 75 CR/T profit at bracket 1.5"]
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
                MarketBuyEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, 100, 500, 2),
                MarketBuyEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, 50, 500, 2),
                MarketBuyEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, 200, 100, 3)
            ],
            ["3 market buy(s). Total: 350 T and 95,000 CR. Average: 271 CR/T at bracket 2.3"]
        )
    ]
)
def test_market_buy(event_summaries: List[MarketSellEventFormatter], expected_activity: str):
    market_sell_event_formatter = MarketBuyEventFormatter()
    assert(market_sell_event_formatter.process(event_summaries) == expected_activity)


@pytest.mark.parametrize(
    "event_summaries, expected_activity",
    [
        (
            [
                MissionCompletedEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, "+")
            ],
            [
                "1 INF+ mission(s)",
                "1 total mission INF"
            ]
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
                "1 INF+++ mission(s)",
                "7 total mission INF"
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
    assert(MissionFailedEventFormatter().process(event_summaries) == expected_activity)


@pytest.mark.parametrize(
    "event_summaries, expected_activity",
    [
        (
            [
                MurderEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {})
            ],
            ["1 clean ship kill(s)"]
        ),
        (
            [
                MurderEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}),
                MurderEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}),
                MurderEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}),
            ],
            ["3 clean ship kill(s)"]
        )
    ]
)
def test_murder(event_summaries: List[MissionFailedEventSummary], expected_activity: str):
    assert(MurderEventFormatter().process(event_summaries) == expected_activity)


@pytest.mark.parametrize(
    "event_summaries, expected_activity",
    [
        (
            [
                SellOrganicDataEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, 1000)
            ],
            ["1,000 CR of Organic Data"]
        ),
        (
            [
                SellOrganicDataEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, 100),
                SellOrganicDataEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, 500),
                SellOrganicDataEventSummary("Shambogi", {"Shambogi Crimson Rats"}, {}, 67),
            ],
            ["667 CR of Organic Data"]
        )
    ]
)
def test_sell_organic_data(event_summaries: List[SellOrganicDataEventSummary], expected_activity: str):
    assert(SellOrganicDataEventFormatter().process(event_summaries) == expected_activity)
