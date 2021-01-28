#!/usr/bin/python
#-*- coding: utf-8 -*-

from utils import *
import csv
import os
import pandas as pd
import shutil

SOURCE = 'https://www.nseindia.com/regulations/member-sebi-debarred-entities'
OUTPUT_DIR = os.path.join(os.getcwd(), 'files/sebi-debarred-nse')
OUTPUT_FILE = 'files/sebi-debarred-nse.csv'

def main():
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
    file_url = soup.find('a', {'class' : 'file--mime-application-vnd-ms-excel'})['href']
    file_sources = download_files([file_url], OUTPUT_DIR)
    filenames = list(file_sources.keys())
    convert_into_csv(filenames=filenames, output_dir=OUTPUT_DIR, ext='xls')

    filename = os.path.join(OUTPUT_DIR, filenames[0].replace('xls', 'csv'))
    df = pd.read_csv(filename, sep=',', dtype=object, error_bad_lines=False)
    df.fillna(method='ffill', inplace=True)
    out_df = pd.DataFrame(columns=['PAN', 'Name', 'AddedDate', 'Source', 'Meta'])
    out_df['PAN'] = df['PAN']
    out_df['Name'] = df['Entity / Individual Name']
    out_df['AddedDate'] = df['Order Date']
    out_df['Source'] = SOURCE
    out_df['Meta'] = pd.Series(df.to_json(orient ='records', lines=True).split('\n'))
    out_df.to_csv(OUTPUT_FILE, sep=',', encoding='utf-8', index=None)

    shutil.rmtree(OUTPUT_DIR)

if __name__ == '__main__':
    main()