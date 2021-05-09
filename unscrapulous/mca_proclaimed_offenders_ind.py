#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

PARENT_SOURCE = 'http://www.mca.gov.in'
SOURCE = 'http://www.mca.gov.in/MinistryV2/proclaimedoffenders.html'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'mca-proclaimed-offenders-ind.csv'

def main(conn):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
    links = [PARENT_SOURCE + a['href'] for a in soup.find_all('a', class_='links_black_EES')]
    file_urls = []
    for link in links:
        soup = get_soup(link)
        for a in soup.find_all('a', class_='links_black_EES'):
            file_urls.append(PARENT_SOURCE + a['href'])

    filenames = download_files(file_urls=file_urls, output_dir=OUTPUT_DIR).keys()
    # TODO: convert downloaded files to csv and write a global csv
    # Note that most of the files don't contain data in a readable format

