#!/usr/bin/python
#-*- coding: utf-8 -*-

import tabula

FILENAME = 'DisqualifiedDirectorsAhmedabadSearchable_02072020.pdf'

def main():
    tables = tabula.read_pdf(FILENAME, pages='all', multiple_tables=True)
    print(type(tables))
    #print(tables)
    #tabula.convert_into(FILENAME, 'out.csv', pages='all')

if __name__ == '__main__':
    main()
