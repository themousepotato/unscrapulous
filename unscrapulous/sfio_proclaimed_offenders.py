#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://sfio.nic.in/'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'sfio-proclaimed-offenders.csv'

def main(conn, session):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE, session)
    menu_links = {link.text : link.get('href') for link in soup.find_all('a', class_='menu__link')}
    file_url = menu_links['List of Proclaimed Offenders']
    filename = file_url.split('/')[-1]
    download_files([file_url], OUTPUT_DIR, session)
    convert_into_csv([filename], OUTPUT_DIR)
    delete_files([os.path.join(OUTPUT_DIR, filename)])
    filename = os.path.join(OUTPUT_DIR, filename.replace('pdf', 'csv'))
    output_filename = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    os.rename(filename, output_filename)
    alias = {
         'Name': 'Name of the\rCompany',
         'AddedDate': 'Date of\rorder of the\rCourt'
    }
    write_to_db(conn, output_filename, SOURCE, alias)
