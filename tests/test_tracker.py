import pytest
import json
from typing import Callable, Dict, List

from edmfs.state import PilotState, GalaxyState, Station
from edmfs.tracker import Tracker

def test_tracker_init():
    MINOR_FACTIONS = ("EDA Kunti League",)
    tracker = Tracker(MINOR_FACTIONS)
    assert(tracker.minor_factions == MINOR_FACTIONS)
    assert(tracker.pilot_state == PilotState())
    assert(tracker.galaxy_state == GalaxyState())
    assert(tracker.activity == "")

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
        "Hydrogen Fuel": { "id":128049202, "Name":"$hydrogenfuel_name;", "Name_Localised":"Hydrogen Fuel", "Category":"$MARKET_category_chemicals;", "Category_Localised":"Chemicals", "BuyPrice":84, "SellPrice":80, "MeanPrice":113, "StockBracket":3, "DemandBracket":0, "Stock":1103, "Demand":1, "Consumer":False, "Producer":True, "Rare":False },
        "Tea": { "id":128049188, "Name":"$tea_name;", "Name_Localised":"Tea", "Category":"$MARKET_category_foods;", "Category_Localised":"Foods", "BuyPrice":0, "SellPrice":2053, "MeanPrice":1696, "StockBracket":0, "DemandBracket":3, "Stock":0, "Demand":53, "Consumer":True, "Producer":False, "Rare":False },
        "Survival Equipment": { "id":128682048, "Name":"$survivalequipment_name;", "Name_Localised":"Survival Equipment", "Category":"$MARKET_category_consumer_items;", "Category_Localised":"Consumer items", "BuyPrice":283, "SellPrice":282, "MeanPrice":684, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False },
        "Superconductors": { "id":128049200, "Name":"$superconductors_name;", "Name_Localised":"Superconductors", "Category":"$MARKET_category_industrial_materials;", "Category_Localised":"Industrial materials", "BuyPrice":4508, "SellPrice":4507, "MeanPrice":6679, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False },
        "Onionhead": { "id":128049200, "Name":"$onionhead_name;", "Name_Localised":"Onionhead", "Category":"$MARKET_category_industrial_materials;", "Category_Localised":"Industrial materials", "BuyPrice":4508, "SellPrice":4507, "MeanPrice":6679, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":True },
        "Moissanite": { "id":128672296, "Name":"$moissanite_name;", "Name_Localised":"Moissanite", "Category":"$MARKET_category_minerals;", "Category_Localised":"Minerals", "BuyPrice":15255, "SellPrice":15254, "MeanPrice":24833, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False }, 
        "Taaffeite": { "id":128672775, "Name":"$taaffeite_name;", "Name_Localised":"Taaffeite", "Category":"$MARKET_category_minerals;", "Category_Localised":"Minerals", "BuyPrice":36027, "SellPrice":36025, "MeanPrice":52089, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False }, 
        "Power Generators": { "id":128049217, "Name":"$powergenerators_name;", "Name_Localised":"Power Generators", "Category":"$MARKET_category_machinery;", "Category_Localised":"Machinery", "BuyPrice":0, "SellPrice":2728, "MeanPrice":2466, "StockBracket":0, "DemandBracket":2, "Stock":0, "Demand":30, "Consumer":True, "Producer":False, "Rare":False },
        "Pesticides": { "id":128049205, "Name":"$pesticides_name;", "Name_Localised":"Pesticides", "Category":"$MARKET_category_chemicals;", "Category_Localised":"Chemicals", "BuyPrice":91, "SellPrice":90, "MeanPrice":437, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False },
        "Grain": { "id":128049180, "Name":"$grain_name;", "Name_Localised":"Grain", "Category":"$MARKET_category_foods;", "Category_Localised":"Foods", "BuyPrice":0, "SellPrice":810, "MeanPrice":410, "StockBracket":0, "DemandBracket":3, "Stock":0, "Demand":569, "Consumer":True, "Producer":False, "Rare":False },
        "Pavonis Ear Grubs" : { "id":128666747, "Name":"$pavoniseargrubs_name;", "Name_Localised":"Pavonis Ear Grubs", "Category":"$MARKET_category_drugs;", "Category_Localised":"Legal drugs", "BuyPrice":2802, "SellPrice":2801, "MeanPrice":10365, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":True },
        "Crop Harvesters": { "id":128049222, "Name":"$cropharvesters_name;", "Name_Localised":"Crop Harvesters", "Category":"$MARKET_category_machinery;", "Category_Localised":"Machinery", "BuyPrice":1365, "SellPrice":1364, "MeanPrice":2230, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False },
        "Clothing": { "id":128049241, "Name":"$clothing_name;", "Name_Localised":"Clothing", "Category":"$MARKET_category_consumer_items;", "Category_Localised":"Consumer items", "BuyPrice":0, "SellPrice":642, "MeanPrice":546, "StockBracket":0, "DemandBracket":2, "Stock":0, "Demand":229, "Consumer":True, "Producer":False, "Rare":False },
        "Food Cartridges": { "id":128049184, "Name":"$foodcartridges_name;", "Name_Localised":"Food Cartridges", "Category":"$MARKET_category_foods;", "Category_Localised":"Foods", "BuyPrice":0, "SellPrice":436, "MeanPrice":265, "StockBracket":0, "DemandBracket":2, "Stock":0, "Demand":83, "Consumer":True, "Producer":False, "Rare":False }, 
        "Polymers": { "id":128049197, "Name":"$polymers_name;", "Name_Localised":"Polymers", "Category":"$MARKET_category_industrial_materials;", "Category_Localised":"Industrial materials", "BuyPrice":41, "SellPrice":40, "MeanPrice":376, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False },
        "Scrap": { "id":128049248, "Name":"$scrap_name;", "Name_Localised":"Scrap", "Category":"$MARKET_category_waste;", "Category_Localised":"Waste", "BuyPrice":59, "SellPrice":58, "MeanPrice":300, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False }, 
        "Non-Lethal Weapons": { "id":128049236, "Name":"$nonlethalweapons_name;", "Name_Localised":"Non-Lethal Weapons", "Category":"$MARKET_category_weapons;", "Category_Localised":"Weapons", "BuyPrice":0, "SellPrice":2176, "MeanPrice":1943, "StockBracket":0, "DemandBracket":2, "Stock":0, "Demand":31, "Consumer":True, "Producer":False, "Rare":False }, 
        "Beryllium": { "id":128049168, "Name":"$beryllium_name;", "Name_Localised":"Beryllium", "Category":"$MARKET_category_metals;", "Category_Localised":"Metals", "BuyPrice":5631, "SellPrice":5630, "MeanPrice":8243, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False }, 
        "Gold": { "id":128049154, "Name":"$gold_name;", "Name_Localised":"Gold", "Category":"$MARKET_category_metals;", "Category_Localised":"Metals", "BuyPrice":44266, "SellPrice":43761, "MeanPrice":47610, "StockBracket":3, "DemandBracket":0, "Stock":80, "Demand":1, "Consumer":False, "Producer":True, "Rare":False }, 
        "Palladium": { "id":128049153, "Name":"$palladium_name;", "Name_Localised":"Palladium", "Category":"$MARKET_category_metals;", "Category_Localised":"Metals", "BuyPrice":47403, "SellPrice":46818, "MeanPrice":50639, "StockBracket":3, "DemandBracket":0, "Stock":12, "Demand":1, "Consumer":False, "Producer":True, "Rare":False },
        "Bertrandite": { "id":128049156, "Name":"$bertrandite_name;", "Name_Localised":"Bertrandite", "Category":"$MARKET_category_minerals;", "Category_Localised":"Minerals", "BuyPrice":16442, "SellPrice":16025, "MeanPrice":18817, "StockBracket":3, "DemandBracket":0, "Stock":175, "Demand":1, "Consumer":False, "Producer":True, "Rare":False }, 
        "Water": { "id":128049166, "Name":"$water_name;", "Name_Localised":"Water", "Category":"$MARKET_category_chemicals;", "Category_Localised":"Chemicals", "BuyPrice":0, "SellPrice":423, "MeanPrice":278, "StockBracket":0, "DemandBracket":2, "Stock":0, "Demand":39, "Consumer":True, "Producer":False, "Rare":False }, 
        "Biowaste": { "id":128049244, "Name":"$biowaste_name;", "Name_Localised":"Biowaste", "Category":"$MARKET_category_waste;", "Category_Localised":"Waste", "BuyPrice":62, "SellPrice":38, "MeanPrice":358, "StockBracket":3, "DemandBracket":0, "Stock":130, "Demand":1, "Consumer":False, "Producer":True, "Rare":False },
        "Algae": { "id":128049177, "Name":"$algae_name;", "Name_Localised":"Algae", "Category":"$MARKET_category_foods;", "Category_Localised":"Foods", "BuyPrice":27, "SellPrice":26, "MeanPrice":356, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False }, 
    }    

@pytest.mark.parametrize(
    "minor_factions, journal_file_name, load_last_market, expected_activity",
    [
        (
            {"HR 1597 & Co"}, 
            "Journal.201019220908.01.log", 
            load_test_market,
            ("HR 1597 - ANTI HR 1597 & Co\n"
            "1,916,227 CR of Bounty Vouchers\n"
            "\n"
            "HR 1597 - PRO HR 1597 & Co\n"
            "1 INF++ mission(s)\n"
            "2 INF+++ mission(s)\n"            
            "12,801,574 CR of Bounty Vouchers")
        ),
        (
            {"EDA Kunti League"}, 
            "Journal.200913212207.01.log", 
            load_test_market,
            ("Kunti - ANTI EDA Kunti League\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "Shambogi - ANTI EDA Kunti League\n"
            "965,956 CR of Bounty Vouchers\n"
            "\n"
            "Shambogi - PRO EDA Kunti League\n"
            "7 INF++ mission(s)\n"
            "1 INF+++ mission(s)\n"
            "139,652 CR of Bounty Vouchers")
        ),
        (
            {"EDA Kunti League"}, 
            "Journal.201018213100.01.log",
            load_test_market,
            ("9 G. Carinae - ANTI EDA Kunti League\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "Kanates - PRO EDA Kunti League\n"
            "3 INF+++ mission(s)\n"
            "1 INF++++ mission(s)\n"
            "436,046 CR of Bounty Vouchers\n"
            "61,635 CR of Cartography Data\n"
            "\n"
            "Kutjara - ANTI EDA Kunti League\n"
            "1 INF++++ mission(s)")
        ),
        (
            {"EDA Kunti League"}, 
            "Journal.210101234033.01.log",
            load_test_market,
            ("HR 1597 - PRO EDA Kunti League\n"
            "559,467 CR of Combat Bonds\n"
            "\n"
            "LTT 2337 - PRO EDA Kunti League\n"
            "718,360 CR of Bounty Vouchers\n"
            "141,361 CR of Cartography Data\n"
            "\n"
            "Shambogi - PRO EDA Kunti League\n"
            "50,765 CR of Cartography Data")
        ),
        (
            {"EDA Kunti League"}, 
            "Journal.201212203015.01.log",
            load_test_market,
            ("Antai - PRO EDA Kunti League\n"
            "2,840 T trade at 2,506 CR average profit per T")
        ),
        (
            {"Green Party of Dulos"}, 
            "Journal.200630212114.01.log",
            load_test_market,
            ("Dulos - ANTI Green Party of Dulos\n"
            "28 T trade at 44 CR average profit per T\n"
            "\n"
            "Dulos - PRO Green Party of Dulos\n"
            "1 INF+++ mission(s)")
        ),
        (
            {"EDA Kunti League"}, 
            "Journal.210102190919.01.log",
            load_test_market,
            ("Groanomana - PRO EDA Kunti League\n"
             "18,704,140 CR of Bounty Vouchers\n"
             "\n"
             "HR 1597 - PRO EDA Kunti League\n"
             "7,622,618 CR of Bounty Vouchers")
        ),
        (
            {"EDA Kunti League"}, 
            "Journal.210105181410.01.log",
            load_test_market,
            ("Anek Wango - ANTI EDA Kunti League\n"
            "1 INF+ mission(s)\n"
            "1 INF++ mission(s)\n"
            "\n"
            "LHS 1832 - ANTI EDA Kunti League\n"
            "1 INF+ mission(s)\n"
            "1 INF++ mission(s)\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "LHS 1832 - PRO EDA Kunti League\n"
            "1 INF++ mission(s)\n"
            "194,136 CR of Bounty Vouchers\n"
            "12,039 CR of Cartography Data\n"
            "\n"
            "LPM 229 - ANTI EDA Kunti League\n"
            "1 INF+ mission(s)\n"
            "2 INF++ mission(s)\n"
            "\n"
            "LTT 2337 - ANTI EDA Kunti League\n"
            "2 INF+ mission(s)\n"
            "1 INF++ mission(s)\n"
            "6 T trade at -198 CR average profit per T\n"
            "\n"
            "LTT 2337 - PRO EDA Kunti League\n"
            "5 T trade at 265 CR average profit per T")
        ),
        (
            {"EDA Kunti League"}, 
            "Journal.210105214916.01.log",
            load_test_market,
            ("LHS 1832 - ANTI EDA Kunti League\n"
            "1 INF+ mission(s)\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "Shongbon - ANTI EDA Kunti League\n"
            "1 INF+++ mission(s)")
        ),
        (
            {
                "EDA Kunti League",
                "LHS 1832 Labour"
            }, 
            "Journal.210105214916.01.log",
            load_test_market,
            ("LHS 1832 - ANTI EDA Kunti League\n"
            "1 INF+ mission(s)\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "Shongbon - ANTI EDA Kunti League\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "LHS 1832 - ANTI LHS 1832 Labour\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "LHS 1832 - PRO LHS 1832 Labour\n"
            "1 INF+ mission(s)")
        ),
        (
            [
                "LHS 1832 Labour",
                "EDA Kunti League"
            ], 
            "Journal.210105214916.01.log",
            load_test_market,
            ("LHS 1832 - ANTI EDA Kunti League\n"
            "1 INF+ mission(s)\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "Shongbon - ANTI EDA Kunti League\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "LHS 1832 - ANTI LHS 1832 Labour\n"
            "1 INF+++ mission(s)\n"
            "\n"
            "LHS 1832 - PRO LHS 1832 Labour\n"
            "1 INF+ mission(s)")
        ),
        (
            [
                "EDA Kunti League"
            ], 
            "LesPaul58_Journal.210117142551.01.log",
            load_test_market,
            ("Arun - ANTI EDA Kunti League\n"
            "1 INF+++++ mission(s)\n"
            "\n"
            "LHS 1832 - ANTI EDA Kunti League\n" 
            "2 market buy(s). Total: 1,088 T and 1,816,960 CR. Average: 1,670 CR/T at supply 0.0\n"
            "2 T trade at 51,622 CR average profit per T\n"
            "\n"
            "Trumuye - ANTI EDA Kunti League\n"
            "7 INF++ mission(s)\n"
            "3 INF+++ mission(s)\n"
            "8 INF+++++ mission(s)")
        ),
        (
            {
                "EDA Kunti League"
            }, 
            "696613390.log",
            load_test_market,
            ("Trumuye - ANTI EDA Kunti League\n"
            "1 INF+++ mission(s)")
        ),
        (
            {
                "EDA Kunti League"
            }, 
            "696609571.log",
            load_test_market,
            ("Trumuye - ANTI EDA Kunti League\n"
            "1 INF++ mission(s)")
        ),
        (
            {
                "EDA Kunti League"
            },
            "Journal.210122183958.01.log",
            load_test_market,
            (
                "Kunti - ANTI EDA Kunti League\n"
                "3,347,636 CR of Combat Bonds"
            )
        ),
        (
            {
                "EDA Kunti League"
            },
            "Journal.210125173739.01.log",
            load_test_market,
            (
                "San Davokje - ANTI EDA Kunti League\n"
                "80 T trade at 3,477 CR average profit per T\n"
                "\n"
                "San Davokje - PRO EDA Kunti League\n1 INF++++ mission(s)"
            )
        ),
        (
            {
                "EDA Kunti League"
            },
            "Journal.210125115425.01.log",
            load_test_market,
            (
                "HR 1597 - PRO EDA Kunti League\n"
                "5 T trade at 3,734 CR average profit per T"
            )
        ),
        (
            {
                "Yuri Grom"
            },
            "Journal.210120211308.01.log",
            load_test_market,
            ("Eta-1 Pictoris - ANTI Yuri Grom\n"
            "26 clean ship kill(s)")
        ),
        (
            {"Atfero Blue General & Co"},
            "Journal.200509115806.01.log",
            load_test_market,
            ("Atfero - ANTI Atfero Blue General & Co\n"
            "2 INF+ mission(s)\n"
            "3 INF++ mission(s)\n"
            "1 market buy(s). Total: 15 T and 12,885 CR. Average: 859 CR/T at supply 0.0\n"
            "77 T trade at 1,048 CR average profit per T\n"
            "1 failed mission(s)\n"
            "\n"
            "Atfero - PRO Atfero Blue General & Co\n"
            "4 INF+ mission(s)\n"
            "1 INF++ mission(s)")
        ),
        (
            {"EDA Kunti League"},
            "Journal.210212124540.01.log",
            load_test_market,
            ("Anek Wango - ANTI EDA Kunti League\n"
            "1,168 T trade at -1,000 CR average profit per T\n"
            "\n"
            "Herci - PRO EDA Kunti League\n"
            "2,930,517 CR of Combat Bonds\n"
            "\n"
            "Trumuye - ANTI EDA Kunti League\n"
            "3,136 T trade at -1,000 CR average profit per T\n"
            "\n"
            "Trumuye - PRO EDA Kunti League\n"
            "1,339,513 CR of Combat Bonds\n"
            "13 market buy(s). Total: 10,091 T and 847,644 CR. Average: 84 CR/T at supply 3.0")
        ),
        (
            {"EDA Kunti League"},
            "Journal.210221171753.01.log",
            load_test_market,
            ("Kunti - PRO EDA Kunti League\n"
            "1 INF+ mission(s)\n"
            "1 INF++ mission(s)\n"
            "2 INF+++ mission(s)\n"
            "2 INF++++ mission(s)\n"
            "1 INF+++++ mission(s)\n"
            "348,491 CR of Bounty Vouchers\n"
            "10,402 CR of Cartography Data\n"
            "\n"
            "LTT 2337 - ANTI EDA Kunti League\n"
            "1 INF+++++ mission(s)")
        ),
        (
            {"Federal Defense League"},
            "Journal.210225200231.01.log",
            load_test_market,            
            ("LHS 1832 - PRO Federal Defense League\n"
            "2 INF++ mission(s)\n"
            "11,772,015 CR of Combat Bonds")
        ),
        (
            {"Extra Corporation"},
            "Journal.210817213224.01.log",
            load_test_market,
            ("Naualam - ANTI Extra Corporation\n"
            "5 INF+ mission(s)\n"
            "1 INF++ mission(s)\n"
            "\n"
            "Naualam - PRO Extra Corporation\n"
            "1,278,672 CR of Bounty Vouchers")
        ),
        (
            {"EDA Kunti League"},
            "Journal.210818120219.01.log",
            load_test_market,
            ("Naualam - PRO EDA Kunti League\n"
            "7,566,083 CR of Combat Bonds")
        ),
        (
            {"EDA Kunti League"},
            "Journal.210805213331.01.log",
            load_test_market,
            ("Kanates - ANTI EDA Kunti League\n"
            "1 INF+++ mission(s)\n"
            "1 INF++++ mission(s)\n"
            "\n"
            "Kanates - PRO EDA Kunti League\n"
            "5 INF++ mission(s)\n"
            "2 INF+++++ mission(s)\n"
            "3,453,667 CR of Bounty Vouchers\n"
            "38,289,972 CR of Cartography Data\n"
            "6 T trade at 515 CR average profit per T\n"
            "\n" 
            "Kunti - PRO EDA Kunti League\n"
            "3,283,200 CR of Organic Data\n"
            "\n"
            "Kutjara - ANTI EDA Kunti League\n"
            "1 INF+++ mission(s)\n"
            "1 INF++++ mission(s)\n"
            "\n"
            "LTT 2337 - ANTI EDA Kunti League\n"
            "1 INF++ mission(s)\n"
            "7,150 CR of Bounty Vouchers\n"
            "8 T trade at 1,255 CR average profit per T\n"
            "1 failed mission(s)\n"
            "63,600 CR of Organic Data\n"
            "\n"
            "LTT 2337 - PRO EDA Kunti League\n"
            "1 INF+ mission(s)\n"
            "1 INF++ mission(s)\n"
            "2,600 CR of Bounty Vouchers\n"
            "\n"
            "Mors - ANTI EDA Kunti League\n"
            "1 INF++ mission(s)")
        )
    ])
def test_journal_file(minor_factions:List[str], journal_file_name:str, load_last_market: Callable[[], Dict], expected_activity:str):
    tracker = Tracker(minor_factions = minor_factions, load_last_market = load_last_market)
    with open("tests/journal_files/" + journal_file_name) as journal_file:
        for line in journal_file.readlines():
            tracker.on_event(json.loads(line))

    # Sanity checks
    assert len([event_summary for event_summary in tracker._event_summaries if not set(event_summary.pro).isdisjoint(set(event_summary.anti))]) == 0 # No overlaps
    # assert len([event_summary for event_summary in tracker._event_summaries if len(event_summary.pro) == 0]) == 0  # No empty pro (can happen if system is not found)
    # assert len([event_summary for event_summary in tracker._event_summaries if len(event_summary.anti) == 0]) == 0  # No empty anti (can happen if system is not found)

    # tracker._update_activity()
    assert tracker.activity == expected_activity
    #print(stream.getvalue())


@pytest.mark.parametrize(
    "journal_file_name, load_last_market",
    [
        (None, None),
        (
            "Journal.201019220908.01.log",
            lambda: { 
                "Consumer Technology": { "id":128049240, "Name":"$consumertechnology_name;", "Name_Localised":"Consumer Technology", "Category":"$MARKET_category_consumer_items;", "Category_Localised":"Consumer items", "BuyPrice":0, "SellPrice":7186, "MeanPrice":6690, "StockBracket":0, "DemandBracket":2, "Stock":0, "Demand":18, "Consumer":True, "Producer":False, "Rare":False },
                "Coltan": { "id":128049159, "Name":"$coltan_name;", "Name_Localised":"Coltan", "Category":"$MARKET_category_minerals;", "Category_Localised":"Minerals", "BuyPrice":5051, "SellPrice":4846, "MeanPrice":6163, "StockBracket":3, "DemandBracket":0, "Stock":277, "Demand":1, "Consumer":False, "Producer":True, "Rare":False }
            }
        )
    ]
)
def test_tracker_clear_activity(journal_file_name, load_last_market):
    events = []
    if(journal_file_name):
        with open("tests/journal_files/" + journal_file_name) as journal_file:
            events = [json.loads(line) for line in journal_file.readlines()]

    MINOR_FACTIONS = set(["EDA Kunti League"])
    tracker = Tracker(minor_factions = MINOR_FACTIONS, load_last_market = load_last_market)
    for event in events:
        tracker.on_event(event)
    tracker.clear_activity()
    assert(tracker.activity == "")
    assert(tracker._event_summaries == [])


def load_test_market():
    return { 
        "Tritium": { "id":128961249, "Name":"$tritium_name;", "Name_Localised":"Tritium", "Category":"$MARKET_category_chemicals;", "Category_Localised":"Chemicals", "BuyPrice":39541, "SellPrice":39539, "MeanPrice":51707, "StockBracket":0, "DemandBracket":0, "Stock":0, "Demand":0, "Consumer":False, "Producer":False, "Rare":False },
        "Power Generators": { "id":128049217, "Name":"$powergenerators_name;", "Name_Localised":"Power Generators", "Category":"$MARKET_category_machinery;", "Category_Localised":"Machinery", "BuyPrice":0, "SellPrice":2728, "MeanPrice":2466, "StockBracket":0, "DemandBracket":2, "Stock":0, "Demand":30, "Consumer":True, "Producer":False, "Rare":False },
    }


@pytest.mark.parametrize(
    "journal_file_name, load_last_market, minor_factions_and_expected_activty",
    [
        (
            "Journal.210125173739.01.log",
            load_test_market,
            [
                (
                    {"EDA Kunti League"},
                    (
                        "San Davokje - ANTI EDA Kunti League\n"
                        "80 T trade at 3,477 CR average profit per T\n"
                        "\n"
                        "San Davokje - PRO EDA Kunti League\n"
                        "1 INF++++ mission(s)"
                    )
                ),
                (
                    {"San Davokje Empire Party"},
                    (
                        "San Davokje - ANTI San Davokje Empire Party\n"
                        "1 INF++++ mission(s)\n"
                        "\n"
                        "San Davokje - PRO San Davokje Empire Party\n"
                        "80 T trade at 3,477 CR average profit per T"
                    )
                )
            ]
        )
    ]
)
def test_tracker_change_minor_factions(journal_file_name:str, load_last_market: Callable[[], Dict], minor_factions_and_expected_activty:List):
    tracker = Tracker(minor_factions = [], load_last_market = load_last_market)
    with open("tests/journal_files/" + journal_file_name) as journal_file:
        for line in journal_file.readlines():
            tracker.on_event(json.loads(line))
    for minor_factions, expected_activity in minor_factions_and_expected_activty:
        tracker.minor_factions = minor_factions
        assert tracker.activity == expected_activity