from bs4 import BeautifulSoup
from selenium import webdriver

import config


def fetch_from_jiomart(url, pincode):
    city = config.get_city_name_with_pincode(pincode)

    config.initialize_selenium()

    print("Fetching [%s] for [%s - %s]" % (url, pincode, city))

    return_dict = {"url": url, "pincode": pincode, "city": config.get_city_name_with_pincode(
        pincode), "category": config.get_category_from_url(url), "items": []}

    try:
        browser.get(url)
        browser.add_cookie({"name": "nms_mgo_pincode", "value": pincode})
        html = browser.page_source
        soup = BeautifulSoup(html, features="html.parser")
    except Exception as e:
        print(e)
    finally:
        browser.quit()

    # Get Product Name, Measure and Quantity from RawName of the product
    for scr in soup('span', {'class': 'clsgetname'}):
        if 'ellipsis' not in scr.attrs['class']:
            return_dict["items"].append(
                {"raw_name": str(scr.contents[0]).strip()})

    # Get Price
    for i, scr in enumerate(soup('span', {'id': 'final_price'})):
        return_dict["items"][i]["price"] = float(
            scr.contents[0].replace("₹", "").strip())

    if len(return_dict["items"]) == 0:
        print(
            ">>> No items fetched [%s] for [%s - %s]" % (url, pincode, city))

    print("Fetched [%s] for [%s]" % (url, pincode))

    return return_dict


def fetch_all_product_name_and_price(pincode_to_city, url_to_category, max_page_check):
    raw_json = []
    for pin in pincode_to_city:
        for url in url_to_category:
            for page_number in range(max_page_check):
                raw_json.append(fetch_from_jiomart(
                    url["url"]+"/page/"+str(page_number+1), pin["pincode"]))
    return raw_json


if __name__ == "__main__":
    raw_json = fetch_all_product_name_and_price(
        config.pincode_to_city, config.url_to_category, config.max_page_check)
    config.write_to_raw_json_file(raw_json)
