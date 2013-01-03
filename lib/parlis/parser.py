import sys
import os
import re
import logging

logger = logging.getLogger(__name__)

class ParlisParser(object):
	properties = []
	data = []
	tree = None

	def __init__(self, contents, entity, relation = None):
		 try:
            self.tree = etree.fromstring(contents)
        except etree.XMLSyntaxError, e:
            logger.exception("XML file for %s failed to parse" % (entity, ))
            self.tree = None

		properties = tree.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties')
        if properties is not None:
            self.properties = [x.tag.split('}')[1] for x in properties.getchildren()]

	def parse(self):
		SID = tree.find('.//{http://www.w3.org/2005/Atom}id')
        if SID is None:
            continue

        SID = SID.text.split('\'')[1]
		for subtree in tree.iterfind('.//{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
			row = {
				'SID': SID
			}

			for item_prop in self.properties:
				attribuut = subtree.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices}'+item_prop)
				if attribuut is not None and attribuut.text is not None:
					row[item_prop] = attribuut.text
				else:
					row[item_prop] = None

			self.data.append(row)

			return (self.properties, self.data)
