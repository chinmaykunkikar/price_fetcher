from bs4 import BeautifulSoup
import sys

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import config


def fetch_from_jiomart(url, pincode):
    city = config.get_city_name_with_pincode(pincode)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level 3') 
    browser = webdriver.Chrome(config.driver_path, options=options)

    print("Fetching [%s] for [%s - %s]" % (url, pincode, city))

    return_dict = {"url": url, "pincode": pincode, "city": config.get_city_name_with_pincode(
        pincode), "category": config.get_category_from_jiomart(url), "items": []}

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


def fetch_from_fraazo(url):

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level 3')
    browser = webdriver.Chrome(config.driver_path, options=options)

    print("Fetching [%s]" % (url))

    return_dict = {"url": url,
                   "category": config.get_category_from_fraazo(url), "items": []}
    try:
        browser.get(url)
        timeout_in_seconds = 10
        WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located(
            (By.XPATH, "//div[@class='frz-fw-500 frz-font-14 frz-lh-19 frz-web-product-name frz-overlay-sold-out']")))
        html = browser.page_source
        soup = BeautifulSoup(html, features="html.parser")
    except TimeoutException:
        print("Connection timed out.")
    finally:
        browser.quit()

    # Get Product Name, Measure and Quantity from RawName of the product
    for scr in soup('div', {'class': 'frz-web-product-name'}):
        return_dict["items"].append(
            {"raw_name": str(scr.contents[0]).strip()})

    # Get Price
    for i, scr in enumerate(soup.select("div[class='frz-rp-10']")):
        return_dict["items"][i]["price"] = float(
            scr.contents[0].strip())

    # Get Pack Size
    for i, scr in enumerate(soup('div', {'class': 'frz-pack-size'})):
        return_dict["items"][i]["pack_size"] = scr.contents[0].strip()

    if len(return_dict["items"]) == 0:
        print(
            ">>> No items fetched from [%s]" % (url))

    print("Fetched from [%s]" % (url))

    return return_dict


def fetch_products_from_jiomart(url_to_category, pincode_to_city, max_page_check):
    raw_json = []
    for pin in pincode_to_city:
        for url in url_to_category:
            for page_number in range(max_page_check):
                raw_json.append(fetch_from_jiomart(
                    url["url"]+"/page/"+str(page_number+1), pin["pincode"]))
    return raw_json


def fetch_products_from_fraazo(url_to_category):
    raw_json = []
    for url in url_to_category:
        raw_json.append(fetch_from_fraazo(url["url"]))
    return raw_json


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage:\n\tpython fetch_data_from_request.py (jiomart|fraazo)\n")
        exit(1)
    else:
        company = sys.argv[1]
        if company == "jiomart":
            raw_json = fetch_products_from_jiomart(
                config.jiomart_url_category, config.pincode_to_city, config.max_page_check)
        elif company == "fraazo":
            raw_json = fetch_products_from_fraazo(config.fraazo_url_category)
        else:
            print("Usage:\n\tpython fetch_data_from_request.py (jiomart|fraazo)\n")
            exit(1)

    config.write_to_raw_json_file(raw_json)
