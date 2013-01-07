import datetime
import logging

from .api import ParlisAPI
from .cache import ParlisFileCache
from .subtree_parser import ParlisSubtreeParser
from .parser import ParlisParser
from .formatter import ParlisTSVFormatter
from .utils import get_dates

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

                ParlisTSVFormatter(entity_properties).format(
                    entities,
                    self.entity,
                    None,
                    'output/%s' % (current_date, )
                )

                # last_items_fetched = len(entities)
                last_items_fetched = contents.count('<entry>')
                entity_count += last_items_fetched

                # fetch the subtree, if necessary
                subtree_parser = ParlisSubtreeParser()
                urls = subtree_parser.parse(self.entity, contents)

                for SID in urls:
                    relation = urls[SID][0]
                    relation_url = urls[SID][1]
                    relation_contents = api.get_request(
                        relation_url, {}, self.entity, relation
                    )

                    parent_name = 'SID_%s' % (self.entity, )
                    relation_properties, relation_entities = ParlisParser(
                        relation_contents, self.entity, relation, [parent_name]
                    ).parse({parent_name: SID})

                    ParlisTSVFormatter(relation_properties).format(
                        relation_entities,
                        self.entity,
                        relation,
                        'output/%s' % (current_date, )
                    )

