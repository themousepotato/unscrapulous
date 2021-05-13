#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

PARENT_SOURCE = 'http://www.mca.gov.in'
SOURCE = 'http://www.mca.gov.in/MinistryV2/defaulterdirectorslist.html'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'mca-director-defaulter-list.csv'

def main(conn, session):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE, session)
    file_urls = [PARENT_SOURCE + a['href'] for a in soup.find_all('a') if a.text.startswith('Link to view')]
    filenames = download_files(file_urls, OUTPUT_DIR, session).keys()
    convert_into_csv(filenames, OUTPUT_DIR, ext='pdf')
    write_added_date(filenames)
    delete_files(filenames)
    filenames = [filename.replace('pdf', 'csv') for filename in filenames]
    merge_csvs(filenames, os.path.join(OUTPUT_DIR, OUTPUT_FILE))
    delete_files(filenames)

    alias = {
        'Name': 'Name',
        'AddedDate': 'AddedDate'
    }
    write_to_db(conn, os.path.join(OUTPUT_DIR, OUTPUT_FILE), SOURCE, alias)
