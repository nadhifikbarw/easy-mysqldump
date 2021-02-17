import sqlite3
from pathlib import Path
from .DBState import DBState
from easymysqldump import DatabaseClosedException


class DB:
    STATE = DBState

    def __init__(self, connection: Path):
        self.connection_state = DB.STATE.OPEN
        self._sqlite3conn: sqlite3.Connection = sqlite3.connect(connection)
        self._cursor: sqlite3.Cursor = self._sqlite3conn.cursor()

    def is_open(self) -> bool:
        return self.connection_state == DB.STATE.OPEN

    def is_closed(self) -> bool:
        return not self.is_open

    @property
    def cursor(self) -> sqlite3.Cursor:
        if self.is_open():
            return self._cursor
        else:
            raise DatabaseClosedException()

    def commit(self) -> None:
        self._sqlite3conn.commit()

    def close(self) -> None:
        if self.is_open():
            self._cursor = None
            self._sqlite3conn.close()
            self.connection_state = DB.STATE.CLOSED
