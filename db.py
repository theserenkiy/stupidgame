import sqlite3

class DB:
    def __init__(self,name):
        self.dataBase = sqlite3.connect(f"db/{name}.db", check_same_thread=False)
        self.cursor = self.dataBase.cursor()
        with open(f"sql/{name}.sql") as c:
            self.execute(c.read())

    def execute(self, command, vars=[]):
        self.cursor.execute(command, vars)
        self.dataBase.commit()
        return self.cursor.fetchall()
    

__all__ = DB