#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *
import datetime

SOURCE = 'https://agencyportal.irdai.gov.in/PublicAccess/BlackListedAgent.aspx'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'irda-blacklisted.csv'

def main(conn, session):
    date = datetime.datetime.strftime(datetime.datetime.today(), '%d %b %Y')
    site_data = {
        'ctl00$ContentPlaceHolder1$txtStartDate': date,
        'ctl00$ContentPlaceHolder1$btnExport': 'Export'
    }
    params = ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTTARGET', '__EVENTARGUMENT', '__EVENTVALIDATION']

    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE, session)
    for param in params:
        site_data[param] = soup.find(
            'input',
            {
                'id': param
            }
        )['value']
    soup = get_soup(SOURCE, session, method='POST', data=site_data)

    table = get_table(
        soup,
        {
            'id': 'ctl00_ContentPlaceHolder1_AgencyGrid'
        }
    )
    convert_into_csv([OUTPUT_FILE], OUTPUT_DIR, table=table)

    alias = {
        'PAN': 'PAN',
        'Name': 'Agent Name',
        'AddedDate': 'Blacklisted date'
    }
    write_to_db(conn, os.path.join(OUTPUT_DIR, OUTPUT_FILE), SOURCE, alias)
