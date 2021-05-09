#!/usr/bin/python
#-*- coding: utf-8 -*-

from importlib import import_module
from subprocess import call
from unscrapulous.utils import *

import argparse
import psycopg2
import toml

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='Path to the config file', default='config.toml')

    args = parser.parse_args()
    config_path = args.config
    config = toml.load(config_path)

    # Create table
    conn = psycopg2.connect(**config['postgresql_conn'])
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE unscrupulous_entities(
            PAN text,
            Name text,
            AddedDate text,
            Source text,
            Meta text
        )
    """)

    submodules = [f for f in config['scrapers'] if config['scrapers'][f]]
    for submodule in submodules:
        mod = import_module(f'unscrapulous.{submodule}')
        mod.main(conn)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
