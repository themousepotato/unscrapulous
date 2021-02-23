#!/usr/bin/python
#-*- coding: utf-8 -*-

from utils import *
import os
import shutil

SOURCE = 'https://www.nseindia.com/regulations/member-sebi-debarred-entities'
OUTPUT_DIR = os.path.join(os.getcwd(), 'files/sebi-debarred-nse')
OUTPUT_FILE = 'sebi-debarred-nse.csv'

def main():
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
    file_url = soup.find('a', {'class' : 'file--mime-application-vnd-ms-excel'})['href']
    file_sources = download_files([file_url], OUTPUT_DIR)
    filenames = list(file_sources.keys())
    convert_into_csv(filenames=filenames, output_dir=OUTPUT_DIR, ext='xls')

    filename = os.path.join(OUTPUT_DIR, filenames[0].replace('xls', 'csv'))
    out_filename = os.path.join(os.getcwd(), 'files', OUTPUT_FILE)
    shutil.move(filename, out_filename)
    alias = {
        'PAN': 'PAN',
        'Name': 'Entity / Individual Name',
        'AddedDate': 'Order Date'
    }
    write_global_csv(filename=out_filename, source=SOURCE, alias=alias, fillna=True)
    shutil.rmtree(OUTPUT_DIR)

if __name__ == '__main__':
    main()