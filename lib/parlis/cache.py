import os
import codecs

from .utils import make_md5, makedirs

class ParlisBaseCache(object):
    def hit(self, entity, relation, url, params={}):
        raise NotImplementedError

    def load(self, entity, relation, url, params={}):
        raise NotImplementedError

    def store(self, result, entity, relation, url, params={}):
        raise NotImplementedError


class ParlisFileCache(ParlisBaseCache):
    output_base_path = '.'
    date_str = None

    def __init__(self, output_base_path, date_str):
        self.output_base_path = output_base_path
        self.date_str = date_str

    def _get_dirs(self, entity, relation, url, params={}):
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

        return dirs

    def _get_filename(self, dirs, url, params={}):
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

    def hit(self, entity, relation, url, params={}):
        dirs = self._get_dirs(entity, relation, url, params)
        path = self._get_filename(dirs, url, params)
        logger.info('Checking for filename : %s', path)
        return os.path.isfile(path)

    def load(self, entity, relation, url, params={}):
        dirs = self._get_dirs(entity, relation, url, params)
        path = self._get_filename(dirs, url, params)
        
        logger.info('Now reading from cache file: %s', path)
        f = codecs.open(path, 'r', 'utf-8')
        text = f.read()
        f.close()

        return text

    def store(self, result, entity, relation, url, params={}):
        dirs = self._get_dirs(entity, relation, url, params)

        makedirs(dirs)

        path = self._get_filename(dirs, url, params)

        logger.info('Now storing into cache file: %s', path)
        f = codecs.open(path, 'w', 'utf-8')
        f.write(result.text)
        f.close()


class ParlisForceFileCache(ParlisFileCache):
    def hit(self, entity, relation, url, params={}):
        return False # always fetch urls, store into file
