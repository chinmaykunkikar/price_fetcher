import time
import json
import os
import csv

# must not be changed
raw_data_folder = "raw_data"
clean_data_folder = "clean_data"

file_name_format = "%Y%m%d"

max_page_check = 3

# input for main
# add pincodes that you would like to grab prices from
pincode_to_city = [
    {
        "pincode": "400703",
        "city": "Thane"
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
    {
        "retailer": "AGMARKNET",
        "url": "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001902b31a21daa411e7ee1d683e5fbc2dc&format=csv&limit=1000&filters[state]=Maharashtra&filters[district]=Mumbai",
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


def get_retailer_from_json(any_json):
    return str(any_json[0]["retailer"]).lower()


def read_from_raw_json_file(file_path):
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def write_to_json_file(any_json, file_path):
    print("Writing to [%s]" % file_path)
    with open(file_path, "w") as json_file:
        json.dump(any_json, json_file)
    print("Wrote to [%s]" % file_path)
    return file_path


def write_to_any_file(any_data, file_path):
    print("Writing to [%s]" % file_path)
    with open(file_path, "wb") as any_file:
        any_file.write(any_data)
    print("Wrote to [%s]" % file_path)
    return file_path


def write_to_clean_json_file(clean_json):
    file_path = clean_data_folder + os.path.sep + \
        "clean-" + time.strftime(file_name_format) + \
        "-" + get_retailer_from_json(clean_json) + ".json"
    return write_to_json_file(clean_json, file_path)


def write_to_raw_json_file(raw_json):
    file_path = raw_data_folder + os.path.sep + \
        "raw-" + time.strftime(file_name_format) + \
        "-" + get_retailer_from_json(raw_json) + ".json"
    return write_to_json_file(raw_json, file_path)


def write_to_csv_file(any_json, file_path):
    with open(file_path + ".json", "r") as json_file:
        json_list = json.load(json_file)
    with open(file_path + ".csv", "w", newline="") as csv_file:
        fieldnames = ["Commodity", "Normal Price", "Normal UoM"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item_list in json_list:
            for item in item_list["items"]:
                writer.writerow(
                    {
                        "Commodity": item["name"],
                        "Normal Price": item["normalized_price"],
                        "Normal UoM": item["normalized_measure"],
                    })


def write_to_clean_csv_file(clean_json):
    file_path = clean_data_folder + os.path.sep + \
        "clean-" + time.strftime(file_name_format) + "-" + \
        get_retailer_from_json(clean_json)
    return write_to_csv_file(clean_json, file_path)


def write_to_agmark_csv_file(clean_csv):
    file_path = clean_data_folder + os.path.sep + \
        "clean-" + time.strftime(file_name_format) + "-" + \
        "agmarknet.csv"
    return write_to_any_file(clean_csv, file_path)
