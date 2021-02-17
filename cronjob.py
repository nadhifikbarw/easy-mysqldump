#!/bin/bash
import os
import sys
import logging

from pathlib import Path
from easymysqldump import BackupLog
from easymysqldump import MetadataDB
from easymysqldump import BackupService


def main(settings):
    db = MetadataDB(Path(settings.DBPATH))
    logging.info(f"Metadata database connected")

    service = BackupService.from_settings(settings)

    # Backup Process
    logging.info(f"Begin backup routine")
    policies = db.get_active_policies()
    for policy in policies:
        logging.info(f"Creating backup for database: {policy.db_name}; policy_id: {policy.policy_id}")
        log = service.backup(policy)
        if isinstance(log, BackupLog):
            logging.info(f"Backup created, filename: {log.filename}")
            db.add_log(log)
        else:
            logging.error(
                f"Backup fail for policy: {policy.policy_id}, mysqldump error, check your credentials and make sure MySQL is running")

    logging.info(f"Backup routine finish")

    # Expiration Process
    logging.info(f"Begin expiration routine")
    logs = db.get_active_logs()
    for log in logs:
        if log.stale:
            logging.info(f"Expiring stale backup for {log.filename}")
            log = service.expire(log)
            if isinstance(log, BackupLog):
                logging.info(f"Expiration success: {log.filename}")
                db.sync_log(log)
            else:
                logging.error(f"Expiration failed: {log.filename}")
    logging.info(f"Expiration routine finished")
    logging.info(f"All routine finished")
    logging.info(f"Closing metadata connection")
    db.close()
    logging.info(f"Metadata database disconnected")


if __name__ == '__main__':
    #####################################
    #  Prerequisite checking and Setup  #
    #####################################

    # Set working directory
    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)
    os.chdir(dirname)

    # Logging
    os.makedirs("./logs", exist_ok=True)
    logging_time_fmt = '%Y:%m:%d:%H:%M:%S'
    logging_format = '[%(asctime)s] %(levelname)s %(message)s'
    logging.basicConfig(filename="logs/app.log", filemode='a+', datefmt=logging_time_fmt, format=logging_format,
                        level=logging.DEBUG)

    # Check settings
    settings_file = Path("./settings.py")
    if settings_file.is_file():
        import settings as AppSettings

        logging.info("AppSettings loaded")
        os.makedirs(Path(AppSettings.TARGET), exist_ok=True)
        logging.info(f"Output dir set to: {AppSettings.TARGET}")
    else:
        msg = "settings.py not found, please run install.sh settings"
        print(msg)
        logging.critical(msg)
        logging.shutdown()
        sys.exit(1)

    # Check metadata.db
    db_file = Path(AppSettings.DBPATH)
    if db_file.is_file():
        logging.info("Metadata Database found")
    else:
        msg = "Database file not found, please run install.sh db"
        print(msg)
        logging.critical(msg)
        logging.shutdown()
        sys.exit(1)

    #######################################
    #  Run Backup and Expiration Routine  #
    #######################################
    main(AppSettings)
    logging.shutdown()
    sys.exit(0)
