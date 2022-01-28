import pytest
import logging
import functools
from typing import Callable, Dict, Tuple

from edmfat_web_services import resolve_star_system_via_edsm, split_tag, get_newer_release, get_last_market_entry
from edmfs.state import StarSystem
from edmfs.tracker import _get_dummy_logger

#@pytest.mark.skip(reason="Potentially long-running or external test")
@pytest.mark.parametrize(
    "system_address, expected_name",
    [
        (5070074488225, "Kamchaa"),
        (11666338948537, "Oluf"),
        (672028108201, "LHS 1832")
    ]
)
def test_resolve_star_system_via_edsm(system_address: int, expected_name: StarSystem) -> None:
    assert resolve_star_system_via_edsm(_get_dummy_logger(), system_address).name == expected_name

@pytest.mark.parametrize(
    "tag, expected_result",
    [
        ("v1.0", (1, 0)),
        ("v1.1.2", (1, 1, 2)),
        ("v0.15", (0, 15)),
        ("v9", (9,))
    ]
)
def test_split_tag(tag:str, expected_result:Tuple[int]):
    assert split_tag(tag) == expected_result

#@pytest.mark.skip(reason="Potentially long-running or external test")
def test_get_newer_release():
    assert get_newer_release(_get_dummy_logger(), "anthonylangsworth", "EDMFAT", (0, 14))


@pytest.mark.parametrize(
    "commodity_name, expected_result",
    [
        ("Platinum", {"BuyPrice":30908, "SellPrice":30906, "MeanPrice":58263, "StockBracket":0, "DemandBracket":0, "Stock":0}),
        ("Animal Meat", {"BuyPrice":0, "SellPrice":1864, "MeanPrice":1539, "StockBracket":0, "DemandBracket":3, "Stock":0}),
        ("Classified Experimental Equipment", {"BuyPrice":4002, "SellPrice":4001, "MeanPrice":11423, "StockBracket":0, "DemandBracket":0, "Stock":0}),
        ("Not A Commodity", None)
    ]
)
def test_get_last_market_entry(commodity_name:str, expected_result:Dict):
    market_entry = get_last_market_entry(commodity_name, "tests/market_files/market.json")
    if expected_result:
        assert market_entry["Name_Localised"] == commodity_name
        for key in expected_result:
            assert market_entry[key] == expected_result[key]
    else:
        assert not market_entry