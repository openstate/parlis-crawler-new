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
            cache.date_str = str(current_date)
            logger.info('Going to fetch data for %s, filtered by %s on %s', self.entity, self.attribute, current_date)
            contents = api.fetch_recent(self.entity, None, 0, self.attribute, self.start_date, self.end_date)

			entity_properties, entities = ParlisParser(contents, self.entity, None).parse()

			ParlisTSVFormatter(entity_properties).format(entities, self.entity, None)

            # fetch the subtree, if necessary
            subtree_parser = ParlisSubtreeParser()
            urls = subtree_parser.parse(self.entity, contents)
            for relation in urls:
                relation_contents = api.get_request(urls[relation], {}, self.entity, relation)

				relation_properties, relation_entities = ParlisParser(relation_contents, self.entity, relation).parse()

				ParlisTSVFormatter(relation_properties).format(relation_entities, self.entity, relation)
