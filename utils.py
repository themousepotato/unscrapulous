#!/usr/bin/python
#-*- coding: utf-8 -*-

import csv
import os
import pandas as pd
import requests as req
import tabula
import zipfile

from bs4 import BeautifulSoup

headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
           'Upgrade-Insecure-Requests': '1',
           'DNT': '1',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'en-US,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate'
           }

def convert_into_csv(filenames, ext='pdf', table=[]):
    '''
    Converts `pdf/xls/xlsx` files to `csv`.
    Also writes a `csv` file from a list
    '''
    if ext == 'pdf':
        for filename in filenames:
            tabula.convert_into(filename, filename.replace(ext, 'csv'))

    else if ext in ['xls', 'xlsx']:
        for filename in filenames:
            excel_file = pd.read_excel(filename)
            excel_file.to_csv(filename.replace(ext, 'csv'),
                              index=None,
                              header=True)

    else if len(table) != 0:
        for filename in filenames:
            with open(filename, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(table)

def download_files(file_urls, output_dir):
    '''
    Downloads all files from a list of `file_urls`
    '''
    file_sources = {}
    for file_url in file_urls:
        resp = req.get(file_url, headers=headers, verify=False)
        filename = file_url.split('/')[-1] # TODO: use regex
        if resp.status_code == 200:
            file_sources[filename] = file_url
            with open(os.path.join(output_dir, filename), 'wb') as f:
                f.write(resp.content)

    return file_sources

def get_soup(source, data={}, cookies={}, verify=False):
    '''
    Returns a `BeautifulSoup` object from request data
    '''
    resp = req.get(source, data=data, headers=headers, cookies=cookies, verify=verify)
    html = resp.content
    soup = BeautifulSoup(html, 'lxml')

    return soup

def get_json_response(source, data={}, cookies={}, verify=False):
    '''
    Returns the `json` response of a request
    '''
    resp = req.post(source, data=data, headers=headers, cookies=cookies, verify=verify)

    return resp.json()
