#!/bin/sh

cd ..

# Zaken
./bin/crawler.py
# Stemmingen
./bin/crawler.py -e Stemmingen
# Besluiten
./bin/crawler.py -e Besluiten
# Documenten
./bin/crawler.py -e Documenten
# Activiteiten
./bin/crawler.py -e Activiteiten
# Reserveringen
./bin/crawler.py -e Reserveringen

# FIXME: copy/move resulting zip (and tsv?) somewhere decent

cd -


