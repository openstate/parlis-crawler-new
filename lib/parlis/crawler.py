import datetime
import logging

from .api import ParlisAPI
from .cache import ParlisFileCache
from .subtree_parser import ParlisSubtreeParser
from .parser import ParlisParser
from .formatter import ParlisTSVFormatter
from .compressor import ParlisZipCompressor
from .utils import get_dates, entity_to_singular

logger = logging.getLogger(__name__)


class ParlisCrawler(object):
    entity = 'Zaken'
    attribute = 'GewijzigdOp'
    start_date = None
    end_date = None

    def __init__(self, entity='Zaken', attribute='GewijzigdOp', start_date=datetime.datetime.now().date(), end_date=datetime.datetime.now().date()):
        self.entity = entity
        self.attribute = attribute
        self.start_date = start_date
        self.end_date = end_date

    def run(self):
        cache = ParlisFileCache('.', '')
        api = ParlisAPI('SOS', 'Open2012', cache)

        for current_date in get_dates(self.start_date, self.end_date):
            current_end_date = current_date + datetime.timedelta(days=1)
            cache.date_str = str(current_date)
            entity_count = 0
            last_items_fetched = 250
            file_list = []

            while (last_items_fetched >= 250):
                logger.info(
                    'Going to fetch data for %s, filtered by %s on %s, skipping %s items',
                    self.entity, self.attribute, current_date, entity_count
                )

                contents = api.fetch_recent(
                    self.entity,
                    None,
                    entity_count,
                    self.attribute,
                    current_date,
                    current_end_date
                )

                entity_properties, entities = ParlisParser(
                    contents, self.entity, None
                ).parse()

                file_name = ParlisTSVFormatter(entity_properties).format(
                    entities,
                    self.entity,
                    None,
                    'output/%s' % (current_date, )
                )
                if file_name is not None:
                    file_list.append(file_name)

                # last_items_fetched = len(entities)
                last_items_fetched = contents.count('<entry>')
                entity_count += last_items_fetched
                logging.info("Parsed %s items, skipped %s items", last_items_fetched, entity_count)

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

                    file_name = ParlisTSVFormatter(relation_properties).format(
                        relation_entities,
                        self.entity,
                        relation,
                        'output/%s' % (current_date, )
                    )
                    if file_name is not None:
                        file_list.append(file_name)

            compressor = ParlisZipCompressor()
            compressor.compress('output/%s-%s.zip' % (current_date, self.entity), list(set(file_list)))

        logger.info('Crawling ended, fetched %s urls ..', api.num_requests)

