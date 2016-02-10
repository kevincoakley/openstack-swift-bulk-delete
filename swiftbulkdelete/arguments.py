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

    parser.add_argument("-t",
                        metavar="threads",
                        dest="threads",
                        help="Concurrent Threads",
                        default=1,
                        required=False)

    parser.add_argument('--debug',
                        dest="debug",
                        action='store_true')

    return vars(parser.parse_args())
