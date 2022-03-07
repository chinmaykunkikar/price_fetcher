import time
import json
import os
import csv

# must not be changed
raw_data_folder = "raw_data"
raw_file_name_format = "raw-%Y%m%d%H"

# must not be changed
clean_data_folder = "clean_data"
clean_file_name_format = "clean-%Y%m%d%H"

max_page_check = 4

# path to selenium chromedriver
driver_path = f"C:\webdrivers\chromedriver.exe"

# input for main
# add pincodes that you would like to grab prices from
pincode_to_city = [
    {
        "pincode": "400026",
        "city": "Mumbai"
    },
]

# add categories and corresponding URLs
url_to_category = [
    {
        "url": "https://www.jiomart.com/c/groceries/fruits-vegetables/fresh-vegetables/229",
        "category": "VEGETABLES"
    },
]

fraazo_url_category = [
    {
        "url": "https://fraazo.com/listing/vegetables/regular-veggies/",
        "category": "VEGETABLES"
    },
    {
        "url": "https://fraazo.com/listing/vegetables/root-vegetables/",
        "category": "VEGETABLES"
    },
    {
        "url": "https://fraazo.com/listing/vegetables/onion-potato-tomatoes/",
        "category": "VEGETABLES"
    },
]

# No need to change
# used to clean the obtained raw data
quantity_trim = [
    {
        "suffix": ["per kg", "per kg pack", "per kg (pack)", "1 kg", "1 kg (pack)", "(kg)", "(per kg)"],
        "measure": "kg",
        "price_multiplier": 1,
        "selling_measure": "kg",
        "selling_quantity": 1
    },
    {
        "suffix": ["1.5 kg", "1.5 kg (pack)", "1.5\u00a0kg"],
        "measure": "kg",
        "price_multiplier": 0.66666666666,
        "selling_measure": "kg",
        "selling_quantity": 1.5
    },
    {
        "suffix": ["2.5 kg", "2.5 kg (pack)"],
        "measure": "kg",
        "price_multiplier": 0.4,
        "selling_measure": "kg",
        "selling_quantity": 2.5
    },
    {
        "suffix": ["3.5 kg", "3.5 kg (pack)"],
        "measure": "kg",
        "price_multiplier": 0.28571428571,
        "selling_measure": "kg",
        "selling_quantity": 3.5
    },
    {
        "suffix": ["3 kg", "3 kg (pack)", "3 kg pack"],
        "measure": "kg",
        "price_multiplier": 0.33333333333,
        "selling_measure": "kg",
        "selling_quantity": 3
    },
    {
        "suffix": ["2 kg", "2 kg (pack)", "2 kg pack"],
        "measure": "kg",
        "price_multiplier": 0.5,
        "selling_measure": "kg",
        "selling_quantity": 2
    },
    {
        "suffix": ["5 kg", "5 kg (pack)", "5 kg pack"],
        "measure": "kg",
        "price_multiplier": 0.2,
        "selling_measure": "kg",
        "selling_quantity": 5
    },
    {
        "suffix": ["25 g", "25 gm", "25 gram", "25 g (pack)"],
        "measure": "kg",
        "price_multiplier": 40,
        "selling_measure": "gm",
        "selling_quantity":25
    },
    {
        "suffix": ["100 g", "100 gm", "100 gram", "100 g (pack)"],
        "measure": "kg",
        "price_multiplier": 10,
        "selling_measure": "gm",
        "selling_quantity": 100
    },
    {
        "suffix": ["150 g", "150 gm", "150 gram", "150 g (pack)"],
        "measure": "kg",
        "price_multiplier": 6.66666666667,
        "selling_measure": "gm",
        "selling_quantity": 150
    },
    {
        "suffix": ["200 g", "200 gm", "200 gram", "200 g (pack)", "200 gms"],
        "measure": "kg",
        "price_multiplier": 5,
        "selling_measure": "gm",
        "selling_quantity": 200
    },
    {
        "suffix": ["250 g", "250 gm", "250 g (pack)"],
        "measure": "kg",
        "price_multiplier": 4,
        "selling_measure": "gm",
        "selling_quantity": 250
    },
    {
        "suffix": ["500 g (pack)", "per 500 g", "500 g", "500 gm", "500 gram"],
        "measure": "kg",
        "price_multiplier": 2,
        "selling_measure": "gm",
        "selling_quantity": 500
    },
    {
        "suffix": ["50 g", "50 gm", "50 gram", "50 g (pack)"],
        "measure": "kg",
        "price_multiplier": 20,
        "selling_measure": "gm",
        "selling_quantity": 50
    },
    {
        "suffix": ["400 g", "400 gm", "400 gram", "400 g (pack)"],
        "measure": "kg",
        "price_multiplier": 2.5,
        "selling_measure": "gm",
        "selling_quantity": 400
    },
    {
        "suffix": ["per pack", "1 pack", "1 bunch", "per bunch"],
        "measure": "pack",
        "price_multiplier": 1,
        "selling_measure": "pack",
        "selling_quantity": 1
    },
    {
        "suffix": ["12 pcs", "12 pcs (pack)"],
        "measure": "piece",
        "price_multiplier": 0.08333333333,
        "selling_measure": "piece",
        "selling_quantity": 12
    },
    {
        "suffix": ["per pc", "1 pc", "1 piece", "each", "(each)", "whole", "per piece"],
        "measure": "piece",
        "price_multiplier": 1,
        "selling_measure": "piece",
        "selling_quantity": 1
    },
    {
        "suffix": ["2 pcs", "2 pcs (pack)"],
        "measure": "piece",
        "price_multiplier": 0.5,
        "selling_measure": "piece",
        "selling_quantity": 2
    },
    {
        "suffix": ["3 pcs", "(3 pcs)", "3 pcs (pack)", "3 pcs (box)", "3 pcs pack"],
        "measure": "piece",
        "price_multiplier": 0.33333333333,
        "selling_measure": "piece",
        "selling_quantity": 3
    },
    {
        "suffix": ["4 pcs", "(4 pcs)", "4 pcs (pack)", "4 pcs (box)"],
        "measure": "piece",
        "price_multiplier": 0.25,
        "selling_measure": "piece",
        "selling_quantity": 2
    },
    {
        "suffix": ["5 pcs", "5 pcs (pack)"],
        "measure": "piece",
        "price_multiplier": 0.2,
        "selling_measure": "piece",
        "selling_quantity": 5
    },
    {
        "suffix": ["6 pcs", "6 pcs (pack)", "6 pcs (box)", "(6 piece pack)"],
        "measure": "piece",
        "price_multiplier": 0.16666666666,
        "selling_measure": "piece",
        "selling_quantity": 6
    },

    {
        "suffix": ["54 pcs (carton)"],
        "measure": "piece",
        "price_multiplier": 0.01851851851,
        "selling_measure": "piece",
        "selling_quantity": 54
    },
    {
        "suffix": ["30 pcs"],
        "measure": "piece",
        "price_multiplier": 0.03333333333,
        "selling_measure": "piece",
        "selling_quantity": 30
    },
    {
        "suffix": ["kg"],
        "measure": "kg",
        "price_multiplier": 1,
        "selling_measure": "kg",
        "selling_quantity": 1
    },
    {
        "suffix": ["pack", "(pack)"],
        "measure": "pack",
        "price_multiplier": 1,
        "selling_measure": "pack",
        "selling_quantity": 1
    },
]

