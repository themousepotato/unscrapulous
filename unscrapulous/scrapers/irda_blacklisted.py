#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *
import datetime

SOURCE = 'https://agencyportal.irdai.gov.in/PublicAccess/BlackListedAgent.aspx'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'irda-blacklisted.csv'

def main(conn):
    date = datetime.datetime.strftime(datetime.datetime.today(), '%d %b %Y')
    site_data = {
        'ctl00$ContentPlaceHolder1$txtStartDate': date,
        'ctl00$ContentPlaceHolder1$btnExport': 'Export'
    }
    params = ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTTARGET', '__EVENTARGUMENT', '__EVENTVALIDATION']

    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
    for param in params:
        site_data[param] = soup.find('input', attrs={'id': param})['value']
    soup = get_soup(SOURCE, method='POST', data=site_data)

    table = get_table(soup, {'id': 'ctl00_ContentPlaceHolder1_AgencyGrid'})
    convert_into_csv(filenames=[OUTPUT_FILE], output_dir=OUTPUT_DIR, table=table)

    alias = {
        'PAN': 'PAN',
        'Name': 'Agent Name',
        'AddedDate': 'Blacklisted date'
    }
    write_to_db(conn=conn, filename=os.path.join(OUTPUT_DIR, OUTPUT_FILE), source=SOURCE, alias=alias)

