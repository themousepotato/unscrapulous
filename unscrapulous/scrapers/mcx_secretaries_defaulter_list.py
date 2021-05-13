#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://www.mcxindia.com/Investor-Services/defaulters/defaulters-list'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'mcx-secretaries-defaulter-list.csv'

def main(conn, session):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE, session)
    table = get_table(soup, {'id': 'lstDefaulter'})
    convert_into_csv([OUTPUT_FILE], OUTPUT_DIR, table=table)

    alias = {
        'Name': '\nDefaulter Member\'s Name\n',
        'AddedDate': '\nDate of Declaration as Defaulter\n'
    }
    write_to_db(conn, os.path.join(OUTPUT_DIR, OUTPUT_FILE), SOURCE, alias)
