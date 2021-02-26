#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://sfio.nic.in/'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'sfio-proclaimed-offenders.csv'

def main():
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
    menu_links = {link.text : link.get('href') for link in soup.find_all('a', class_='menu__link')}
    file_url = menu_links['List of Proclaimed Offenders']
    filename = file_url.split('/')[-1]
    download_files(file_urls=[file_url], output_dir=OUTPUT_DIR)
    convert_into_csv(filenames=[filename], output_dir=OUTPUT_DIR)
    delete_files([os.path.join(OUTPUT_DIR, filename)])
    filename = os.path.join(OUTPUT_DIR, filename.replace('pdf', 'csv'))
    output_filename = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    os.rename(filename, output_filename)
    alias = {
         'Name': 'Name of the\rCompany',
         'AddedDate': 'Date of\rorder of the\rCourt'
    }
    write_global_csv(filename=output_filename, source=SOURCE, alias=alias)

if __name__ == '__main__':
    main()