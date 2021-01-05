#!/usr/bin/python
#-*- coding: utf-8 -*-

import json
import os
import pandas as pd
import requests
import tabula

# https://github.com/jmcarp/robobrowser/issues/93
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from robobrowser import RoboBrowser

from bs4 import BeautifulSoup

br = RoboBrowser(history=True,
                 user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
                 parser='lxml'
                 )


def main():
    # MCA Director Disqualified List
    PARENT_SOURCE = 'http://www.mca.gov.in'
    SOURCE = 'http://www.mca.gov.in/MinistryV2/disqualifieddirectorslist.html'

    br.open(SOURCE)
    html = br.response.content
    soup = BeautifulSoup(html, 'lxml')
    links = [a['href'] for a in soup.find_all('a', class_='links_black_EES')]
    file_sources = {}

    if not os.path.exists('files'):
        os.makedirs('files')

    # Download files
    for link in links:
        br.open(PARENT_SOURCE + link)
        html = br.response.content
        soup = BeautifulSoup(html, 'lxml')
        file_links = [a['href'] for a in soup.find_all('a', class_='links_black_EES')]
        for file_link in file_links:
            FILE_URL = PARENT_SOURCE + file_link
            FILENAME = file_link.split('/')[-1]
            br.open(FILE_URL)
            if br.response.status_code != 200:
                break
            file_sources[FILENAME] = FILE_URL
            with open(os.path.join('files', FILENAME), 'wb') as f:
                f.write(br.response.content)

    with open('files/file_sources.json', 'w') as f:
        json.dump(file_sources, f)

    # Parse from pdf files
    for filename in filenames:
        if filename.endswith('pdf'):
            tabula.convert_into(filename, filename.replace('pdf', 'csv'), pages='all')

    # Convert xlsx to csv
    for filename in filenames:
        for ext in ['xlsx', 'xls']:
            if filename.endswith(ext):
                excel_file = pd.read_excel(filename)
                excel_file.to_csv(filename.replace(ext, 'csv'),
                                  index=None,
                                  header=True)

if __name__ == '__main__':
    main()
