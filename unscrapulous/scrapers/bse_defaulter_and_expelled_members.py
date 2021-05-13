#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://www.bseindia.com/static/members/List_defaulters_Expelled_members.aspx'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'bse-defaulter-and-expelled-members.csv'

def main(conn):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
    table = get_table(soup)
    table = table[1:]
    convert_into_csv(filenames=[OUTPUT_FILE], output_dir=OUTPUT_DIR, table=table)

    alias = {
        'Name': 'Name of the Member',
        'AddedDate': 'Date on which Declared Defaulter/Expelled'
    }
    # TODO: fix invalid format after writing global csv
    # write_to_db(filename=os.path.join(OUTPUT_DIR, OUTPUT_FILE), source=SOURCE, alias=alias)

