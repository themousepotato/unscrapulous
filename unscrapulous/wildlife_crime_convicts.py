#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'http://wccb.gov.in/Content/Convicts.aspx'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'wildlife-crime-convicts.csv'

def main():
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
    table = get_table(soup, omit_cols=[2])
    convert_into_csv(filenames=[OUTPUT_FILE], output_dir=OUTPUT_DIR, table=table)

    alias = {
        'Name': 'Name, Father\'s Name &\r\n            Address'
    }
    write_global_csv(filename=os.path.join(OUTPUT_DIR, OUTPUT_FILE), source=SOURCE, alias=alias)

if __name__ == '__main__':
    main()
