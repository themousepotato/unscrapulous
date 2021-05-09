#!/usr/bin/python
#-*- coding: utf-8 -*-

from unscrapulous.utils import *

SOURCE = 'https://ncdex.com/suspended_member/latest_info'
OUTPUT_DIR = '/tmp/unscrapulous/files'
OUTPUT_FILE = 'ncdex-suspended-defaulted-expelled-debarred-members.csv'

FORM_DATA = {
    "draw":"2",
    "columns[0][data]":"title",
    "columns[0][name]":"",
    "columns[0][searchable]":"true",
    "columns[0][orderable]":"true",
    "columns[0][search][value]":"",
    "columns[0][search][regex]":"false",
    "columns[1][data]":"file",
    "columns[1][name]":"",
    "columns[1][searchable]":"true",
    "columns[1][orderable]":"false",
    "columns[1][search][value]":"",
    "columns[1][search][regex]":"false",
    "order[0][column]":"0",
    "order[0][dir]":"asc",
    "start":"0",
    "length":"10",
    "search[value]":"",
    "search[regex]":"false",
    "_token":"LGoJVR5H8oYGT4rtp17wfTwf4MiVjvIhDXA43iV5"
}
COOKIES = {
    "_ga":"GA1.2.115752129.1610379486",
    "_gid":"GA1.2.1896960417.1614161517",
    "ncdex_session":"eyJpdiI6IlkwSkUxQjhsclBLNU9SVGpTMVRtOXc9PSIsInZhbHVlIjoiTzRDSEIwSFRqNTZaaWhNRFVJR1pncFBxTjk1dWxkNnlod2pVNUMzZlVQRDBacE5cL0tBbUMyaXpoWXRnUWdZWTUiLCJtYWMiOiJiY2U0NTQ1ZjdiNzUzNTdmYmRlNDk5YzRkMzM0NzU1MTI2YTVlMDAwM2FjNWY2NmQzYmRhYWQxZDE3ZjY4MWE0In0=",
    "XSRF-TOKEN":"eyJpdiI6Im50dXpaM045OGJmbVwvWWkwNjVtbkh3PT0iLCJ2YWx1ZSI6IlJFYzIzSVJqZHpHcWd1ejRUQ2FOeXNPNzRFR0hqenNXVFkxdnpORDJubDA2YUpXQWdja2ZPRWZYdzNMRlBya3YiLCJtYWMiOiI5OTQ3NDBhZjhmZDRiYTA5MTQ3MzEyZDA2M2UxMzI0Mzg2ODFkYzlhYWM1ZmMzMzdlMWNlOTNhZWVlNzVmNWExIn0="
}

def main(conn):
    create_dir(OUTPUT_DIR)
    soup = get_soup(SOURCE)
    rjson = get_json_response(source=SOURCE, data=FORM_DATA, cookies=COOKIES)
    a = rjson['data'][0]['file']
    soup = BeautifulSoup(a, 'lxml')
    file_url = soup.find('a')['href']
    filenames = list(download_files(file_urls=[file_url], output_dir=OUTPUT_DIR).keys())
    convert_into_csv(filenames=filenames, output_dir=OUTPUT_DIR)
    delete_files(filenames)
    os.rename(os.path.join(OUTPUT_DIR, filenames[0].replace('pdf', 'csv')),
              os.path.join(OUTPUT_DIR, OUTPUT_FILE))

    #TODO: write global csv after preprocessing the csv in bad format

