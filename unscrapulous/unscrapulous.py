#!/usr/bin/python
#-*- coding: utf-8 -*-

# Usage: ./unscrapulous.py --config=config.toml --output=results.csv

from subprocess import call
from importlib import import_module
from unscrapulous.utils import *

import argparse
import toml

OUTPUT_DIR = '/tmp/unscrapulous/files'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='Path to the config file', default='config.toml')
    parser.add_argument('--output', help='Path to the output csv file', default='output.csv')
    args = parser.parse_args()

    config_path = args.config
    output_filename = args.output

    config = toml.load(config_path)

    submodules = [f for f in config['scrapers'] if config['scrapers'][f]]
    for submodule in submodules:
        mod = import_module(f'unscrapulous.{submodule}')
        mod.main()

    csv_files = [os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR) if f.endswith('.csv')]
    merge_csvs(filenames=csv_files, output_filename=output_filename, delete=True)

if __name__ == '__main__':
    main()
