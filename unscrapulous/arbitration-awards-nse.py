#!/usr/bin/python
#-*- coding: utf-8 -*-

from utils import *

SOURCE = 'https://www1.nseindia.com/invest/dynaContent/arbitration_award.jsp?requestPage=main&qryFlag=yes'
OUTPUT_DIR = os.path.join(os.getcwd(), 'files')
OUTPUT_FILE = 'arbitration-awards-nse.csv'

def main():
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
    table = get_table(soup, {'class' : 'tabular_data'})
    convert_into_csv(filenames=[OUTPUT_FILE], output_dir=OUTPUT_DIR, table=table)

    # TODO: download data from range of 1 year and paginate
    # write_global_csv() is behaving different here. Need to fix
    # alias = {
    #     'Name': 'Name of the Applicant',
    #     'AddedDate': 'Date of Arbitration Award'
    # }
    # write_global_csv(filename=os.path.join(OUTPUT_DIR, OUTPUT_FILE), source=SOURCE, alias=alias)


if __name__ == '__main__':
    main()
