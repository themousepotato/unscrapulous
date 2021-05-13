#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://www.nseindia.com/regulations/exchange-defaulting-clients'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'nse-regulatory-defaulting-clients.csv'

def main(conn, session):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE, session)
    file_url = soup.find('a', {'class' : 'file'})['href']
    filename = file_url.split('/')[-1]
    download_files([file_url], OUTPUT_DIR)
    convert_into_csv([filename], OUTPUT_DIR, ext='xlsx')
    os.rename(os.path.join(OUTPUT_DIR, filename.replace('xlsx', 'csv')), os.path.join(OUTPUT_DIR, OUTPUT_FILE))
    delete_files([os.path.join(OUTPUT_DIR, filename)])

    alias = {
        'PAN': 'Pan of Client ',
        'Name': 'Name of the Defaulting client ',
        'AddedDate': 'Date of Order / Award '
    }
    write_to_db(conn, os.path.join(OUTPUT_DIR, OUTPUT_FILE), SOURCE, alias)
