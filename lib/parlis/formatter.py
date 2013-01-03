import sys
import os
import re
import logging
import codecs

logger = logging.getLogger(__name__)


class ParlisBaseFormatter(object):
	properties = []

	def __init__(self, properties):
		self.properties = properties

	def format(self, rows, entity, relation=None):
		raise NotImplementedError

		
class ParlisTSVFormatter(ParlisBaseFormatter):
	def format(self, rows, entity, relation=None):
		# FIXME: date-based output path somehow?
		if relation is not None:
			filename = '%s_%s.tsv' % (entity, relation)
		else:
			filename = '%s.tsv' % (entity)
		
		if not os.path.isfile(filename):
			f = codecs.open(filename, 'w', 'utf-8')
			f.write(u"\t".join(self.properties) + "\n")
		else:
			f = codecs.open(filename, 'a', 'utf-8')

		for row in rows:
			row_items = [row[item_prop] for item_prop in self.properties]
			f.write(u"\t".join(row_items) + "\n"

		f.close()