import datetime
import logging

from lxml import etree
import requests

from .utils import date_to_parlis_str

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
            return []

        for entry in tree.iterfind('.//{http://www.w3.org/2005/Atom}entry'):
            base = entry.find('.//{http://www.w3.org/2005/Atom}id')
            if base is None:
                continue

            base_url = base.text
            # FIXME: Reserveringen has a number, not a GUID with ' around them :/
            SID = base_url.split('\'')[1]
            logger.info("Subtree parsing for %s, found a new SID : %s", entity, SID)

            # <link rel="http://schemas.microsoft.com/ado/2007/08/dataservices/related/ZaakActoren"
            # type="application/atom+xml;type=feed" title="ZaakActoren" 
            # href="Zaken(guid'aec25db9-e037-44a6-8ace-001e313952dd')/ZaakActoren" />
            for link in entry.iterfind('.//{http://www.w3.org/2005/Atom}link'):
                if not link.get('rel').startswith('http://schemas.microsoft.com/ado/2007/08/dataservices/related/'):
                    continue
                if not link.get('type') == u'application/atom+xml;type=feed':
                    continue
                relation = link.get('title')
                urls[(SID, relation)] = u'%s/%s' % (base_url, relation)

        return urls