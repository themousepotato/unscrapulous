#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://www.un.org/securitycouncil/content/un-sc-consolidated-list'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'unsc-consolidated-list.csv'

def main():
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
    file_url = [link['href'] for link in soup.find_all('a', {'class' : 'documentlinks uw-link-btn'}) if 'xml' in link['href']][0]
    soup = get_soup(file_url)
    filenames = [OUTPUT_FILE.replace('list','individuals'), OUTPUT_FILE.replace('list', 'entities')]
    for i, parent in enumerate(['individual', 'entity']):
        table = get_table(
            soup=soup,
            attrs={
                'xml_parent': parent
            },
            from_xml=True
        )
        convert_into_csv(filenames=[filenames[i]], output_dir=OUTPUT_DIR, table=table)

    filenames = [os.path.join(OUTPUT_DIR, filename) for filename in filenames]
    output_filename = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    merge_csvs(filenames=filenames, output_filename=output_filename)
    delete_files(filenames)
    alias = {
         'Name': 'first_name',
         'AddedDate': 'listed_on'
    }
    write_global_csv(filename=output_filename, source=SOURCE, alias=alias)

if __name__ == '__main__':
    main()