import csv
from datetime import datetime


file_name = 'results.csv'

def get_result(file_name: str):
    with open(file_name) as csvfile:
        dict_reader = csv.DictReader(csvfile, delimiter='|')
    
        last_result = list(dict_reader)[0]

        timestamp = int(last_result['timestamp'][:-3])
        date = datetime.fromtimestamp(timestamp)
        print(date)
    return dict_reader

