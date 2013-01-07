import sys
import os
import re
import logging
import codecs

from .utils import tsv_escape, makedirs


logger = logging.getLogger(__name__)


class ParlisBaseFormatter(object):
    properties = []

    def __init__(self, properties):
        self.properties = properties

    def format(self, rows, entity, relation=None):
        raise NotImplementedError

        
class ParlisTSVFormatter(ParlisBaseFormatter):
    def format(self, rows, entity, relation=None, path='.'):
        makedirs(path)

        if relation is not None:
            filename = '%s/%s_%s.tsv' % (path, entity, relation)
        else:
            filename = '%s/%s.tsv' % (path, entity)
        
        if not os.path.isfile(filename):
            f = codecs.open(filename, 'w', 'utf-8')
            f.write(u"\t".join(self.properties) + "\n")
        else:
            f = codecs.open(filename, 'a', 'utf-8')

        for row in rows:
            logger.info('Formatting a row for SID : %s', row['SID'])
            row_items = []
            for item_prop in self.properties:
                if not row.has_key(item_prop):
                    val = None
                else:
                    val = row[item_prop]
                row_items.append(tsv_escape(val))
            f.write(u"\t".join(row_items) + "\n")

        f.close()