#!/usr/bin/python
#-*- coding: utf-8 -*-

from utils import *

SOURCE = 'https://www.nseindia.com/regulations/exchange-defaulting-clients'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'nse-regulatory-defaulting-clients.csv'

def main():
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
    file_url = soup.find('a', {'class' : 'file'})['href']
    filename = file_url.split('/')[-1]
    download_files(file_urls=[file_url], output_dir=OUTPUT_DIR)
    convert_into_csv(filenames=[filename], output_dir=OUTPUT_DIR, ext='xlsx')
    os.rename(os.path.join(OUTPUT_DIR, filename.replace('xlsx', 'csv')), os.path.join(OUTPUT_DIR, OUTPUT_FILE))
    delete_files([os.path.join(OUTPUT_DIR, filename)])

    alias = {
        'PAN': 'Pan of Client ',
        'Name': 'Name of the Defaulting client ',
        'AddedDate': 'Date of Order / Award '
    }
    write_global_csv(filename=os.path.join(OUTPUT_DIR, OUTPUT_FILE), source=SOURCE, alias=alias)


if __name__ == '__main__':
    main()