#!/usr/bin/env python
# encoding: utf-8
"""
crawler.py

Created by Breyten Ernsting on 2013-01-02.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import os
import sys
import getopt
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib')))

import parlis

help_message = '''
The help message goes here.
'''

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    logger.info('Starting up ...')

    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
