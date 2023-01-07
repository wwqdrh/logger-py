import peewee


class SqliteDriver:
    def __init__(self, dbname: str):
        self._db = peewee.SqliteDatabase(dbname)

    @property
    def db(self) -> peewee.SqliteDatabase:
        return self._db
