#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

PARENT_SOURCE = 'http://www.mca.gov.in'
SOURCE = 'http://www.mca.gov.in/MinistryV2/defaulterdirectorslist.html'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'mca-director-defaulter-list.csv'

def main():
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
    file_urls = [PARENT_SOURCE + a['href'] for a in soup.find_all('a') if a.text.startswith('Link to view')]
    filenames = download_files(file_urls=file_urls, output_dir=OUTPUT_DIR).keys()
    convert_into_csv(filenames=filenames, output_dir=OUTPUT_DIR, ext='pdf')
    write_added_date(filenames=filenames)
    delete_files(filenames)
    filenames = [filename.replace('pdf', 'csv') for filename in filenames]
    merge_csvs(filenames=filenames, output_filename=os.path.join(OUTPUT_DIR, OUTPUT_FILE))
    delete_files(filenames)

    alias = {
        'Name': 'Name',
        'AddedDate': 'AddedDate'
    }
    write_global_csv(filename=os.path.join(OUTPUT_DIR, OUTPUT_FILE), source=SOURCE, alias=alias)

if __name__ == '__main__':
    main()
