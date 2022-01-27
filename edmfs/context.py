from typing import Dict
import json

class Context:
    def get_last_market_entry(self, commodity_name: str, market_json_file_path:str = None) -> Dict:
        '''Return a Dict containg the market.json line for commodity_name or None, if no line matches'''
        file_path = "%%userprofile%%\\Saved Games\\Frontier Developments\\Elite Dangerous\\market.json" if market_json_file_path == None else market_json_file_path
        with open(file_path, mode="r") as market_json_file:
            market = json.load(market_json_file)
        return next(filter(lambda market_entry: market_entry["Name_Localised"] == commodity_name, market["Items"]), None)
