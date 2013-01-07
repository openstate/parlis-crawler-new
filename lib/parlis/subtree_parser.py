import datetime
import logging

from lxml import etree
import requests

from .utils import date_to_parlis_str

logger = logging.getLogger(__name__)


# subtree parser simply parses atom file, returns list of urls to fetch
class ParlisSubtreeParser(object):
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

    def parse(self, entity, contents):
        urls = {} # hash of relation => url

        if not self.subtree_filters.has_key(entity):
            return urls # if no filter was found, then no subtree parsing!

        try:
            tree = etree.fromstring(contents)
        except etree.XMLSyntaxError, e:
            logger.exception("XML file for %s failed to parse the subtree" % (entity, ))
            tree = None

        if tree is None:
            return []

        for entry in tree.iterfind('.//{http://www.w3.org/2005/Atom}entry'):
            base = entry.find('.//{http://www.w3.org/2005/Atom}id')
            if base is None:
                continue

            base_url = base.text
            SID = base_url.split('\'')[1]
            logger.info("Subtree parsing for %s, found a new SID : %s", entity, SID)

            for relation in self.subtree_filters[entity]:
                urls[(SID, relation)] = u'%s/%s' % (base_url, relation)

        return urls