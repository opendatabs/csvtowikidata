import csv
import pprint

def read_file(path):
    '''
    Returns all rows as dict
    '''
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f, )
        for row_dict in reader:
            rows.append(row_dict)
    return rows


rows = read_file("Einwohnerzahl_BS.csv")
pprint.pprint(rows)
