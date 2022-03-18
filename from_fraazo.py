from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

import config


def fetch_data(url):

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    print("Fetching [%s]" % (url))

    return_dict = {"url": url,
                   "category": config.get_category_from_url(url), "retailer": config.get_retailer_from_url(url), "items": []}
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
