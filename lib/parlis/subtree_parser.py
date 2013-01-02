import datetime
import logging

from lxml import etree
import requests

from .utils import date_to_parlis_str

logger = logging.getLogger(__name__)


# subtree parser simply parses atom file, returns list of urls to fetch
class ParlisSubtreeParser(object):
    filename = None
    entity = None

    subtree_filters = {
        'Zaken': [
            'ZaakActoren',
            'Statussen',
            'KamerstukDossier',
            'Documenten',
            'Activiteiten',
            'Besluiten',
            'GerelateerdVanuit',
            'GerelateerdNaar',
            'HoofdOverig',
            'GerelateerdOverig',
            'VervangenVanuit',
            'VervangenDoor',
            'Agendapunten'
        ],
        'Activiteiten': [
            'ActiviteitActoren',
            'Agendapunten',
            'Documenten',
            'Zaken',
            'VoortgezetVanuit',
            'VoortgezetIn',
            'VervangenVanuit',
            'VervangenDoor',
            'Reserveringen'
        ]
    }

    def __init__(self, filename, entity):
        self.filename = filename
        self.entity = entity

    def parse(self):
        urls = {} # hash of relation => url

        if not self.subtree_filters.has_key(self.entity):
            return urls # if no filter was found, then no subtree parsing!

        tree = etree.parse(filename)
        for elem in tree.iterfind('.//{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}id'):
            base_url = elem.text
            for relation in self.subtree_filters[self.entity]:
                urls[relation] = u'%s/%s' % (base_url, relation)

        return urls