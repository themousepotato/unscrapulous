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

def convert_into_csv(filenames, output_dir, ext='pdf', table=[]):
    '''
    Converts `pdf/xls/xlsx` files to `csv`.
    Also writes a `csv` file from a list
    '''
    if len(table) != 0:
        for filename in filenames:
            filename = os.path.join(output_dir, filename)
            with open(filename, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(table)
        return

    if ext == 'pdf':
        for filename in filenames:
            filename = os.path.join(output_dir, filename)
            tabula.convert_into(filename, filename.replace(ext, 'csv'), pages='all')

    elif ext in ['xls', 'xlsx']:
        for filename in filenames:
            filename = os.path.join(output_dir, filename)
            excel_file = pd.read_excel(filename)
            excel_file.to_csv(filename.replace(ext, 'csv'),
                              index=None,
                              header=True)

def create_dir(dirpath):
    '''
    Create a directory if not exists
    '''
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

def download_files(file_urls, output_dir):
    '''
    Downloads all files from a list of `file_urls` and returns a mapping
    between filenames and the corresponding file_urls
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

def extract_zip(filename, output_dir):
    '''
    Extracts the zipfile and returns the paths of files it contains
    '''
    with zipfile.ZipFile(filename, 'r') as f:
        f.extractall(output_dir)
        paths = f.namelist()

    return paths

def get_soup(source, method='GET', data={}, cookies={}, verify=False):
    '''
    Returns a `BeautifulSoup` object from request data
    '''
    if method == 'GET':
        resp = req.get(source, data=data, headers=headers, cookies=cookies, verify=verify)
    elif method == 'POST':
        resp = req.post(source, data=data, headers=headers, cookies=cookies, verify=verify)

    html = resp.content
    soup = BeautifulSoup(html, 'lxml')

    return soup

def get_table(soup, attrs={}, header=[]):
    '''
    Finds table from `BeautifulSoup` object and returns a python list
    '''
    table = soup.find('table', attrs=attrs)
    out_rows = []
    i = 0
    if header:
        out_rows.append(header)
    else:
        header = table.find_all('th')
        if header:
            out_rows.append([th.text for th in header])
            i = 1

    for row in table.find_all('tr')[i:]:
        out_row = []
        for col in row.find_all('td'):
            out_row.append(col.text)
        out_rows.append(out_row)

    return out_rows

def get_json_response(source, data={}, cookies={}, verify=False):
    '''
    Returns the `json` response of a request
    '''
    resp = req.post(source, data=data, headers=headers, cookies=cookies, verify=verify)

    return resp.json()

def write_global_csv(filename, source, alias, fillna=False):
    '''
    Writes a csv file with the following global attributes:
    1. PAN
    2. Name
    3. AddedDate - day of blacklisting according to the source
    4. Source
    5. Meta - a JSON encoded field of whatever fields each source provides
    '''
    df = pd.read_csv(filename, sep=',', dtype=object, error_bad_lines=False)
    if fillna:
        df.fillna(method='ffill', inplace=True)

    out_df = pd.DataFrame(columns=['PAN', 'Name', 'AddedDate', 'Source', 'Meta'])
    for k, v in alias.items():
        out_df[k] = df[v]

    out_df['Source'] = source
    out_df['Meta'] = pd.Series(df.to_json(orient ='records', lines=True).split('\n'))
    out_df.to_csv(filename, sep=',', encoding='utf-8', index=None)
