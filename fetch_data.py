import sys

import config
import from_fraazo
import from_jiomart


def fetch_products(retailer_url_category, **options):
    raw_json = []
    for url in retailer_url_category:
        match url["retailer"]:
            case "FRAAZO":
                raw_json.append(from_fraazo.fetch_data(url["url"]))
            case "JIOMART":
                if "pincode" in options:
                    for pin in options["pincode"]:
                        for page_number in range(options["max_page_check"]):
                            raw_json.append(from_jiomart.fetch_data(
                                url["url"]+"/page/"+str(page_number+1), pin["pincode"]))
            case _:
                print("Retailer not found\n")
                exit(1)
    return raw_json


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage:\n\tpython " + sys.argv[0] + " (fraazo|jiomart)\n")
        exit(1)
    else:
        retailer = sys.argv[1].lower()
        match retailer:
            case "fraazo":
                raw_json = fetch_products(config.retailer_url_category)
            case "jiomart":
                raw_json = fetch_products(
                    config.retailer_url_category,
                    pincode=config.pincode_to_city,
                    max_page_check=config.max_page_check)
            case _:
                print("Usage:\n\tpython " +
                      sys.argv[0] + " (fraazo|jiomart)\n")
                exit(1)

    config.write_to_raw_json_file(raw_json)
