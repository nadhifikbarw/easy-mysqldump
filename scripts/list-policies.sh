#!/bin/bash

if [ -z $1 ]; then
    echo "Usage: $0 metadata_db_path"
else
    sqlite3 $1 "SELECT * FROM backup_policy"
fi