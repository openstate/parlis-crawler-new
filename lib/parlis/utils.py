import sys
import os
import re
import errno
import datetime
import hashlib

SINGULAR_ENTITIES = {
    u'Activiteiten': u'Activiteit',
    u'ActiviteitActoren': u'ActiviteitActor',
    u'Agendapunten': u'Agendapunt',
    u'AgendapuntActoren': u'AgendapuntActor',
    u'Besluiten': u'Besluit',
    u'DocumentActoren': u'DocumentActor',
    u'Documenten': u'Document',
    u'DocumentVersies': u'DocumentVersie',
    u'KamerstukDossiers': u'KamerstukDossier',
    u'Statussen': u'Status',
    u'Stemmingen': u'Stemming',
    u'ZaakActiviteitBesluitSoorten': u'ZaakActiviteitBesluitSoort',
    u'ZaakActoren': u'ZaakActor',
    u'Zaken': u'Zaak',
    u'Reserveringen': u'Reservering',
    u'Zalen': u'Zaal'
}


def date_to_parlis_str(date):
    return date.strftime('%Y-%m-%d')

def make_md5(text):
    return hashlib.md5(text).hexdigest()

# from http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
def makedirs(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def get_dates(from_date, end_date):
    while from_date <= end_date:
        yield from_date
        from_date = from_date + datetime.timedelta(days=1)

def tsv_escape(text):
    if text is not None:
        return text.replace('\n', ' ').replace('\t', ' ').replace('\r', '')
    else:
        return u''

def entity_to_singular(entity):
    if SINGULAR_ENTITIES.has_key(entity):
        return SINGULAR_ENTITIES[entity]
    else:
        return entity

    return entity

def extract_sid_from_url(url):
    try:
        sid = url.split('\'')[1]
    except IndexError, e:
        sid = url.split('(')[1]
    return sid
