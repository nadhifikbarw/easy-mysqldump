from enum import Enum
from enum import unique as UniqueEnum


@UniqueEnum
class DBState(Enum):
    OPEN = 1
    CLOSED = 2
