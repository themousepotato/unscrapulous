#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://sfio.nic.in/'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'sfio-convicted.csv'

def main(conn, session):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE, session)
    menu_links = {a.text : a.get('href') for a in soup.find_all('a', class_='menu__link')}
    file_url = menu_links['List of Directors Convicted']
    filenames = list(download_files([file_url], OUTPUT_DIR, session).keys())
    convert_into_csv(filenames, OUTPUT_DIR)
    delete_files(filenames)
    os.rename(os.path.join(OUTPUT_DIR, filenames[0].replace('pdf', 'csv')),
              os.path.join(OUTPUT_DIR, OUTPUT_FILE))

    alias = {
        'Name': 'Name of the Company',
        'AddedDate': 'Date of filing / Reciving of notice'
    }
    write_to_db(conn, os.path.join(OUTPUT_DIR, OUTPUT_FILE), SOURCE, alias)
