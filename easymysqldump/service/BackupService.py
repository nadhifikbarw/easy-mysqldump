import os
import subprocess
from pathlib import Path
from datetime import datetime
from easymysqldump.model import BackupLog
from easymysqldump.model import BackupPolicy
from easymysqldump.model import BackupRequest
from easymysqldump.model import ExpirationRequest
from easymysqldump import IllegalExpirationException
from easymysqldump.common import expand_resolve_path


class BackupService:

    def __init__(self, target: str, username: str, password: str, hostname: str = 'localhost', port: str = '3306'):
        self.target = target
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

    @classmethod
    def from_settings(cls, settings):
        return cls(
            target = expand_resolve_path(settings.TARGET),
            username = settings.MYSQL_USERNAME,
            password = settings.MYSQL_PASSWORD,
            hostname = settings.MYSQL_HOSTNAME,
            port = settings.MYSQL_PORT
        )

    # Backup Service
    @property
    def base_command(self):
        return f"mysqldump -h{self.hostname} -P{self.port} -u{self.username} -p{self.password}"

    @staticmethod
    def __run_command(command: str):
        return subprocess.call(command, shell=True, executable='/bin/bash')

    def __gen_target_path(self, filename: str):
        return f"{self.target}/{filename}"

    def __gen_backup_command(self, request: BackupRequest):
        target_path = self.__gen_target_path(request.filename)
        return f"{self.base_command} {request.options} {request.db_name} {request.tbl_names} --result-file={target_path} > /dev/null 2>&1"

    def backup(self, policy: BackupPolicy):
        request = BackupRequest.from_policy(policy)
        command = self.__gen_backup_command(request)
        status_code = self.__run_command(command)
        if status_code == 0:
            return BackupLog(None, policy.policy_id, request.filename, request.time, request.expiration, False, "")
        else:
            return status_code

    # Expiration Service
    def expire(self, log: BackupLog):
        if log.inserted:
            status = ""
            request = ExpirationRequest.from_log(log)
            target_path = Path(self.__gen_target_path(request.filename))
            # Check if exist
            if target_path.is_file():
                os.remove(target_path)
                status += "EXPIRATION OK"
            else:
                status += "EXPIRATION OK; DELETED PRIOR REQUEST"

            log.retention_action_status = status
            log.expired_at = datetime.now()
            log.is_expired = True
            return log
        else:
            raise IllegalExpirationException()
