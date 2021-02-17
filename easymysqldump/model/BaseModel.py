from datetime import datetime

class BaseModel:
    @staticmethod
    def to_datetime(iso_date_string: str):
        return datetime.fromisoformat(iso_date_string)
    
    @staticmethod
    def to_iso(date_time: datetime) -> str:
        return date_time.isoformat()