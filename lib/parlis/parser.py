import sys
import os
import re
import logging

from lxml import etree

logger = logging.getLogger(__name__)

class ParlisParser(object):
    properties = []
    data = []
    tree = None

    def __init__(self, contents, entity, relation = None, extra_properties = []):
        try:
            self.tree = etree.fromstring(contents)
        except etree.XMLSyntaxError, e:
            logger.exception("XML file for %s failed to parse" % (entity, ))
            self.tree = None

        properties = self.tree.find(
            './/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'
        )
        if properties is not None:
            self.properties = list(set(
                extra_properties + [x.tag.split('}')[1] for x in properties.getchildren()]
            ))

    def parse(self, extra_attributes = {}):
        for entry in self.tree.iterfind('.//{http://www.w3.org/2005/Atom}entry'):
            SID = entry.find('.//{http://www.w3.org/2005/Atom}id')
            if SID is None:
                continue

            SID = SID.text.split('\'')[1]
            logger.info('Parsing, found SID %s', SID)

            row = extra_attributes
            row['SID'] = SID

            for subtree in entry.iterfind(
                './/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'
            ):

                for item_prop in self.properties:
                    attribuut = subtree.find(
                        './/{http://schemas.microsoft.com/ado/2007/08/dataservices}' + item_prop
                    )
                    if attribuut is not None and attribuut.text is not None:
                        row[item_prop] = attribuut.text
                    else:
                        row[item_prop] = None

            self.data.append(row)

        return (self.properties, self.data)
