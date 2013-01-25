import os
from collections import defaultdict
import datetime
import logging

import iso8601

from .api import ParlisAPI
from .cache import ParlisFileCache, ParlisForceFileCache
from .subtree_parser import ParlisSubtreeParser
from .attachment_parser import ParlisAttachmentParser
from .parser import ParlisParser
from .formatter import ParlisTSVFormatter
from .compressor import ParlisZipCompressor
from .utils import get_dates, entity_to_singular, makedirs, date_to_parlis_str

logger = logging.getLogger(__name__)


class ParlisCrawler(object):
    entity = 'Zaken'
    attribute = 'GewijzigdOp'
    start_date = None
    end_date = None
    force = False
    fetch_all = False

    def __init__(self, entity='Zaken', attribute='GewijzigdOp', start_date=datetime.datetime.now().date(), end_date=datetime.datetime.now().date(), force=False, fetch_all=False):
        self.entity = entity
        self.attribute = attribute
        self.start_date = start_date
        self.end_date = end_date
        self.force = force
        self.fetch_all = fetch_all

    def _format_entities(self, entity, entity_properties, entities, relation = None, output_dir='output', order_field='GewijzigdOp'):
        ordered_entities = defaultdict(list)
        for unordered_entity in entities:
            if (order_field == u'GewijzigdOp') or (order_field == u'AangemaaktOp'):
                sort_entry = date_to_parlis_str(iso8601.parse_date(unordered_entity[order_field]))
            else:
                sort_entry = unordered_entity[order_field]
            ordered_entities[sort_entry].append(unordered_entity)

        file_names = []
        for entry in sorted(ordered_entities.keys()):
            file_name = ParlisTSVFormatter(entity_properties).format(
                ordered_entities[entry],
                entity,
                relation,
                '%s/%s' % (output_dir, entry, )
            )
            if file_name is not None:
                file_names.append(file_name)

        return file_names

    def _fetch_attachments(self, api, contents, current_date, entity, relation=None):
        file_list = []
        # fetch the attachments, if necessary
        attachment_parser = ParlisAttachmentParser()
        if relation is not None:
            entity_name = relation
        else:
            entity_name = entity

        attachments = attachment_parser.parse(entity_name, contents)
        if len(attachments) > 0:
            makedirs('output/Attachments')

        for attachment_SID in attachments:
            attachment_url = attachments[attachment_SID]
            attachment_file = 'output/Attachments/%s' % (
                attachment_SID
            )

            if not os.path.exists(attachment_file):
                response = api.get_request_response(
                    attachment_url, {}
                )
                with open(attachment_file, "wb") as att:
                    att.write(response.content)

            file_list.append(attachment_file)

        return file_list

    def run(self):
        if self.force:
            cache = ParlisForceFileCache('.', '')
        else:
            cache = ParlisFileCache('.', '')

        api = ParlisAPI('SOS', 'Open2012', cache, True)

        #for current_date in get_dates(self.start_date, self.end_date):
        for current_date in [self.start_date]:
            #current_end_date = current_date + datetime.timedelta(days=1)
            current_end_date = self.end_date + datetime.timedelta(days=1)
            print current_date, current_end_date
            cache.date_str = str(current_date)
            entity_count = 0
            last_items_fetched = 250
            file_list = []

            while (last_items_fetched >= 250):
                logger.debug(
                    'Going to fetch data for %s, filtered by %s on %s, skipping %s items',
                    self.entity, self.attribute, current_date, entity_count
                )

                if not self.fetch_all:
                    contents = api.fetch_recent(
                        self.entity,
                        None,
                        entity_count,
                        self.attribute,
                        current_date,
                        current_end_date,
                        True
                    )
                else:
                    contents = api.fetch_all(
                        self.entity,
                        None,
                        entity_count,
                        True
                    )

                entity_properties, entities = ParlisParser(
                    contents, self.entity, None
                ).parse()

                file_list += self._format_entities(
                    self.entity, entity_properties, entities, None, 'output', self.attribute
                )

                # last_items_fetched = len(entities)
                last_items_fetched = contents.count('<entry>')
                entity_count += last_items_fetched
                logging.debug("Parsed %s items, skipped %s items", last_items_fetched, entity_count)

                file_list = file_list + self._fetch_attachments(
                    api, contents, current_date, self.entity
                )

                # fetch the subtree, if necessary
                subtree_parser = ParlisSubtreeParser()
                urls = subtree_parser.parse(self.entity, contents)

                for SID, relation in urls:
                    #relation = urls[SID][0]
                    relation_url = urls[(SID, relation)]

                    # FIXME: only get subtree items that have changed on this date?
                    relation_contents = api.get_request(
                        relation_url, {}, self.entity, relation
                    )

                    parent_name = 'SID_%s' % (entity_to_singular(self.entity), )
                    extra_attributes = {parent_name: SID}

                    relation_properties, relation_entities = ParlisParser(
                        relation_contents, self.entity, relation, [parent_name]
                    ).parse(extra_attributes)

                    file_list += self._format_entities(
                        self.entity, relation_properties, relation_entities, relation, 'output', self.attribute
                    )
                    
                    # add attachments
                    file_list = file_list + self._fetch_attachments(
                        api, relation_contents, current_date, self.entity, relation
                    )
                    

            compressor = ParlisZipCompressor()
            compressor.compress('output/%s-%s.zip' % (current_date, self.entity), list(set(file_list)))

        logger.debug('Crawling ended, fetched %s urls ..', api.num_requests)

