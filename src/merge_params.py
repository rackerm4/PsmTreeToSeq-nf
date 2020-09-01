import json
import argparse
import data_to_csv as dtc
import loader as cl
import os
import glob


def main():
    parser = argparse.ArgumentParser(description='Generate sample tree data under the protracted speciation model')
    parser.add_argument('--t', metavar='N', nargs='+', help='Incoming tree parameter')
    parser.add_argument('--s', metavar='N', nargs='+', help='Incoming tree parameter')
    parser.add_argument('--output')
    args = parser.parse_args()
    args.parser = parser

    config = cl.Loader(args.output)
    headers = config.load_headers()

    for i in args.s:
        file = i[:-14] + '_t_params.json'
        with open(file, 'r') as f:
            d = json.load(f)
        with open(i, 'r') as r:
            d2 = json.load(r)
        d.update(d2)
        dtc.write_params_to_txt(d, headers)


if __name__ == '__main__':
    main()
