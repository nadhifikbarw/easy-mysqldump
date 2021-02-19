# #!/bin/bash

# Defaults
HOSTNAME="localhost"
USER="root"
PORT=3306

# Print help message
printHelp() {
  echo "Usage: $0 [-u user] [-p password] [-P port] [-h hostname] [-e db_name1,db_name2,...] metadata_db_path"
  exit 2
}

# Check if options is valid
checkValid() {
  local VALID=1
  if [ -z "$HOSTNAME" ]; then
    VALID=0
  fi
  if [ -z "$USER" ]; then
    VALID=0
  fi
  if [ -z "$PORT" ] && [ "$PORT" -ne "$PORT" ]; then
    VALID=0
  fi
  if [ ! -f "$DBLOCATION" ]; then
    VALID=0
  fi
  if [ "$VALID" -eq 0 ]; then
    printHelp
  fi
}

# Check if connection provided is valid
checkConnection() {
  mysql $COMMAND_OPTS -e "SHOW DATABASES;" > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "MySQL connection invalid. Please provide correct credential"
    exit 2
  fi
}

# Helper function to populate script variable for building
# mysql command options
buildOption(){
  unset USER_OPT
  unset PASS_OPT
  unset HOST_OPT
  unset PORT_OPT
  USER_OPT="-u$USER"
  if [ -z "$PASSWORD" ]; then
    PASS_OPT=""
  else
    PASS_OPT="-p$PASSWORD"
  fi
  HOST_OPT="-h$HOSTNAME"
  PORT_OPT="-P$PORT"
}

# Chain all mysql options into one variable
buildOptions() {
  unset COMMAND_OPTS
  buildOption
  COMMAND_OPTS="$USER_OPT $PASS_OPT $HOST_OPT $PORT_OPT"
}

# Check MySQL

mysql --version > /dev/null 2>&1
if [ "$?" -ne 0 ]; then
  echo "Critical! mysql not found" 1>&2
fi

# Check sqlite3

sqlite3 --version > /dev/null 2>&1
if [ "$?" -ne 0 ]; then
  echo "Critical! sqlite3 not found" 1>&2
fi

# Parse script options
while getopts ":P:e:u:p:h" opt; do
  case $opt in
    P ) PORT=$OPTARG ;;
    e ) EXCEPTIONS=$OPTARG ;;
    u ) USER=$OPTARG ;;
    p ) PASSWORD=$OPTARG ;;
    \? ) printHelp ;;
    : ) printHelp ;;
  esac
done
shift "$(($OPTIND-1))"

# Get Metadata DB Location
DBLOCATION=$1

checkValid
buildOptions
checkConnection

# Main function
mysql $COMMAND_OPTS -BNe "SHOW DATABASES;" 2>/dev/null | \
while read DBNAME; do
  # Determine if db in exceptions
  unset ACTIVE
  if [ -n "$EXCEPTIONS" ] && [[ "$EXCEPTIONS" == *"$DBNAME"* ]]; then
    ACTIVE="0" # Disable
  else
    ACTIVE="1"
  fi

  # INSERT if not exist or UPDATE if exists
  unset STATUS
  STATUS=$(sqlite3 $DBLOCATION "SELECT active FROM backup_policy WHERE db_name='$DBNAME'" 2>/dev/null)
  if [ -n "$STATUS" ]; then
    sqlite3 $DBLOCATION "UPDATE backup_policy SET active=$ACTIVE WHERE db_name='$DBNAME'"
  else
    sqlite3 $DBLOCATION "INSERT INTO backup_policy(db_name, active) VALUES ('$DBNAME', $ACTIVE)"
  fi
done
