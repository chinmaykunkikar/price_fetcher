# Price Fetcher
A simple web scrapper written in Python3 that fetches price of any listed item from retailers like JioMart and Fraazo and dumps them as JSON and CSV.

## Disclaimer
1. Cannot guarantee it's working, as website may change it's structure or URL at any point in time and I might not keep it up-to-date with those changes.

## Features
1. Fetches Name and Price of any commodity on the website.
2. Cleans and normalizes the obtained data (i.e calculates and dumps price for a per kg, per piece or per pack).

## Usage
Below sample code for Linux also it is assumed that Python3 is installed.    
```bash
# change directory to project folder
cd fetch_prices

# create a virtual env
python -m venv .env

# enable the virtual environment (Windows Batch)
.env\Scripts\activate.bat
#
# OR
#
# enable the virtual environment (PowerShell)
.env\Scripts\Activate.ps1

# install requirements
pip install -r requirements.txt

# once all requirements has been installed
# you can run the script by -
python fetch_data.py (fraazo|jiomart)
# data will be fetched and dumped in the folder mentioned in config (default: raw_data)

# above dumped data can then be cleaned by running
python clean_data.py <raw_file_path>

# example
python clean_data.py raw_data/raw-2022031415.json
```

## Configurations
Configuration file is `config.py`.  

Available configurable values:
1. Folder Name and File Name by which the files will be created.
    ```python
    raw_data_folder = "raw_data"
    raw_file_name_format = "raw-%Y%m%d%H"

    clean_data_folder = "clean_data"
    clean_file_name_format = "clean-%Y%m%d%H"
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
    jiomart_url_category = [
        {
        "retailer": "JIOMART",
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
