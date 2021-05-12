#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'http://office.incometaxindia.gov.in/administration/_layouts/15/inplview.aspx?List={5A26177B-D7A0-4251-843D-5E6C0B3C3DF2}&View={D8DD9754-8FD1-4D72-9908-727646E99CA0}&ViewCount=450&IsXslView=TRUE&IsCSR=TRUE&Paged=TRUE&p_ID='
FILE_URL = 'http://office.incometaxindia.gov.in/administration/Lists/Tax%20Defaulters/AllItems.aspx'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'income-tax-defaulters.csv'

def main(conn):
    out_rows = [
        ['Title',
         'Approval Status',
         'Address',
         'Father Name',
         'Date of Birth',
         'PAN',
         'Source of Incomeme',
         'Tax Arrear',
         'Year Prefix',
         'CMSID',
         'Category of Assessee',
         'Income Tax Authority',
         'Remarks',
         'Sort Order',
         'Active',
         'Modified',
         'Modified By']
    ]
    page = 0
    row_count = 30
    while True:
        first_item_row = page * row_count + 1
        resp = req.post(SOURCE + str(first_item_row))
        if resp.status_code != 200:
            break

        data = resp.json()
        
        for row in data['Row']:
            parent = BeautifulSoup(row['DITHtml'], 'lxml')
            parent = parent.find('div').text
            parent = parent.replace('<br>', '\n')
            income_tax_authority = BeautifulSoup(row['DITHtml2'], 'lxml')
            income_tax_authority = income_tax_authority.find('div').text
            income_tax_authority = income_tax_authority.replace('<br>', '\n')
            out_rows.append([
                row['Title'],
                row['_ModerationStatus'],
                row['Address'].replace('<br>', '\n'),
                parent, row['Date_x0020_of_x0020_Birth'],
                row['PAN'],
                row['Source_x0020_of_x0020_Income'],
                row['Tax_x0020_Arrear'],
                row['Year_x0020_Prefix'],
                row['CMSID'],
                row['Category_x0020_of_x0020_Assessee'],
                income_tax_authority,
                row['Remarks'],
                row['Sort_x0020_Order'],
                row['Active'],
                row['Modified'],
                row['Editor'][0]['title']
        ])
        page += 1

    convert_into_csv(filenames=[OUTPUT_FILE], output_dir=OUTPUT_DIR, table=out_rows)
    alias = {
        'PAN': 'PAN',
        'Name': 'Title',
        'AddedDate': 'Modified'
    }
    write_to_db(conn=conn, filename=os.path.join(OUTPUT_DIR, OUTPUT_FILE), source=FILE_URL, alias=alias)

