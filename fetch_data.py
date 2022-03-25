import sys

import config
import from_agmarknet
import from_fraazo
import from_jiomart


def fetch_products_from_agmarknet(retailer_url_category):
    for url in retailer_url_category:
        if "AGMARKNET" in url["retailer"]:
            config.write_to_agmark_csv_file(
                from_agmarknet.fetch_data(url["url"]))
    exit(0)


def fetch_products_from_fraazo(retailer_url_category):
    raw_json = []
    for url in retailer_url_category:
        if "FRAAZO" in url["retailer"]:
            raw_json.append(from_fraazo.fetch_data(url["url"]))
    return raw_json


def fetch_products_from_jiomart(retailer_url_category, pincode_to_city, max_page_check):
    raw_json = []
    for pin in pincode_to_city:
        for url in retailer_url_category:
            if "JIOMART" in url["retailer"]:
                for page_number in range(max_page_check):
                    raw_json.append(from_jiomart.fetch_data(
                        url["url"]+"/page/"+str(page_number+1), pin["pincode"]))
    return raw_json


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage:\n\tpython " +
              sys.argv[0] + " (agmarknet|fraazo|jiomart)\n")
        exit(1)
    else:
        retailer = sys.argv[1]
        if retailer == "agmarknet":
            fetch_products_from_agmarknet(config.retailer_url_category)
        elif retailer == "fraazo":
            raw_json = fetch_products_from_fraazo(config.retailer_url_category)
        elif retailer == "jiomart":
            raw_json = fetch_products_from_jiomart(
                config.retailer_url_category, config.pincode_to_city, config.max_page_check)
        else:
            print("Usage:\n\tpython " +
                  sys.argv[0] + " (agmarknet|fraazo|jiomart)\n")
            exit(1)

    config.write_to_raw_json_file(raw_json)
