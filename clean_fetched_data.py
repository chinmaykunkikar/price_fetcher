import math
import config
import sys

import quantity_measure


def get_normalized_quantity(json_items):
    quantity_items = []

    for item in json_items:
        is_found = False
        for suffix in quantity_measure.quantity_trim:
            for suff in suffix["suffix"]:
                if item["raw_name"].lower().strip().endswith(suff):
                    if item["price"] != 0:
                        quantity_items.append(
                            {
                                "raw_name": item["raw_name"],
                                "price": item["price"],
                                "name": item["raw_name"][:-(len(suff))].strip().strip("-"),
                                "normalized_measure": suffix["measure"],
                                "normalized_price": math.ceil(item["price"] * suffix["price_multiplier"]),
                                "selling_measure": suffix["selling_measure"],
                                "selling_quantity": suffix["selling_quantity"],
                                "selling_price": item["price"]
                            }
                        )
                    is_found = True
                    break
            if is_found:
                break
        if not is_found:
            if item["price"] != 0:
                print(">>> Unable to get quantity for [%s]" % item["raw_name"])
                quantity_items.append(
                    {
                        "raw_name": item["raw_name"],
                        "price": item["price"],
                        "name": item["raw_name"],
                        "normalized_measure": "unknown",
                        "normalized_price": item["price"],
                        "selling_measure": "unknown",
                        "selling_quantity": 1,
                        "selling_price": item["price"]
                    }
                )
    return quantity_items


def get_all_normalized_quantities_json(any_json):
    for i in range(len(any_json)):
        any_json[i]["items"] = get_normalized_quantity(any_json[i]["items"])
    return any_json


def merge_all_pages(any_json):
    return_json = []
    for entry in any_json:
        if len(return_json) > 0 and entry["category"] == return_json[-1]["category"] and entry["pincode"] == return_json[-1]["pincode"]:
            return_json[-1]["items"].extend(entry["items"])
        else:
            return_json.append(entry)
    return return_json


def remove_empty_items(any_json):
    return_json = []
    for entry in any_json:
        if len(entry["items"]) != 0:
            return_json.append(entry)
    return return_json


def get_normalized_names(json_items):
    normalized_names = []

    for item in json_items:
        pass


if __name__ == "__main__":
    raw_file_path = sys.argv[1]
    raw_json = config.read_from_raw_json_file(raw_file_path)

    clean_json = get_all_normalized_quantities_json(raw_json)
    clean_json = remove_empty_items(clean_json)
    clean_json = merge_all_pages(clean_json)

    config.write_to_clean_json_file(clean_json)
    config.write_to_clean_csv_file(clean_json)
