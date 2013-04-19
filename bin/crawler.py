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
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib')))

import parlis

help_message = '''
Usage: crawer.py [-p <path>] [-a <attribute>] [-f <from_date>] [-t <till_date>] [-F]
'''

#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    verbose = False
    entity = 'Zaken'
    attribute = 'GewijzigdOp'
    start_date = datetime.datetime.now().date()
    #end_date = (datetime.datetime.now() + datetime.timedelta(days=1)).date()
    end_date = datetime.datetime.now().date()
    force = False
    fetch_all = False
    numeric_level = logging.DEBUG #logging.INFO
    force_cache = False

    if argv is None:
        argv = sys.argv

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "he:a:f:t:vFAC", ["help", "entity=", "attribute=", "from=", "till=", "force", "all", "log=", "cache"])
        except getopt.error, msg:
            raise Usage(msg)

        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-e", "--entity"):
                entity = value #.capitalize()
            if option in ("-a", "--attribute"):
                attribute = value
            if option in ("-f", "--from"):
                start_date = datetime.datetime.strptime(value, '%Y-%m-%d').date()
            if option in ("-t", "--till"):
                end_date = datetime.datetime.strptime(value, '%Y-%m-%d').date()
            if option in ("-F", "--force"):
                force = True
            if option in ("-A", "--all"):
                fetch_all = True
            if option in ("-C", "--cache"):
                force_cache = True
            if option in ("--log"):
                numeric_level = getattr(logging, value.upper(), None)
                if not isinstance(numeric_level, int):
                    raise ValueError('Invalid log level: %s' % value)

        logging.basicConfig(level=numeric_level)
        logger.debug('Starting up ...')
        parlis_crawler = parlis.ParlisCrawler(
            entity, attribute, start_date, end_date, force, force_cache, fetch_all
        )
        parlis_crawler.run()

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
