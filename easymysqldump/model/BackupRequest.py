from datetime import datetime
from datetime import timedelta
from easymysqldump.model import BaseModel
from easymysqldump.model import BackupPolicy

class BackupRequest(BaseModel):
    def __init__(self, db_name: str, tbl_names: str, file_suffix:str, options: str, retention_timeout: int):
        self.db_name = db_name
        self.tbl_names = tbl_names if isinstance(tbl_names, str) else ""
        self.options = options if isinstance(options, str) else ""
        self.suffix = file_suffix if isinstance(file_suffix, str) else ""
        self.timeout = retention_timeout
        self.time = None
        self.expiration = None
        self.refresh()

    def refresh(self):
        self.time = datetime.now()
        self.expiration = self.time + timedelta(seconds=self.timeout)
        return self

    @property
    def filename(self):
        name =  f"{self.time.isoformat()}_{self.db_name}"
        return f"{name}_{self.suffix}.sql" if self.suffix else f"{name}.sql" 

    @classmethod
    def from_policy(cls, policy: BackupPolicy):
        return cls(policy.db_name, policy.tbl_names, policy.file_suffix, policy.options, policy.retention_timeout)       