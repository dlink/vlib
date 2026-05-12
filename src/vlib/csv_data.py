''' Read data csv file

    from vlib.csv_data import get_csv_data

    data = get_csv_data('example.csv')
'''

import csv

from vlib.odict import odict

def get_csv_data(filepath):
    '''Read csv file and return list of odicts with standardized headers.
       Note: utf-8-sig deals with BOM (Byte Orde Mark) \ufeff
    '''
    with open(filepath, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        raw_headers = next(reader)
        headers = std_headers(raw_headers)
        rows = []
        for row in reader:
            row_dict = odict(zip(headers, row))
            rows.append(row_dict)
    return rows

def std_headers(headers):
    return [h.strip().lower()\
            .replace(' ', '_')\
            .replace('\\', '_')\
            for h in headers]
