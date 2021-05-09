#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://www.msei.in/investors/list-of-arbitrators'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'sfio-convicted.csv'

def main(conn):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
    table = soup.find('table', {'class' : 'table-striped'})
    file_urls = []
    for row in table.find_all('tr')[1:]:
        for col in row.find_all('td'):
            if col.find('a'):
                file_urls.append(col.find('a')['href'])

    filenames = list(download_files(file_urls, OUTPUT_DIR).keys())
    convert_into_csv(filenames=filenames, output_dir=OUTPUT_DIR)
    delete_files([os.path.join(OUTPUT_DIR, filename) for filename in filenames])

    #TODO: write global csv after preprocessing the csvs in bad format and merging them

