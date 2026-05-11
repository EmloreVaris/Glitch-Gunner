import pygame
from projectiledata import projectile_data, projectile_colors, projectile_effects
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
        self.ticks = 0
        self.effect = projectile_effects[data["effect"]]
    def move(self, bspd: float) -> tuple[float, float]:
        self.pos = (self.pos[0] + self.vel[0] * self.speed * bspd, self.pos[1] + self.vel[1] * self.speed * bspd)
        return self.pos
    def effects(self, projectiles: list["Projectile"]) -> bool:
        if self.effect == "none": return False
        if self.ticks >= 1:
            if self.effect == "split":
                projectiles.append(Projectile(self.pid - 1, (self.vel[0] - .1, self.vel[1] + .1), self.pos))
                projectiles.append(Projectile(self.pid - 1, (self.vel[0] + .1, self.vel[1] - .1), self.pos))
            return True
        self.ticks += 1
        return False
    def display(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, self.pos, self.size)