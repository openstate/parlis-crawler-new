import sys
import os
import re
import logging
from zipfile import ZipFile, ZIP_DEFLATED

logger = logging.getLogger(__name__)


class ParlisBaseCompressor(object):
    def compress(self, file_name, file_list):
        raise NotImplementedError


class ParlisZipCompressor(ParlisBaseCompressor):
    def compress(self, file_name, file_list):
        logger.info("Compressing %s (%s)", file_name, file_list)

        with ZipFile(file_name, 'w', ZIP_DEFLATED) as zip_file:
            for tsv_file in file_list:
                # ugly hack to make subdirs in zip :/
                if tsv_filw.lower().find('attachment') >= 0:
                    zip_file.write(tsv_file, u'Attachments/%s' % (os.path.basename(tsv_file), ))
                else:
                    zip_file.write(tsv_file, os.path.basename(tsv_file))
