import sys
import os
import re
import logging
import codecs

from .utils import tsv_escape, makedirs


logger = logging.getLogger(__name__)


class ParlisBaseFormatter(object):
    properties = []

    def __init__(self, properties):
        self.properties = properties

    def format(self, rows, entity, relation=None):
        raise NotImplementedError

        
class ParlisTSVFormatter(ParlisBaseFormatter):
    fields = {
        'Activiteiten': [
            'Id',
            'Nummer',
            'Onderwerp',
            'Soort',
            'DatumSoort',
            'Aanvangstijd',
            'EindTijd',
            'Locatie',
            'Besloten',
            'Status',
            'Vergaderjaar',
            'Kamer',
            'Noot',
            'AangemaaktOp',
            'GewijzigdOp',
            'VRSNummer',
            'Voortouwnaam',
            'Voortouwafkorting',
            'Voortouwkortenaam'
        ],
        'ActiviteitActoren': [
            'Id',
            'Naam',
            'Functie',
            'Partij',
            'Relatie',
            'Spreektijd',
            'Volgorde',
            'AangemaaktOp',
            'GewijzigdOp'
        ],
        'Agendapunten': [
            'Id',
            'Nummer',
            'Onderwerp',
            'Aanvangstijd',
            'Eindtijd',
            'Volgorde',
            'Rubriek',
            'Noot',
            'Status',
            'AangemaaktOp',
            'GewijzigdOp'        
        ],
        'AgendapuntActoren': [
            'Id',
            'AgendapuntId',
            'Actor_SID',
            'Relatie',
            'ActorNaam',
            'ActorFunctie',
            'ActorPartij',
            'AangemaaktOp',
            'GewijzigdOp'        
        ],
        'Besluiten': [
            'Id',
            'Soort',
            'StemmingsSoort',
            'VoorstelText',
            'BesluitText',
            'AangemaaktOp',
            'GewijzigdOp',
            'Opmerking',
            'Status'
        ],
        'Documenten': [
            'Id',
            'DocumentNummer',
            'Titel',
            'Soort',
            'Onderwerp',
            'Datum',
            'Volgnummer',
            'Vergaderjaar',
            'Kamer',
            'AangemaaktOp',
            'GewijzigdOp',
            'Citeertitel',
            'Alias',
            'DatumRegistratie',
            'DatumOntvangst',
            'AanhangelNummer',
            'KenmerkAfzender',
            'ContentType'
        ],
        'DocumentActoren': [
            'Id',
            'DocumentId',
            'Naam',
            'Functie',
            'Partij',
            'Relatie',
            'AangemaaktOp',
            'GewijzigdOp'
        ],
        'DocumentVersies': [
            'Id',
            'DocumentId',
            'Status',
            'Versienummer',
            'Bestandsgrootte',
            'Extensie',
            'Datum',
            'AangemaaktOp',
            'GewijzigdOp'
        ],
        'KamerstukSossiers': [
            'Id',
            'Titel',
            'CiteerTitel',
            'Alias',
            'Nummer',
            'Toevoeging',
            'HoogsteVolgnummer',
            'Afgesloten',
            'Kamer',
            'AangemaaktOp',
            'GewijzigdOp'
        ],
        'Statussen': [
            'Id',
            'ZaakId',
            'BesluitId',
            'Soort',
            'Datum',
            'AangemaaktOp',
            'GewijzigdOp'
        ],
        'Stemmingen': [
            'Id',
            'Soort',
            'FractieGrootte',
            'FractieStemmen',
            'ActorNaam',
            'ActorPartij',
            'Vergissing',
            'AangemaaktOp',
            'GewijzigdOp',
            'SID_ActorLid',
            'SID_ActorFractie',
            'SID_Besluit'
        ],
        'Zaken': [
            'Id',
            'Nummer',
            'Soort',
            'Titel',
            'CiteerTitel',
            'Alias',
            'Status',
            'Onderwerp',
            'DatumStart',
            'Kamer',
            'GrondslagVoorhang',
            'Termijn',
            'Vergaderjaar',
            'Volgnummer',
            'HuidigeBehandelStatus',
            'Afgedaan',
            'GrootProject',
            'AangemaaktOp',
            'GewijzigdOp'
        ],
        'ZaakActoren': [
            'Id',
            'Naam',
            'Functie',
            'Partij',
            'Relatie',
            'AangemaaktOp',
            'GewijzigdOp',
            'ActorAbreviatedName'
        ]
    }

    def format(self, rows, entity, relation=None, path='.'):
        if len(rows) <= 0:
            return None
        
        makedirs(path)

        if relation is not None:
            filename = '%s/%s_%s.tsv' % (path, entity, relation)
        else:
            filename = '%s/%s.tsv' % (path, entity)
        
        if not os.path.isfile(filename):
            f = codecs.open(filename, 'w', 'utf-8')
            f.write(u"\t".join(self.properties) + "\n")
        else:
            f = codecs.open(filename, 'a', 'utf-8')

        #if relation is not None:
        #    entity_field = relation
        #else:
        #    entity_field = entity
        #if self.fields.has_key(entity_field):
        #    properties = self.fields[entity_field]
        #else:
        properties = self.properties

        for row in rows:
            logger.info('Formatting a row for SID : %s', row['SID'])
            row_items = []
            for item_prop in properties:
                if not row.has_key(item_prop):
                    val = None
                else:
                    val = row[item_prop]
                row_items.append(tsv_escape(val))
            f.write(u"\t".join(row_items) + "\n")

        f.close()

        return filename
