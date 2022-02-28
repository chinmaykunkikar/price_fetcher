import json, csv

json_list = json.load(open('clean_data/clean.json', 'r'))

with open('clean_data/clean.csv', 'w', newline='') as csv_file:
    fieldnames = ['Commodity', 'Price']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for item_list in json_list:
        for individual_item in item_list['items']:
            writer.writerow({'Commodity': individual_item['name'], 'Price': individual_item['normalized_price']})