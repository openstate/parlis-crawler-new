import datetime
import logging
import urllib

import requests

from .utils import date_to_parlis_str

logger = logging.getLogger(__name__)


class ParlisAPI(object):
    username = None
    password = None
    # no slash at the end!
    base_url = 'https://api.tweedekamer.nl/APIDataService/v1'
    cache = None

    def __init__(self, username, password, cache=None):
        self.username = username
        self.password = password
        self.cache = cache

    def get_request(self, url, params={}, entity=None, relation=None):
        is_hit = (self.cache is not None) and self.cache.hit(entity, relation, url, params)
        contents = u''

        if not is_hit:
            real_url = '%s?' % (url, )

            # for some reason either the requests params parsing is too lenient,
            # (the requests params encding transforms $ into %24 and a space to +)
            # or the parlis param checking is too weak. Probably the latter, so
            # assemble url ourselves.
            if params.has_key('$filter'):
                real_url = real_url + '$filter=%s&' % (urllib.quote(params['$filter']), )
            if params.has_key('$skip'):
                real_url = real_url + '$skip=%s' % (params['$skip'], )

            logger.info('Now fetching URL : %s', real_url)
            result = requests.get(
                real_url,
            #    params=params,
                verify=False,
                auth=(self.username, self.password)
            )
            logger.info('Fetched URL : %s', result.url)

            if self.cache is not None:
                self.cache.store(result, entity, relation, url, params)

            contents = result.text
        else:
            contents = self.cache.load(entity, relation, url, params)

        return "\n".join(contents.split("\n")[1:])

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
