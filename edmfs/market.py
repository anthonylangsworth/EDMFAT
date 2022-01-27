from typing import Dict
import json


def get_market_entry(commodity_name: str, market_json_file_path:str = None) -> Dict:
    '''Return a Dict containg the market.json line for commodity_name or None, if no line matches'''
    file_path = "%%userprofile%%\\Saved Games\\Frontier Developments\\Elite Dangerous\\market.json" if market_json_file_path == None else market_json_file_path
    with open(file_path, mode="r") as market_json_file:
        market = json.load(market_json_file)
    for market_entry in market["Items"]:
        if market_entry["Name_Localised"] == commodity_name:
            return market_entry            
    return None
