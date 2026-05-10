import pygame
import random
from random import randint
from projectile import Projectile
from enemydata import enemy_data, enemy_colors
from const import PLAYER_SIZE_X, PLAYER_SIZE_Y, SCREEN_WIDTH, SCREEN_HEIGHT

class Enemy:
    def __init__(self, eid: int, pos: tuple[float, float]) -> None:
        self.eid = eid
        self.pos = pos
        self.health = enemy_data[eid]["health"]
        self.dmg = enemy_data[eid]["damage"]
        self.speed = enemy_data[eid]["speed"]
        self.exp = (enemy_data[eid]["drops"] - enemy_data[eid]["variance"], enemy_data[eid]["drops"] + enemy_data[eid]["variance"])
        self.size = (enemy_data[eid]["sizex"], enemy_data[eid]["sizey"])
        self.color = enemy_colors[enemy_data[eid]["color"]]
        if random.random() >= .5:
            self.pos = (random.randint(0, 1) * (SCREEN_WIDTH + self.size[0]) - self.size[0] / 2, pos[1])
        else:
            self.pos = (self.pos[0], random.randint(0, 1) * (SCREEN_HEIGHT + self.size[1]) - self.size[1] / 2)

    def kill(self, enemies: list["Enemy"]) -> int:
        exp = randint(self.exp[0], self.exp[1])
        enemies.remove(self)
        return exp

    def display(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (20, 20, 20), (self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2 - 20, self.size[0], 10), border_radius=7)
        pygame.draw.rect(screen, (20 + round(130 * ((enemy_data[self.eid]["health"] - self.health) / enemy_data[self.eid]["health"])), 150 - round(130 * ((enemy_data[self.eid]["health"] - self.health) / enemy_data[self.eid]["health"]) // 1), 20), (self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2 - 20, self.size[0] / (enemy_data[self.eid]["health"] / self.health), 10), border_radius=7)
        pygame.draw.rect(screen, self.color, (self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2, self.size[0], self.size[1]), border_radius=7)
    
    def damage(self, damage: float, enemies: list["Enemy"]) -> int:
        self.health -= damage
        if self.health <= 0:
            return self.kill(enemies)
        return 0

    def hit_by_bullet(self, projectile: Projectile) -> bool:
        return self.pos[0] - self.size[0] / 2 <= projectile.pos[0] <= self.pos[0] + self.size[0] / 2 and self.pos[1] - self.size[1] / 2 <= projectile.pos[1] <= self.pos[1] + self.size[1] / 2

    def move(self, player_pos: tuple[float, float]) -> tuple[float, float]:
        diffx = self.pos[0] - player_pos[0]
        diffy = player_pos[1] - self.pos[1]
        if diffx == 0 and diffy == 0:
            return self.pos
        if diffx == 0:
            self.pos = (self.pos[0], self.pos[1] + diffy / abs(diffy) * self.speed)
        elif diffy == 0:
            self.pos = (self.pos[0] - diffx / abs(diffx), self.pos[1])
        else:
            self.pos = (self.pos[0] - diffx / (abs(diffx) + abs(diffy)) * self.speed, self.pos[1] + diffy / (abs(diffx) + abs(diffy)) * self.speed)
        return self.pos

    def touching_player(self, player_pos: tuple[float, float]) -> bool:
        return (self.pos[0] - self.size[0] / 2 < player_pos[0] + PLAYER_SIZE_X / 2) and (self.pos[0] + self.size[0] / 2 > player_pos[0] - PLAYER_SIZE_X / 2) and (self.pos[1] - self.size[1] / 2 < player_pos[1] + PLAYER_SIZE_Y / 2) and (self.pos[1] + self.size[1] / 2 > player_pos[1] - PLAYER_SIZE_Y / 2)