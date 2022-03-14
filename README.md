# Jio Mart Price Fetcher
A Simple WebScrapper written in Python3 that fetches price of any listed item from JioMart.com and dumps them as JSON.

## Disclaimer
1. Cannot guarantee it's working, as website may change it's structure or URL at any point in time and I might not keep it up-to-date with those changes.
2. This is only for educational purposes.

## Features
1. Fetches Name and Price of any commodity on the website.
2. Cleans and normalizes the obtained data (i.e calculates and dumps price for a per kg, per piece or per pack).
3. Can be used to fetch price in different cities from India.

## Usage
Below sample code for Linux also it is assumed that Python3 is installed.    
```bash
# change directory to project folder
cd price_fetcher_jiomart
# create a virtual env
python -m venv .env
# enable the virtual environment
source .env/bin/activate
# install requirements
pip install -r requirements.txt

# once all requirements has been installed
# you can run the script by -
python fetch_data_from_request.py
# data will be fetched and dumped in the folder mentioned in config (default: raw_data)

# above dumped data can then be cleaned by running
python clean_fetched_data.py <raw_file_path>
# example,
python clean_fetched_data.py raw_data/raw-20210102-205105.json
```

## Configurations
Configuration file is `config.py`.  

Available configurable values:
1. Folder Name and File Name by which the files will be created.
    ```python
    raw_data_folder = "raw_data"
    raw_file_name_format = "raw-%Y%m%d-%H%M%S"

    clean_data_folder = "clean_data"
    clean_file_name_format = "clean-%Y%m%d-%H%M%S"
    ```
2. Pincodes of cities of which data needs to be obtained off -
    ```python
    pincode_to_city = [
        {
        "pincode": "400026",
        "city": "Mumbai"
        },
    ...
    ]
    ```
3. URLS of categories that will be crawled -
    ```python
    url_to_category = [
        {
        "url": "https://www.jiomart.com/c/groceries/fruits-vegetables/fresh-vegetables/229",
        "category": "VEGETABLES"
        
        },
    ...
    ]
    ```
4. Max pages that needs to be crawled, useful if a category has items listed accross multiple pages,
    ```python
    max_page_check = 2
    ```

## Dump JSON Format
Sample dumps are available at - [clean_data/clean-20210101-114910.json](clean_data/clean-20210101-114910.json) and [raw_data/raw-20210101-114545.json](raw_data/raw-20210101-114545.json).

## Issues
1. Names of some items differs between different cities, which makes it difficult to compare prices of an item accross city.
2. Same item is sold in 2 different quantities some times, e.g: Onion 1kg and Onion 5Kg (Pack). So after cleaning there are 2 entries of Onion in JSON.

## Future Implementations
1. Normalize/Group Similar items.
2. Using pandas to visualize this data
