from easymysqldump.service import DB
from easymysqldump.model import BackupPolicy
from easymysqldump.model import BackupLog


class MetadataDB(DB):

    def get_active_policies(self) -> list:
        self.cursor.execute("SELECT * FROM backup_policy WHERE active=1")
        return [BackupPolicy.from_query(policy) for policy in self.cursor.fetchall()]

    def get_active_logs(self) -> list:
        self.cursor.execute("SELECT * FROM backup_log WHERE is_expired=0")
        return [BackupLog.from_query(log) for log in self.cursor.fetchall()]

    def add_log(self, log: BackupLog) -> None:
        flat_log = log.flatten()
        self.cursor.execute("INSERT INTO backup_log VALUES (?,?,?,?,?,?,?)", flat_log)
        self.commit()

    def sync_log(self, log: BackupLog) -> None:
        flat_log = log.flatten_for_update()
        self.cursor.execute(f'''
            UPDATE backup_log
            SET log_id = ?,
                policy_id = ?,
                filename = ?,
                backup_at = ?,
                expired_at = ?,
                is_expired = ?,
                retention_action_status = ?
            WHERE log_id = ?
        ''', flat_log)
        self.commit()
