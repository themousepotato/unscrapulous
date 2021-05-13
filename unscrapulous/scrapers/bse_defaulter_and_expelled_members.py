#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://www.bseindia.com/static/members/List_defaulters_Expelled_members.aspx'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'bse-defaulter-and-expelled-members.csv'

def main(conn, session):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE, session)
    table = get_table(soup)
    table = table[1:]
    convert_into_csv([OUTPUT_FILE], OUTPUT_DIR, table=table)

    alias = {
        'Name': 'Name of the Member',
        'AddedDate': 'Date on which Declared Defaulter/Expelled'
    }
    # TODO: fix invalid format after writing global csv
    # write_to_db(conn, os.path.join(OUTPUT_DIR, OUTPUT_FILE), SOURCE, alias)
