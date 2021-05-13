#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

PARENT_SOURCE = 'http://www.mca.gov.in'
SOURCE = 'http://www.mca.gov.in/MinistryV2/proclaimedoffenders.html'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'mca-proclaimed-offenders-ind.csv'

def main(conn, session):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE, session)
    links = [PARENT_SOURCE + a['href'] for a in soup.find_all('a', class_='links_black_EES')]
    file_urls = []
    for link in links:
        soup = get_soup(link, session)
        for a in soup.find_all('a', class_='links_black_EES'):
            file_urls.append(PARENT_SOURCE + a['href'])

    filenames = download_files(file_urls, OUTPUT_DIR, session).keys()
    # TODO: convert downloaded files to csv and write a global csv
    # Note that most of the files don't contain data in a readable format
