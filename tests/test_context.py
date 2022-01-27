import pytest
from typing import Dict

from edmfs.context import Context

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
    market_entry = Context().get_last_market_entry(commodity_name, "tests/market_files/market.json")
    if expected_result:
        assert market_entry["Name_Localised"] == commodity_name
        for key in expected_result:
            assert market_entry[key] == expected_result[key]
    else:
        assert not market_entry