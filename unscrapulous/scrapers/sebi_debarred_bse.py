#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

PARENT_SOURCES = ['https://www.bseindia.com', 'https://www.bseindia.com/investors/']
SOURCE = 'https://www.bseindia.com/investors/debent.aspx'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'sebi-debarred-bse.csv'

def main(conn, session):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE, session)
    link = soup.find('div', {'id': 'divid'}).find('div')['ng-include'].replace('\'', '')
    link = PARENT_SOURCES[1] + link
    soup = get_soup(link, session)
    file_url = PARENT_SOURCES[0] + soup.find_all('a')[0]['href'][2:]
    zip_filename = list(download_files([file_url], OUTPUT_DIR, session).keys())[0]
    filename = extract_zip(zip_filename, OUTPUT_DIR)[0]
    delete_files([zip_filename])
    convert_into_csv([filename], OUTPUT_DIR, ext='xlsx')
    os.rename(os.path.join(OUTPUT_DIR, filename.replace('xlsx', 'csv')),
              os.path.join(OUTPUT_DIR, OUTPUT_FILE))
    delete_files([os.path.join(OUTPUT_DIR, filename)])

    alias = {
        'PAN': 'PAN No.',
        'Name': 'Scrip Name /Entity',
        'AddedDate': 'Date of Order '
    }
    write_to_db(conn, os.path.join(OUTPUT_DIR, OUTPUT_FILE), SOURCE, alias)
