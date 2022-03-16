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

max_page_check = 3

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

retailer_url_category = [
    {
        "retailer": "JIOMART",
        "url": "https://www.jiomart.com/c/groceries/fruits-vegetables/fresh-vegetables/229",
        "category": "VEGETABLES"
    },
    {
        "retailer": "FRAAZO",
        "url": "https://fraazo.com/listing/vegetables/regular-veggies/",
        "category": "VEGETABLES"
    },
    {
        "retailer": "FRAAZO",
        "url": "https://fraazo.com/listing/vegetables/root-vegetables/",
        "category": "VEGETABLES"
    },
    {
        "retailer": "FRAAZO",
        "url": "https://fraazo.com/listing/vegetables/onion-potato-tomatoes/",
        "category": "VEGETABLES"
    },
]

# method definitions that are commonly used


def get_city_name_with_pincode(pincode):
    for pincode_city_map in pincode_to_city:
        if pincode == pincode_city_map["pincode"]:
            return pincode_city_map["city"]


def get_category_from_url(url):
    for url_category_map in retailer_url_category:
        if url_category_map["url"] in url:
            return url_category_map["category"]


def get_retailer_from_url(url):
    for retailer_map in retailer_url_category:
        if retailer_map["url"] in url:
            return retailer_map["retailer"]


def get_retailer_from_json(file_path):
    pass


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
    with open(file_path + ".csv", "w", newline="") as csv_file:
        fieldnames = ["Commodity", "Price (per kg)"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item_list in json_list:
            for item in item_list["items"]:
                writer.writerow(
                    {"Commodity": item["raw_name"], "Price (per kg)": item["normalized_price"]})


def write_to_clean_csv_file(clean_json):
    file_path = clean_data_folder + os.path.sep + \
        time.strftime(clean_file_name_format)
    return write_to_csv_file(clean_json, file_path)