# method definitions that are commonly used


def get_city_name_with_pincode(pincode):
    for pincode_city_map in pincode_to_city:
        if pincode == pincode_city_map["pincode"]:
            return pincode_city_map["city"]


def get_category_from_url(url):
    for url_category_map in url_to_category:
        if url_category_map["url"] in url:
            return url_category_map["category"]


def read_from_raw_json_file(file_path):
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def write_to_json_file(any_json, file_path):
    print("Writing to [%s]" % file_path)
    with open(file_path, "w") as json_file:
        json.dump(any_json, json_file)
    print("Wrote to [%s]" % file_path)
    return file_path


def write_to_clean_json_file(clean_json):
    file_path = clean_data_folder + os.path.sep + \
        time.strftime(clean_file_name_format) + ".json"
    return write_to_json_file(clean_json, file_path)


def write_to_raw_json_file(raw_json):
    file_path = raw_data_folder + os.path.sep + \
        time.strftime(raw_file_name_format) + ".json"
    return write_to_json_file(raw_json, file_path)


def write_to_csv_file(any_json, file_path):
    with open(file_path + ".json", "r") as json_file:
        json_list = json.load(json_file)
    with open(file_path + ".csv", 'w', newline='') as csv_file:
        fieldnames = ['Commodity', 'Price (per kg)']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item_list in json_list:
            for individual_item in item_list['items']:
                writer.writerow(
                    {'Commodity': individual_item['name'], 'Price (per kg)': individual_item['normalized_price']})


def write_to_clean_csv_file(clean_json):
    file_path = clean_data_folder + os.path.sep + \
        time.strftime(clean_file_name_format)
    return write_to_csv_file(clean_json, file_path)
