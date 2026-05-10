import pygame

from projectiledata import projectile_data, projectile_colors

class Projectile:
    def __init__(self, pid: int, vel: tuple[float, float], pos: tuple[float, float]) -> None:
        self.pid = pid
        self.vel = vel
        self.pos = pos
        data = projectile_data[pid]
        self.speed = data["speed"]
        self.color = projectile_colors[data["color"]]
        self.size = data["size"]
        self.damage = data["damage"]
        #raise NotImplementedError("Finish Projectile __init__() bro.")

    def move(self, bspd: float) -> tuple[float, float]:
        self.pos = (self.pos[0] + self.vel[0] * self.speed * bspd, self.pos[1] + self.vel[1] * self.speed * bspd)
        return self.pos

    def display(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, self.pos, self.size)