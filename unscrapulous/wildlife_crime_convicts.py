#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'http://wccb.gov.in/Content/Convicts.aspx'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'wildlife-crime-convicts.csv'

def main(conn, session):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE, session)
    table = get_table(soup, omit_cols=[2])
    convert_into_csv([OUTPUT_FILE], OUTPUT_DIR, table=table)

    alias = {
        'Name': 'Name, Father\'s Name &\r\n            Address'
    }
    write_to_db(conn, os.path.join(OUTPUT_DIR, OUTPUT_FILE), SOURCE, alias)
