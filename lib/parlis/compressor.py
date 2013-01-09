import sys
import os
import re
import logging
from zipfile import ZipFile

logger = logging.getLogger(__name__)


class ParlisBaseCompressor(object):
    def compress(self, file_name, file_list):
        raise NotImplementedError


class ParlisZipCompressor(ParlisBaseCompressor):
    def compress(self, file_name, file_list):
        logger.info("Compressing %s (%s)", file_name, file_list)

        with ZipFile(file_name, 'w') as zip_file:
            for tsv_file in file_list:
                zip_file.write(tsv_file)
