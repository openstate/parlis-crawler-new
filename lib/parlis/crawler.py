import datetime
import logging

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
        for current_date in get_dates(self.start_date, self.end_date):
            logger.info('Going to fetch data for %s, filtered by %s on %s', self.entity, self.attribute, current_date)
