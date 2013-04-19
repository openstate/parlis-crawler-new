import datetime
import logging

from lxml import etree
import requests

from .utils import date_to_parlis_str, extract_sid_from_url

logger = logging.getLogger(__name__)


# subtree parser simply parses atom file, returns list of urls to fetch
class ParlisSubtreeParser(object):

    def parse(self, entity, contents):
        urls = {} # hash of relation => url

        try:
            tree = etree.fromstring(contents)
        except etree.XMLSyntaxError, e:
            logger.exception("XML file for %s failed to parse the subtree" % (entity, ))
            tree = None

        if tree is None:
            return {}

        for entry in tree.iterfind('.//{http://www.w3.org/2005/Atom}entry'):
            base = entry.find('.//{http://www.w3.org/2005/Atom}id')
            if base is None:
                continue

            base_url = base.text

            SID = extract_sid_from_url(base_url)
            logger.debug("Subtree parsing for %s, found a new SID : %s", entity, SID)

            # <link rel="http://schemas.microsoft.com/ado/2007/08/dataservices/related/ZaakActoren"
            # type="application/atom+xml;type=feed" title="ZaakActoren" 
            # href="Zaken(guid'aec25db9-e037-44a6-8ace-001e313952dd')/ZaakActoren" />
            # <link rel="http://schemas.microsoft.com/ado/2007/08/dataservices/related/KamerstukDossier" 
            # type="application/atom+xml;type=entry" title="KamerstukDossier"
            # href="Zaken(guid'b72a2b31-b662-4eab-a930-07d43d2e3a1d')/KamerstukDossier" />
            for link in entry.iterfind('.//{http://www.w3.org/2005/Atom}link'):
                if not link.get('rel').startswith('http://schemas.microsoft.com/ado/2007/08/dataservices/related/'):
                    continue
                if not (link.get('type') == u'application/atom+xml;type=feed' or link.get('type') == u'application/atom+xml;type=entry'):
                    continue
                relation = link.get('title')
                urls[(SID, relation)] = u'%s/%s' % (base_url, relation)

        return urls