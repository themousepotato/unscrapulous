#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://www1.nseindia.com/invest/json/exp_members.json'
FILE_PARENT_URL = 'https://www1.nseindia.com/invest/resources/download/'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'nse-expelled-members.csv'

def main(conn, session):
    create_dir(OUTPUT_DIR)
    rjson = get_json_response(SOURCE, session, method='GET')
    table = [list(rjson['data'][0].keys())]
    for data in rjson['data']:
        row = list(data.values())
        row[1] = FILE_PARENT_URL + row[1]
        table.append(row)

    convert_into_csv([OUTPUT_FILE], OUTPUT_DIR, table=table)

    alias = {
        'Name': 'memberName',
        'AddedDate': 'declarationDate'
    }
    write_to_db(conn, os.path.join(OUTPUT_DIR, OUTPUT_FILE), SOURCE, alias)
