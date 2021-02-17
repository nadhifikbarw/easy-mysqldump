#!/bin/bash

CWD=$(dirname "$0")
COMMONFOLDER=$CWD/common
DATAFOLDER=$CWD/data

chksqlite() {
  sqlite3 --version >/dev/null 2>&1
  if [ "$?" -ne 0 ]; then
    echo "Fatal! sqlite3 not installed"
    exit 1
  fi
}

chkmysqldump() {
  mysqldump --version >/dev/null 2>&1
  if [ "$?" -ne 0 ]; then
    echo "Fatal! mysqldump not installed"
    exit 1
  fi
}

copydb() {
  cp $COMMONFOLDER/metadata.db $DATAFOLDER
}

installdb() {
  if [ -f $DATAFOLDER/metadata.db ]; then
    # Perform integrity check
    local BACKUPLOG=$(sqlite3 -line "$DATAFOLDER/metadata.db" '.table' | awk -F' ' '{print $1}')
    local BACKUPPOLICY=$(sqlite3 -line "$DATAFOLDER/metadata.db" '.table' | awk -F' ' '{print $2}')

    if [[ ! $BACKUPLOG -eq "backup_log" && ! $BACKUPPOLICY -eq "backup_policy" ]]; then
      copydb
    fi
  else
    copydb
  fi
  return 0
}

installsetting() {
  if [ ! -f $CWD/settings.py ]; then
    cp $CWD/settings.py.example $CWD/settings.py
    echo "Don't forget to edit 'settings.py' with appropriate configuation"
  fi
  return 0
}

check() {
  chksqlite
  chkmysqldump
}

main() {
  check
  installdb
  installsetting
}

COMMAND=$1
case $COMMAND in
db)
  check
  installdb
  ;;
settings)
  check
  installsetting
  ;;
*)
  main
  ;;
esac
exit 0
