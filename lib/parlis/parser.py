import sys
import os
import re
import logging

from lxml import etree

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
            properties_set = self.tree.iterfind(
                './/{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'
            )
            parsed_properties = extra_properties
            for property_set in properties_set:
                current_properties = [x.tag.split('}')[1] for x in property_set.getchildren()]
                parsed_properties  = list(set(parsed_properties + current_properties))
            self.properties = parsed_properties

        logger.info("Parsed properties for %s, found the following : %s", property_entity, u','.join(parsed_properties))

    def parse(self, extra_attributes = {}):
        # initialize on new parsing :P
        data = []

        if self.tree is None:
            return ([], [])

        for entry in self.tree.iterfind('.//{http://www.w3.org/2005/Atom}entry'):
            SID = entry.find('.//{http://www.w3.org/2005/Atom}id')
            if SID is None:
                continue

            SID = SID.text.split('\'')[1]
            logger.info("Parsing, found a new SID : %s", SID)

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

            row += extra_attributes
            row['SID'] = SID

            data.append(row.copy())

        return (self.properties, data)
