#!/usr/bin/python
#-*- coding: utf-8 -*-

# Usage: ./unscrapulous.py --config=config.toml --output=results.csv

from subprocess import call
from utils import *

import argparse
import toml

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='Path to the config file', default='config.toml')
    parser.add_argument('--output', help='Path to the output csv file', default='output.csv')
    args = parser.parse_args()

    config_path = args.config
    output_filename = args.output

    config = toml.load(config_path)

    filenames = [f for f in config['scrapers'] if config['scrapers'][f]]
    for filename in filenames:
        call(['python', filename + '.py'])

    csv_files = [os.path.join('files', f) for f in os.listdir('files') if f.endswith('.csv')]
    merge_csvs(filenames=csv_files, output_filename=output_filename)

if __name__ == '__main__':
    main()