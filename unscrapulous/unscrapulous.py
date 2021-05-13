#!/usr/bin/python
#-*- coding: utf-8 -*-

from importlib import import_module
from unscrapulous.utils import *

import argparse
import concurrent.futures
import psycopg2
import threading
import time
import toml

thread_local = threading.local()
conn = None

def get_session():
    if not hasattr(thread_local, 'session'):
        thread_local.session = req.Session()
    return thread_local.session

def scrape(scraper):
    mod = import_module(f'unscrapulous.{scraper}')
    mod.main(conn, get_session())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='Path to the config file', default='config.toml')

    args = parser.parse_args()
    config_path = args.config
    config = toml.load(config_path)

    # Create table
    global conn
    conn = psycopg2.connect(**config['postgresql_conn'])
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS unscrupulous_entities(
            ID SERIAL PRIMARY KEY,
            PAN text,
            Name text,
            AddedDate text,
            Source text,
            Meta text
        )
    """)

    scrapers = [f for f in config['scrapers'] if config['scrapers'][f]]
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(scrape, scrapers)
    end = time.time()

    print(f'Process completed in {end - start} seconds')

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
