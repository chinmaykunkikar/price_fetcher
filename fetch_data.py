import sys

import config
import from_fraazo
import from_jiomart


def fetch_products_from_jiomart(url_to_category, pincode_to_city, max_page_check):
    raw_json = []
    for pin in pincode_to_city:
        for url in url_to_category:
            if "JIOMART" in url["retailer"]:
                for page_number in range(max_page_check):
                    raw_json.append(from_jiomart.fetch_data(
                        url["url"]+"/page/"+str(page_number+1), pin["pincode"]))
    return raw_json


def fetch_products_from_fraazo(url_to_category):
    raw_json = []
    for url in url_to_category:
        if "FRAAZO" in url["retailer"]:
            raw_json.append(from_fraazo.fetch_data(url["url"]))
    return raw_json


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage:\n\tpython " + sys.argv[0] + " (jiomart|fraazo)\n")
        exit(1)
    else:
        retailer = sys.argv[1]
        if retailer == "jiomart":
            raw_json = fetch_products_from_jiomart(
                config.retailer_url_category, config.pincode_to_city, config.max_page_check)
        elif retailer == "fraazo":
            raw_json = fetch_products_from_fraazo(config.retailer_url_category)
        else:
            print("Usage:\n\tpython " + sys.argv[0] + " (jiomart|fraazo)\n")
            exit(1)

    config.write_to_raw_json_file(raw_json)