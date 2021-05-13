#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://www.nseindia.com/regulations/member-sebi-debarred-entities'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'sebi-debarred-nse.csv'

def main(conn, session):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE, session)
    file_url = soup.find('a', {'class' : 'file--mime-application-vnd-ms-excel'})['href']
    filenames = list(download_files([file_url], OUTPUT_DIR, session).keys())
    convert_into_csv(filenames, OUTPUT_DIR, ext='xls')
    delete_files(filenames)

    filename = os.path.join(OUTPUT_DIR, filenames[0].replace('xls', 'csv'))
    out_filename = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    os.rename(filename, out_filename)
    alias = {
        'PAN': 'PAN',
        'Name': 'Entity / Individual Name',
        'AddedDate': 'Order Date'
    }
    write_to_db(conn, out_filename, SOURCE, alias, fillna=True)
