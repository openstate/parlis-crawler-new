import sys
import os
import re
import logging

from lxml import etree

from .utils import extract_sid_from_url

logger = logging.getLogger(__name__)

class ParlisParser(object):
    properties = []
    tree = None

    entity_properties = {}

    def __init__(self, contents, entity, relation = None, extra_properties = []):
        try:
            self.tree = etree.fromstring(contents)
        except etree.XMLSyntaxError, e:
            logger.exception("XML file for %s failed to parse" % (entity, ))
            self.tree = None

        if self.tree is None:
            return

        if relation is not None:
            property_entity = relation
        else:
            property_entity = entity

        if self.entity_properties.has_key(property_entity):
            self.properties = self.entity_properties(property_entity)
        else:
            property_set = self.tree.find(
                './/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'
            )
            if property_set is not None:
                self.properties = [x.tag.split('}')[1] for x in property_set.getchildren()] + extra_properties
            else:
                self.properties = extra_properties

        logger.debug("Parsed properties for %s, found the following : %s", property_entity, u','.join(self.properties))

    def parse(self, extra_attributes = {}):
        # initialize on new parsing :P
        data = []

        if self.tree is None:
            return ([], [])

        entries = [e for e in self.tree.iterfind('.//{http://www.w3.org/2005/Atom}entry')]
        if (len(entries) == 0) and (self.tree.tag == '{http://www.w3.org/2005/Atom}entry'):
            entries = [self.tree]
        for entry in entries:
            SID = entry.find('.//{http://www.w3.org/2005/Atom}id')
            if SID is None:
                continue

            SID = extract_sid_from_url(SID.text)
            logger.debug("Parsing, found a new SID : %s", SID)

            subtree = entry.find(
                './/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'
            )

            row = {}

            for item_prop in self.properties:
                attribuut = subtree.find(
                    './/{http://schemas.microsoft.com/ado/2007/08/dataservices}' + item_prop
                )
                if attribuut is not None and attribuut.text is not None:
                    row[item_prop] = attribuut.text
                else:
                    row[item_prop] = None

            for attr in extra_attributes:
                row[attr] = extra_attributes[attr]
            row['SID'] = SID

            data.append(row.copy())

        return (self.properties, data)
