#!/usr/bin/env python

import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-c",
                        metavar="container",
                        dest="container",
                        help="Container Name",
                        required=True)

    parser.add_argument("-l",
                        metavar="limit",
                        dest="limit",
                        help="Number of Objects to Delete per Operation",
                        required=True)

    parser.add_argument("-o",
                        metavar="offset_multiplier",
                        dest="offset_multiplier",
                        help="Offset Multiplier",
                        default=0,
                        required=False)

    return vars(parser.parse_args())
