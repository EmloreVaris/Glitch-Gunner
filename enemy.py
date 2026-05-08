import sqlite3

class Enemy:
    def __init__(self, eid: int) -> None:
        self.eid = eid
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM enemies WHERE id = ?", (self.eid,))
        data = cursor.fetchone()
        raise NotImplementedError("Finish Enemy __init__() bro.")
