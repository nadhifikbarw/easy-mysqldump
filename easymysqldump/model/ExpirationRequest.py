from easymysqldump.model import BaseModel
from easymysqldump.model import BackupLog


class ExpirationRequest(BaseModel):
    def __init__(self, filename: str):
        self.filename = filename

    @classmethod
    def from_log(cls, log: BackupLog):
        return cls(log.filename)
