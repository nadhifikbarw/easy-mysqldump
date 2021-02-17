from easymysqldump.model import BaseModel
from datetime import datetime


class BackupLog(BaseModel):
    def __init__(self, log_id: int or None, policy_id: int, filename: str, backup_at: datetime, expired_at: datetime,
                 is_expired: bool, retention_action_status: str, is_inserted=False):
        self.log_id = log_id
        self.policy_id = policy_id
        self.filename = filename
        self.backup_at = backup_at
        self.expired_at = expired_at
        self.is_expired = is_expired
        self.retention_action_status = retention_action_status
        self._is_inserted = is_inserted
        self._cast_sync()

    def _cast_sync(self) -> None:
        self.backup_at = self.backup_at if isinstance(self.backup_at, datetime) else self.to_datetime(self.backup_at)
        self.expired_at = self.expired_at if isinstance(self.expired_at, datetime) else self.to_datetime(
            self.expired_at)

    def flatten(self) -> tuple:
        return (
            self.log_id,
            self.policy_id,
            self.filename,
            self.to_iso(self.backup_at),
            self.to_iso(self.expired_at),
            self.is_expired,
            self.retention_action_status
        )

    def flatten_for_update(self) -> tuple:
        return (
            self.log_id,
            self.policy_id,
            self.filename,
            self.to_iso(self.backup_at),
            self.to_iso(self.expired_at),
            self.is_expired,
            self.retention_action_status,
            self.log_id
        )

    @property
    def inserted(self):
        return self._is_inserted == True

    @property
    def stale(self):
        return datetime.now() > self.expired_at

    @classmethod
    def from_query(cls, query: tuple):
        return cls(*query, is_inserted=True)
