import sqlite3

class Projectile:
    def __init__(self, pid: int, vel: tuple[int, int], pos: tuple[int, int]) -> None:
        self.pid = pid
        self.vel = vel
        self.pos = pos
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM projectiles WHERE id = ?", (self.pid,))
        data = cursor.fetchone()
