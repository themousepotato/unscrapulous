#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://www.icexindia.com/membership/expelled-defaulter-surrendered-members'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'icex-defaulter-members.csv'

def main(conn, session):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE, session)
    soup = soup.find_all(
        'ul',
        {
            'class': 'downloadSec'
        }
    )[0]
    links = {link.text : link.find('a').get('href') for link in soup.find_all('li')}
    
    file_url = links['List of Defaulter Members']
    filenames = list(download_files([file_url], OUTPUT_DIR, session).keys())
    convert_into_csv(filenames, OUTPUT_DIR)
    delete_files([os.path.join(OUTPUT_DIR, filename) for filename in filenames])
    os.rename(os.path.join(OUTPUT_DIR, filenames[0].replace('pdf', 'csv')),
              os.path.join(OUTPUT_DIR, OUTPUT_FILE))
    
    alias = {
        'PAN': 'PAN',
        'Name': 'Name and address of the Member',
        'AddedDate': 'Date of\rDeclaration'
    }
    write_to_db(conn, os.path.join(OUTPUT_DIR, OUTPUT_FILE), SOURCE, alias)
