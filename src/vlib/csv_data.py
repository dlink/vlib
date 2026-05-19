''' Csv file related functions

     - read_csv(filenpath)

     - write_csv(data, headers=None, filepath=None)
'''

import csv
import sys

from vlib.odict import odict

def read_csv(filepath):
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

def write_csv(data, headers=None, filepath=None):
    '''Write list of dict-like records as csv.

       If filepath is None or '-', write to stdout.
    '''
    if headers is None:
        headers = list(data[0].keys()) if data else []

    if filepath is None or filepath == '-':
        f = sys.stdout
        close_file = False
    else:
        f = open(filepath, 'w', newline='', encoding='utf-8')

    try:
        writer = csv.writer(f)
        writer.writerow(headers)

        for rec in data:
            writer.writerow([rec.get(h, '') for h in headers])
    finally:
        if close_file:
            f.close()
