#!/usr/bin/python
#-*- coding: utf-8 -*-

from utils import *

PARENT_SOURCE = 'https://www.mcxindia.com'
SOURCE = 'https://www.mcxindia.com/membership/notice-board/notice-board-disciplinary-action'
OUTPUT_DIR = os.path.join(os.getcwd(), 'files')
OUTPUT_FILE = 'mcx-action-ap.csv'

def main():
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
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

    file_url = links['Disciplinary Action taken against Authorised Persons']
    filenames = list(download_files(file_urls=[file_url], output_dir=OUTPUT_DIR).keys())
    convert_into_csv(filenames, OUTPUT_DIR)
    delete_files([os.path.join(OUTPUT_DIR, filename) for filename in filenames])
    os.rename(os.path.join(OUTPUT_DIR, filenames[0].replace('pdf', 'csv')),
              os.path.join(OUTPUT_DIR, OUTPUT_FILE))
    
    alias = {
        'PAN': 'PAN',
        'Name': 'Name and address of the AP',
        'AddedDate': 'Date of withdrawal of approval'
    }
    write_global_csv(filename=os.path.join(OUTPUT_DIR, OUTPUT_FILE), source=SOURCE, alias=alias)

if __name__ == '__main__':
    main()
