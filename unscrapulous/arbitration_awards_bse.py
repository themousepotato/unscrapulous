#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://www.bseindia.com/investors/ArbitAwards.aspx'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'arbitration-awards-bse.csv'

def main():
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
    table = get_table(soup, {'id' : 'ContentPlaceHolder1_gvAwardDetails'})
    convert_into_csv(filenames=[OUTPUT_FILE], output_dir=OUTPUT_DIR, table=table)

    # TODO: download data from range of 1 year and paginate
    alias = {
        'Name': 'Name of Member',
        'AddedDate': 'Date Of Issue'
    }
    write_global_csv(filename=os.path.join(OUTPUT_DIR, OUTPUT_FILE), source=SOURCE, alias=alias)


if __name__ == '__main__':
    main()
