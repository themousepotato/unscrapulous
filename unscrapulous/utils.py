#!/usr/bin/python
#-*- coding: utf-8 -*-

import csv
import os
import PyPDF2 as pypdf
import pandas as pd
import psycopg2.extras
import requests as req
import tabula
import xml.etree.ElementTree as ET
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

req.packages.urllib3.disable_warnings()

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
            tabula.convert_into(
                filename,
                filename.replace(ext, 'csv'),
                lattice=True,
                pages='all'
            )

    elif ext in ['xls', 'xlsx']:
        for filename in filenames:
            filename = os.path.join(output_dir, filename)
            excel_file = pd.read_excel(filename)
            excel_file.to_csv(filename.replace(ext, 'csv'),
                              index=None,
                              header=True)

def create_dir(dirpath):
    '''
    Creates a directory if not exists
    '''
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

def delete_files(filenames):
    '''
    Deletes files from a list of paths
    '''
    for filename in filenames:
        os.remove(filename)

def download_files(file_urls, output_dir, session):
    '''
    Downloads all files from a list of `file_urls` and returns a mapping
    between filenames and the corresponding file_urls
    '''
    with session:
        file_sources = {}
        for file_url in file_urls:
            resp = session.get(file_url, headers=headers, verify=False)
            filename = os.path.join(output_dir, file_url.split('/')[-1]) # TODO: use regex
            if resp.status_code == 200:
                file_sources[filename] = file_url
                with open(filename, 'wb') as f:
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

def get_soup(source, session, method='GET', data={}, cookies={}, verify=False):
    '''
    Returns a `BeautifulSoup` object from request data
    '''
    with session:
        if method == 'GET':
            resp = session.get(
                source, data=data, headers=headers, cookies=cookies, verify=verify
            )
        elif method == 'POST':
            resp = session.post(
                source, data=data, headers=headers, cookies=cookies, verify=verify
            )

    html = resp.content
    soup = BeautifulSoup(html, 'lxml')

    return soup

def get_table(soup, attrs={}, header=[], omit_cols=[], from_xml=False):
    '''
    Finds table from `BeautifulSoup` object and returns a python list
    '''
    if from_xml:
        table = soup.find_all(attrs['xml_parent'])
        header = [th for th in get_xml_tags(str(table[0]))[1:] if th != 'value']
        out_rows = [header]
        for row in table:
            out_row = []
            for th in header:
                try:
                    col = row.find(th).text
                except AttributeError:
                    col = ''
                out_row.append(col)
            out_rows.append(out_row)
        return out_rows

    table = soup.find('table', attrs=attrs)
    out_rows = []
    i = 0
    if header:
        out_rows.append(header)
    else:
        header = table.find_all('th')
        header = [th for th in header if header.index(th) not in omit_cols]
        if header:
            out_rows.append([th.text for th in header])
            i = 1

    for row in table.find_all('tr')[i:]:
        out_row = []
        cols = row.find_all('td')
        for col in cols:
            if cols.index(col) not in omit_cols:
                out_row.append(col.text)
                if col.find('a'):
                    try:
                        out_row.append(col.find('a')['href'])
                    except KeyError:
                        pass

        # For MCX Secretaries Defaulter List
        if len(out_row) > 4 and out_row[4] == '\n\n\n\n':
            out_rows.append([out_row[0], out_row[1], out_row[2], out_row[3], out_row[5]])
        else:
            out_rows.append(out_row)

    return out_rows

def get_json_response(source, session, data={}, cookies={}, verify=False, method='POST'):
    '''
    Returns the `json` response of a request
    '''
    with session:
        if method == 'GET':
            resp = session.get(
                source, data=data, headers=headers, cookies=cookies, verify=verify
            )
        elif method == 'POST':
            resp = session.post(
                source, data=data, headers=headers, cookies=cookies, verify=verify
            )

    return resp.json()

def get_xml_tags(string):
    '''
    Returns all tags from the given xml string
    '''
    xml_tree = ET.fromstring(string)
    tags = [elem.tag for elem in xml_tree.iter()]

    return tags

def merge_csvs(filenames, output_filename, delete=False):
    '''
    Merges csv files with same format
    '''
    df = pd.concat((pd.read_csv(f, header=0) for f in filenames))
    df.to_csv(output_filename, sep=',', encoding='utf-8', index=None)

    if delete:
        delete_files(filenames)

def write_added_date(filenames):
    '''
    Writes `AddedDate` field to the csv files which tabula missed to parse from
    outside the table
    '''
    for filename in filenames:
        pdf_obj = open(filename, 'rb')
        pdf_reader = pypdf.PdfFileReader(pdf_obj)
        page_obj  = pdf_reader.getPage(0)
        date = page_obj.extractText().split()[2]
        csv_filename = filename.replace('pdf', 'csv')
        df = pd.read_csv(csv_filename)
        df = df.replace('\r', ' ', regex=True)
        df = df.replace('\n', ' ', regex=True)
        df['AddedDate'] = date
        df.to_csv(csv_filename, index=False)

def write_to_db(conn, filename, source, alias, fillna=False):
    '''
    Writes data to a Postgres DB with the following fields:
    1. PAN
    2. Name
    3. AddedDate - day of blacklisting according to the source
    4. Source
    5. Meta - a JSON encoded field of whatever fields each source provides
    '''
    df = pd.read_csv(filename, sep=',', dtype=object, error_bad_lines=False)
    df = df.replace('\r', ' ', regex=True)
    df = df.replace('\n', ' ', regex=True)
    df = df.replace(',', ' ')

    # Change columns to second row if first row is a single cell text
    # For ex: in SFIO convicted
    try:
        i = len(df.columns[~df.columns.str.contains('unnamed',case = False)])
        j = len(df.iloc[0][~df.iloc[0].str.contains('unnamed',case = False)])
        if j > i:
            df.columns = df.iloc[0]
            df = df.iloc[1:]
    except:
        pass

    # Remove multiple headers
    # For ex: in MCX Action AP
    df = df[df.ne(df.columns).any(1)]
    if alias:
        field = list(alias.values())[0]
        df = df[df[field] != field]

    if fillna:
        df.fillna(method='ffill', inplace=True)

    out_df = pd.DataFrame(columns=['PAN', 'Name', 'AddedDate', 'Source', 'Meta'])
    for k, v in alias.items():
        out_df[k] = df[v]

    out_df['Source'] = source
    out_df['Meta'] = pd.Series(df.to_json(orient ='records', lines=True).split('\n'))

    df_columns = list(out_df)
    columns = ','.join(df_columns)
    values = 'VALUES({})'.format(','.join(['%s' for _ in df_columns]))

    cur = conn.cursor()
    psycopg2.extras.execute_batch(
        cur,
        f'INSERT INTO unscrupulous_entities ({columns}) {values}',
        out_df.values
    )
    conn.commit()
    cur.close()

    delete_files([filename])
