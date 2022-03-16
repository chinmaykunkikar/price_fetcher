from selenium import webdriver

from bs4 import BeautifulSoup

import config


def fetch_data(url, pincode):
    city = config.get_city_name_with_pincode(pincode)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(config.driver_path, options=options)

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
