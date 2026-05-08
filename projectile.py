class Projectile:
    def __init__(self, pid: int, vel: tuple[int, int], pos: tuple[int, int]) -> None:
        self.pid = pid
        self.vel = vel
        self.pos = pos