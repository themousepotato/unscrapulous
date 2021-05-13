#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

PARENT_SOURCE = 'https://www.mcxindia.com'
SOURCE = 'https://www.mcxindia.com/membership/notice-board/notice-board-disciplinary-action'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'mcx-defaulter-members.csv'

def main(conn, session):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE, session)
    table = soup.find('table', {'class': 'table1'})
    out_rows = []
    for row in table.find_all('tr')[1:]:
        out_row = []
        for col in row.find_all('td'):
            if col.find('a'):
                link = PARENT_SOURCE + col.find('a')['href']
                link = link[:link.find('.pdf')+4]
                if link.endswith('pdf'):
                    out_row.append(link)
            else:
                out_row.append(col.text.replace('  ', '').replace('\n', ''))
        out_rows.append(out_row)

    links = {}
    for out_row in out_rows:
        try:
            links[out_row[0]] = out_row[1]
        except IndexError:
            pass

    file_url = links['List of Members declared Defaulters']
    filenames = list(download_files([file_url], OUTPUT_DIR, session).keys())
    convert_into_csv(filenames, OUTPUT_DIR)
    delete_files([os.path.join(OUTPUT_DIR, filename) for filename in filenames])
    os.rename(os.path.join(OUTPUT_DIR, filenames[0].replace('pdf', 'csv')),
              os.path.join(OUTPUT_DIR, OUTPUT_FILE))
    
    alias = {
        'PAN': 'PAN',
        'Name': 'Name and address of the Member',
        'AddedDate': 'Date of\rDeclaration'
    }
    write_to_db(conn, os.path.join(OUTPUT_DIR, OUTPUT_FILE), SOURCE, alias)
