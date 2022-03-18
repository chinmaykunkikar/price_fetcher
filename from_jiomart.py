from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

import config


def fetch_data(url, pincode):
    city = config.get_city_name_with_pincode(pincode)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    print("Fetching [%s] for [%s - %s]" % (url, pincode, city))

    return_dict = {"url": url, "pincode": pincode, "city": config.get_city_name_with_pincode(
        pincode), "category": config.get_category_from_url(url), "retailer": config.get_retailer_from_url(url), "items": []}

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
    for scr in soup.select("div[id='mstar_box'] span[class='clsgetname']"):
        return_dict["items"].append(
            {"raw_name": str(scr.contents[0]).strip()})

    # Get Price
    for i, scr in enumerate(soup.select("div[id='mstar_box'] span[id='final_price']")):
        return_dict["items"][i]["price"] = float(
            scr.contents[0].replace("₹", "").strip())

    if len(return_dict["items"]) == 0:
        print(
            ">>> No items fetched [%s] for [%s - %s]" % (url, pincode, city))

    print("Fetched [%s] for [%s]" % (url, pincode))

    return return_dict
