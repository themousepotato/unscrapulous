#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://www.mcxindia.com/Investor-Services/defaulters/defaulters-list'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'mcx-secretaries-defaulter-list.csv'

def main():
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
    table = get_table(soup, {'id': 'lstDefaulter'})
    convert_into_csv(filenames=[OUTPUT_FILE], output_dir=OUTPUT_DIR, table=table)

    alias = {
        'Name': '\nDefaulter Member\'s Name\n',
        'AddedDate': '\nDate of Declaration as Defaulter\n'
    }
    write_global_csv(filename=os.path.join(OUTPUT_DIR, OUTPUT_FILE), source=SOURCE, alias=alias)


if __name__ == '__main__':
    main()