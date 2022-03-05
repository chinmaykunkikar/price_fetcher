import requests
from bs4 import BeautifulSoup

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

import config

def fetch_product_name_and_price(url, pincode):
    city = config.get_city_name_with_pincode(pincode)
    
    print("Fetching... [%s] for [%s - %s]" % (url, pincode, city))

    return_dict = {"url": url, "pincode": pincode, "city" : config.get_city_name_with_pincode(pincode), "category" : config.get_category_from_url(url), "items": []}
    cookies = {"nms_mgo_pincode": pincode}
    reply = requests.get(url, cookies=cookies)
    
    if reply.status_code != 200:
        raise Exception("Return code other than 200 - Actual Return Code: %s" % reply.status_code)
    
    soup = BeautifulSoup(reply.content, features="html.parser")

    # Get Product Name, Measure and Quantity from RawName of the product
    for scr in soup('span', {'class': 'clsgetname'}):
        # clsgetname is also present in some other span tag
        # thus need to filter out using 'ellipsis' class
        if 'ellipsis' not in scr.attrs['class']:
            # name, qty, measure = get_name_qty_measure(scr.contents[0])
            return_dict["items"].append(
                {"raw_name": str(scr.contents[0]).strip()})

    # Get Price
    for i, scr in enumerate(soup('span', {'id': 'final_price'})):
        return_dict["items"][i]["price"] = float(
            scr.contents[0].replace("₹", "").strip())
    
    if len(return_dict["items"]) == 0:
        print(">>>   No Items Fetched! [%s] for [%s - %s]" % (url, pincode, city))
    
    print("Fetched! [%s] for [%s]" % (url, pincode))

    return return_dict

def fetch_all_product_name_and_price(pincode_to_city, url_to_category, max_page_check):
    raw_json = []
    for pin in pincode_to_city:
        for url in url_to_category:
            for page_number in range(max_page_check):
                raw_json.append(fetch_product_name_and_price(url["url"]+"/page/"+str(page_number+1), pin["pincode"]))
    return raw_json

if __name__ == "__main__":
    raw_json = fetch_all_product_name_and_price(config.pincode_to_city, config.url_to_category, config.max_page_check)
    config.write_to_raw_json_file(raw_json)
