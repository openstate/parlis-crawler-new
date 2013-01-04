import datetime
import logging

import requests

from .utils import date_to_parlis_str

logger = logging.getLogger(__name__)


class ParlisAPI(object):
    username = None
    password = None
    # no slash at the end!
    base_url = 'https://api.tweedekamer.nl/APIDataService/v1'
    cache = None

    def __init__(self, username, passwd, cache=None):
        self.username = username
        self.password = password
        self.cache = cache

    def get_request(self, url, params={}, entity=None, relation=None):
        is_hit = (self.cache is not None) and self.cache.hit(entity, relation, url, params)
        contents = u''

        if not is_hit:
            logger.info('Now fetching URL : %s', url)
            result = requests.get(
                url,
                params=params,
                verify=False,
                auth=(self.username, self.password)
            )

            if self.cache is not None:
                self.cache.store(result, entity, relation, url, params)

            contents = result.text
        else:
            contents = self.cache.load(entity, relation, url, params)

        return contents

    def post_request(self, url, params={}, data={}, entity=None, relation=None):
        pass

    def _fetch(self, entity, relation = None, skip=0, filter=None):
        params = {
            '$skip': skip
        }

        if filter is not None:
            params['$filter'] = filter

        return self.get_request(
            '%s/%s/' % (self.base_url, entity),
            params=params,
            entity=entity,
            relation=relation
        )

    def fetch_recent(self, entity, relation=None, skip=0, attribute='GewijzijgdOp', start_date=datetime.datetime.now().date(), end_date=datetime.datetime.now().date()):
        date_filter = "%s ge datetime'%s' and %s le datetime'%s'" % (
            attribute,
            date_to_parlis_str(start_date),
            attribute,
            date_to_parlis_str(end_date)
        )

        return self._fetch(entity, relation, skip, date_filter)
