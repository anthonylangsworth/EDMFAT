from functools import cache
import pytest
import json
from typing import Callable, Dict

from edmfs.tracker import Tracker,_get_dummy_logger
from edmfs.serializers import TrackerFileRepository
from edmfs.state import StarSystem


def load_test_market():
    return { 
        "Consumer Technology": { "id":128049240, "Name":"$consumertechnology_name;", "Name_Localised":"Consumer Technology", "Category":"$MARKET_category_consumer_items;", "Category_Localised":"Consumer items", "BuyPrice":0, "SellPrice":7186, "MeanPrice":6690, "StockBracket":0, "DemandBracket":2, "Stock":0, "Demand":18, "Consumer":True, "Producer":False, "Rare":False },
        "Coltan": { "id":128049159, "Name":"$coltan_name;", "Name_Localised":"Coltan", "Category":"$MARKET_category_minerals;", "Category_Localised":"Minerals", "BuyPrice":5051, "SellPrice":4846, "MeanPrice":6163, "StockBracket":3, "DemandBracket":0, "Stock":277, "Demand":1, "Consumer":False, "Producer":True, "Rare":False },
        "Copper": { "id":128049175, "Name":"$copper_name;", "Name_Localised":"Copper", "Category":"$MARKET_category_metals;", "Category_Localised":"Metals", "BuyPrice":246, "SellPrice":245, "MeanPrice":689, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False },
        "Indium": { "id":128049169, "Name":"$indium_name;", "Name_Localised":"Indium", "Category":"$MARKET_category_metals;", "Category_Localised":"Metals", "BuyPrice":3949, "SellPrice":3948, "MeanPrice":5845, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False },
        "Uranium": { "id":128049172, "Name":"$uranium_name;", "Name_Localised":"Uranium", "Category":"$MARKET_category_metals;", "Category_Localised":"Metals", "BuyPrice":1697, "SellPrice":1696, "MeanPrice":2827, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False },
        "Reactive Armour": { "id":128049235, "Name":"$reactivearmour_name;", "Name_Localised":"Reactive Armour", "Category":"$MARKET_category_weapons;", "Category_Localised":"Weapons", "BuyPrice":0, "SellPrice":2649, "MeanPrice":2224, "StockBracket":0, "DemandBracket":3, "Stock":0, "Demand":46, "Consumer":True, "Producer":False, "Rare":False },
        "Tantalum": { "id":128049171, "Name":"$tantalum_name;", "Name_Localised":"Tantalum", "Category":"$MARKET_category_metals;", "Category_Localised":"Metals", "BuyPrice":2567, "SellPrice":2566, "MeanPrice":4044, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False },
        "Atmospheric Processors": { "id":128064028, "Name":"$atmosphericextractors_name;", "Name_Localised":"Atmospheric Processors", "Category":"$MARKET_category_machinery;", "Category_Localised":"Machinery", "BuyPrice":205, "SellPrice":204, "MeanPrice":571, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False },
        "Tritium": { "id":128961249, "Name":"$tritium_name;", "Name_Localised":"Tritium", "Category":"$MARKET_category_chemicals;", "Category_Localised":"Chemicals", "BuyPrice":39541, "SellPrice":39539, "MeanPrice":51707, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False },
        "Platinum Alloy": { "id":128049152, "Name":"$platinumalloy_name;", "Name_Localised":"Platinum Alloy", "Category":"$MARKET_category_metals;", "Category_Localised":"Metals", "BuyPrice":30908, "SellPrice":30906, "MeanPrice":58263, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":True },
        "Eden Apples Of Aerial": { "id":128049152, "Name":"$edenapplesofaerial_name;", "Name_Localised":"Eden Apples of Aerial", "Category":"$MARKET_category_metals;", "Category_Localised":"Metals", "BuyPrice":30908, "SellPrice":30906, "MeanPrice":58263, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":True },
        "Tea": { "id":128049188, "Name":"$tea_name;", "Name_Localised":"Tea", "Category":"$MARKET_category_foods;", "Category_Localised":"Foods", "BuyPrice":0, "SellPrice":2053, "MeanPrice":1696, "StockBracket":0, "DemandBracket":3, "Stock":0, "Demand":53, "Consumer":True, "Producer":False, "Rare":False },
        "Survival Equipment": { "id":128682048, "Name":"$survivalequipment_name;", "Name_Localised":"Survival Equipment", "Category":"$MARKET_category_consumer_items;", "Category_Localised":"Consumer items", "BuyPrice":283, "SellPrice":282, "MeanPrice":684, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False },
        "Superconductors": { "id":128049200, "Name":"$superconductors_name;", "Name_Localised":"Superconductors", "Category":"$MARKET_category_industrial_materials;", "Category_Localised":"Industrial materials", "BuyPrice":4508, "SellPrice":4507, "MeanPrice":6679, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False },
        "Onionhead": { "id":128049200, "Name":"$onionhead_name;", "Name_Localised":"Onionhead", "Category":"$MARKET_category_industrial_materials;", "Category_Localised":"Industrial materials", "BuyPrice":4508, "SellPrice":4507, "MeanPrice":6679, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":True }
    }


@pytest.mark.parametrize(
    "minor_factions, journal_file_name, load_last_market",
    [
        ({"HR 1597 & Co"}, "Journal.201019220908.01.log", load_test_market),
        ({"EDA Kunti League"}, "Journal.200913212207.01.log", load_test_market),
        ({"EDA Kunti League"}, "Journal.201018213100.01.log", load_test_market),
        ({"EDA Kunti League"}, "Journal.210101234033.01.log", load_test_market),
        ({"EDA Kunti League"}, "Journal.201212203015.01.log", load_test_market),
        ({"Green Party of Dulos"}, "Journal.200630212114.01.log", load_test_market),
        ({"EDA Kunti League"}, "Journal.210102190919.01.log", load_test_market),
        ({"EDA Kunti League"}, "Journal.210105181410.01.log", load_test_market),
        ({"EDA Kunti League"}, "Journal.210105214916.01.log", load_test_market),
        ({"EDA Kunti League", "LHS 1832 Labour"}, "Journal.210105214916.01.log", load_test_market),
        ({"LHS 1832 Labour", "EDA Kunti League"}, "Journal.210105214916.01.log", load_test_market),
        ({"EDA Kunti League"}, "LesPaul58_Journal.210117142551.01.log", load_test_market),
        ({"EDA Kunti League"}, "Journal.210122183958.01.log", load_test_market),
        ({"EDA Kunti League"}, "Journal.210125173739.01.log", load_test_market),
        ({"EDA Kunti League"}, "Journal.210125115425.01.log", load_test_market),
        ({"Yuri Grom"}, "Journal.210120211308.01.log", load_test_market),
        ({"Atfero Blue General & Co"}, "Journal.200509115806.01.log", load_test_market),
        ({"EDA Kunti League"}, "Journal.210221171753.01.log", load_test_market)
    ]
)
def test_serialize_tracker(minor_factions:str, journal_file_name:str, load_last_market: Callable[[], Dict]):
    tracker = Tracker(minor_factions = minor_factions, load_last_market = load_last_market)
    with open("tests/journal_files/" + journal_file_name) as journal_file:
        for line in journal_file.readlines():
            tracker.on_event(json.loads(line))

    logger = _get_dummy_logger()
    resolver = lambda x: StarSystem("a", 122, [])

    repository = TrackerFileRepository()
    serialized_tracker = repository.serialize(tracker)
    new_tracker = repository.deserialize(serialized_tracker, logger, resolver)

    assert tracker.minor_factions == new_tracker.minor_factions
    assert tracker.pilot_state.missions == new_tracker.pilot_state.missions
    assert tracker._event_summaries == new_tracker._event_summaries
    assert len(new_tracker.galaxy_state.systems) == 0
    assert tracker.activity == new_tracker.activity

    assert new_tracker.pilot_state.system_address == None
    assert new_tracker.pilot_state.last_docked_station == None

    assert new_tracker._logger == logger
    assert new_tracker.galaxy_state.systems.resolver == resolver
