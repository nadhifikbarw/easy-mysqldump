from easymysqldump.model import BaseModel

class BackupPolicy(BaseModel):
    def __init__(self, policy_id: int, db_name: str, tbl_names: str, file_suffix: str, options: str, retention_timeout:int, active: bool):
        self.policy_id = policy_id
        self.db_name = db_name
        self.tbl_names = tbl_names
        self.file_suffix = file_suffix
        self.options = options
        self.retention_timeout = retention_timeout
        self.active = active

    @classmethod
    def from_query(cls, query: tuple):
        return cls(*query)