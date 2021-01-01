import pytest

from edmfs.event_formatters import RedeemVoucherEventFormatter
from edmfs.event_summaries import RedeemVoucherEventSummary

@pytest.mark.parametrize(
        "event_summaries, expected_activity",
        []
    )
def test_default(event_summaries: list, expected_activity: str):
    pass