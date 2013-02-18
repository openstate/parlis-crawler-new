#!/bin/sh

PARLIS_CRAWLER_HOME=/home/breyten/parlis-crawler-new
PARLIS_HTDOCS_UPDATES=/mnt/projects/appsvoordemocratie/data/htdocs/updates
PARLIS_VIRTUAL_ENV=parlis_new

export WORKON_HOME=$HOME/.virtualenvs
source /usr/bin/virtualenvwrapper.sh

cd $PARLIS_CRAWLER_HOME
workon $PARLIS_VIRTUAL_ENV

YESTERDAY=`date -d yesterday '+%Y-%m-%d'`

for ENTITY in Zaken Stemmingen Besluiten Documenten Activiteiten Reserveringen KamerstukDossiers
do
  # Zaken
  echo "Downloading $ENTITY for $YESTERDAY"
  ./bin/crawler.py -e $ENTITY -f $YESTERDAY -t $YESTERDAY 2>>$PARLIS_CRAWLER_HOME/daily.err >>$PARLIS_CRAWLER_HOME/daily.log
done

cd "$PARLIS_CRAWLER_HOME/output"
find . -name '*.zip' -exec mv \{\} $PARLIS_HTDOCS_UPDATES \;

cd -


