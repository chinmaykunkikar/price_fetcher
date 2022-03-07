from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import config


def fetch_product_name_and_price(url, pincode):
    city = config.get_city_name_with_pincode(pincode)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(
        f"C:\webdrivers\chromedriver.exe", options=options)

    print("Fetching... [%s] for [%s - %s]" % (url, pincode, city))

    return_dict = {"url": url, "pincode": pincode, "city": config.get_city_name_with_pincode(
        pincode), "category": config.get_category_from_url(url), "items": []}
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
            ">>> No items fetched! [%s] for [%s - %s]" % (url, pincode, city))

    print("Fetched! [%s] for [%s]" % (url, pincode))

    return return_dict


def fetch_all_product_name_and_price(pincode_to_city, url_to_category, max_page_check):
    raw_json = []
    for pin in pincode_to_city:
        for url in url_to_category:
            raw_json.append(fetch_product_name_and_price(
                url["url"], pin["pincode"]))
    return raw_json


if __name__ == "__main__":
    raw_json = fetch_all_product_name_and_price(
        config.pincode_to_city, config.url_to_category, config.max_page_check)
    config.write_to_raw_json_file(raw_json)
