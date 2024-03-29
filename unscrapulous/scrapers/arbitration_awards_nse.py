#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://www1.nseindia.com/invest/dynaContent/arbitration_award.jsp?requestPage=main&qryFlag=yes'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'arbitration-awards-nse.csv'

def main(conn, session):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE, session)
    table = get_table(
        soup,
        {
            'class' : 'tabular_data'
        }
    )
    convert_into_csv([OUTPUT_FILE], OUTPUT_DIR, table=table)

    # TODO: download data from range of 1 year and paginate
    # write_to_db() is behaving different here. Need to fix
    # alias = {
    #     'Name': 'Name of the Applicant',
    #     'AddedDate': 'Date of Arbitration Award'
    # }
    # write_to_db(conn, os.path.join(OUTPUT_DIR, OUTPUT_FILE), SOURCE, alias)
