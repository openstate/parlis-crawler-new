import sys
import os
import re
import datetime
import codecs

import requests

from .utils import date_to_parlis_str, make_md5, makedirs

class ParlisBaseCache(object):
    def cache(self, result, entity, relation, url, params = {}):
        raise NotImplementedError

class ParlisFileCache(ParlisBaseCache):
    output_base_path = '.'
    date_str = None

    def __init__(self, output_base_path, date_str):
        self.output_base_path = output_base_path
        self.date_str = date_str

    def cache(self, result, entity, relation, url, params = {}):
        if relation is not None:
            dirs = '%s/%s/%s/%s' % (
                self.output_base_path,
                self.date_str,
                entity,
                relation
            )
        else:
            dirs = '%s/%s/%s' % (
                self.output_base_path,
                self.date_str,
                entity
            )

        makedirs(dirs)

        if not params.has_key('$skip'):
            path = '%s/%s.xml' % (
                dirs,
                make_md5(url),
            )
        else:
            path = '%s/%s_%s.xml' % (
                dirs,
                make_md5(url),
                str(params['$skip'])
            )

        f = codecs.open(path, 'w', 'utf-8')
        f.write(result.text)
        f.close()

class ParlisAPI(object):
    username = None
    password = None
    base_url = 'https://api.tweedekamer.nl/APIDataService/v1' # no slash at the end
    cache = None

    def __init__(self, username, passwd, cache=None):
        self.username = username
        self.password = password
        self.cache = cache

    def _get_request(self, url, params={}, entity=None, relation=None):
        result = requests.get(
            url,
            params=params,
            verify=False,
            auth=(self.username, self.password)
        )

        if self.cache is not None:
            self.cache.cache(result, entity, relation, url, params)

        return result

    def _post_request(self, url, params={}, data={}, entity=None, relation=None):
        pass

    def _fetch(self, entity, relation = None, skip=0, filter=None):
        params = {
            '$skip': skip
        }

        if filter is not None:
            params['$filter'] = filter

        return self._get_request(
            '%s/%s/' % (self.base_url, entity),
            params=params,
            entity=entity,
            relation=relation
        )

    def _fetch_recent(self, entity, relation=None, skip=0, attribute='GewijzijgdOp', start_date=datetime.datetime.now().date(), end_date=datetime.datetime.now().date()):
        date_filter = "%s ge datetime'%s' and %s le datetime'%s'" % (
            attribute,
            date_to_parlis_str(start_date),
            attribute,
            date_to_parlis_str(end_date)
        )

        return self._fetch(entity, relation, skip, date_filter)
