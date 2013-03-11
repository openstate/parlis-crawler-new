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
    def compress(self, file_name, all_file_list):
        logger.debug("Compressing %s (%s)", file_name, all_file_list)

        total_size = [os.path.getsize(f) for f in all_file_list]
        
        do_multi = total_size > 2000000000
        
        file_lists = [[]]
        size_count = 0
        for tsv_file in all_file_list:
            file_size = os.path.getsize(tsv_file)
            if (size_count + file_size) > 2000000000:
                file_lists.append([tsv_file])
                size_count = 0
            else:
                file_lists[-1].append(file_size)
            size_count += file_size

        file_count = 0
        orig_file_name = file_name
        for file_list in file_lists:
            if do_multi:
                file_name = orig_file_name.replace('.zip', '-%s.zip' % (file_count, ))
            with ZipFile(file_name, 'w', ZIP_DEFLATED) as zip_file:
                for tsv_file in file_list:
                    # ugly hack to make subdirs in zip :/
                    if tsv_file.lower().find('attachment') >= 0:
                        zip_file.write(tsv_file, u'Attachments/%s' % (os.path.basename(tsv_file), ))
                    else:
                        zip_file.write(tsv_file, os.path.basename(tsv_file))
            file_count += 1
