from const import SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_MARGIN, FRICTION, SPEED
from downgrades import upgrades
import random
import pygame
import typing
import asyncio
class Player:
    def __init__(self) -> None:
        self.health = 100.0
        self.mhealth = 100
        self.energee = 20
        self.menergee = 20
        self.pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.vel = (0, 0)
        self.sizex = 70
        self.sizey = 100
        self.exp = 0
        self.lvl = 1
        self.upgrades: list[str] = []
        self.modifiers: dict[str, int] = {}
    def move(self) -> tuple[float, float]:
        if self.get("spd"):
            self.pos = (self.pos[0] + self.vel[0] * pow(1.05, self.get("spd")), self.pos[1] + self.vel[1] * pow(1.05, self.get("spd")))
        else:
            self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])
        if self.pos[0] < self.sizex / 2 + SCREEN_MARGIN:
            self.pos = (self.sizex / 2 + SCREEN_MARGIN, self.pos[1])
            self.vel = (0, self.vel[1])
        if self.pos[0] > SCREEN_WIDTH - self.sizex / 2 - SCREEN_MARGIN:
            self.pos = (SCREEN_WIDTH - self.sizex / 2 - SCREEN_MARGIN, self.pos[1])
            self.vel = (0, self.vel[1])
        if self.pos[1] < self.sizey / 2 + SCREEN_MARGIN:
            self.pos = (self.pos[0], self.sizey / 2 + SCREEN_MARGIN)
            self.vel = (self.vel[0], 0)
        if self.pos[1] > SCREEN_HEIGHT - self.sizey / 2 - SCREEN_MARGIN:
            self.pos = (self.pos[0], SCREEN_HEIGHT - self.sizey / 2 - SCREEN_MARGIN)
            self.vel = (self.vel[0], 0)
        return self.pos
    def slow(self) -> tuple[float, float]:
        self.vel = (self.vel[0] * FRICTION, self.vel[1] * FRICTION)
        return self.vel
    def apply_vel(self, direction: int) -> tuple[float, float]:
        if direction == 0:
            return self.vel
        elif direction < -2:
            self.vel = (self.vel[0] + SPEED, self.vel[1] + SPEED * (direction // -4))
        elif direction == -2:
            self.vel = (self.vel[0] + SPEED, self.vel[1] - SPEED)
        elif direction < 2:
            self.vel = (self.vel[0], self.vel[1] + -direction * SPEED)
        elif direction == 2:
            self.vel = (self.vel[0] - SPEED, self.vel[1] + SPEED)
        else:
            self.vel = (self.vel[0] - SPEED, self.vel[1] - SPEED * (direction // 4))
        return self.vel
    async def levelup(self, screen: pygame.Surface) -> None:
        level = 0
        while self.exp >= round(20 * pow(1.1, self.lvl - 1)):
            self.exp -= round(20 * pow(1.1, self.lvl - 1))
            level += 1
            self.lvl += 1
        self.lvl -= level
        for _ in range(level):
            pool: dict[str, dict[str, list[str]]] = {}
            for r in upgrades:
                if self.lvl in r:
                    for downgrade in upgrades[r]:
                        pool[downgrade] = upgrades[r][downgrade]
            downgrades: list[str] = [random.choice(list(pool.keys())) for _ in range(3)]
            upgrading = True
            while upgrading:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if SCREEN_WIDTH / 2 - 170 <= event.pos[0] <= SCREEN_WIDTH / 2 + 170 and SCREEN_HEIGHT / 2 - 70 <= event.pos[1] <= SCREEN_HEIGHT / 2 + 70:
                                pos = event.pos[0] - (SCREEN_WIDTH / 2 - 170)
                                self.upgrades.append(typing.cast(str, downgrades[round(pos // 120)]))
                                upgrading = False
                screen.fill((20, 20, 20))
                for index, d in enumerate(downgrades):
                    pygame.draw.rect(screen, (60, 60, 60), (SCREEN_WIDTH / 2 - 50 + (index - 1) * 120, SCREEN_HEIGHT / 2 - 70, 100, 140), border_radius=10)
                    font = pygame.font.SysFont("arial", 20)
                    name = d.split(" ")
                    line = name[0]
                    linenum = 0
                    name = name[1:]
                    while len(name) > 0:
                        line += " " + name[0]
                        if font.render(d, True, (165, 98, 204)).get_width() > 80:
                            line = line[:line.index(name[0]) - 1]
                            screen.blit(font.render(line, True, (165, 98, 204)), (SCREEN_WIDTH / 2 - 40 + (index - 1) * 120, SCREEN_HEIGHT / 2 - 60 + linenum * 25))
                            linenum += 1
                            line = name[0]
                        name = name[1:]
                    screen.blit(font.render(line, True, (165, 98, 204)), (SCREEN_WIDTH / 2 - 40 + (index - 1) * 120, SCREEN_HEIGHT / 2 - 60 + linenum * 25))
                pygame.display.update()
                await asyncio.sleep(0)
            self.lvl += 1
        self.recall()
    def recall(self) -> None:
        self.modifiers = {}
        modifiers: list[str] = []
        for upgrade in self.upgrades:
            for value in upgrades.values():
                if upgrade in value:
                    for v in value[upgrade]["benefit"]:
                        modifiers.append(v)
                    for v in value[upgrade]["detriment"]:
                        modifiers.append(v)
        for downgrade in modifiers:
            try:
                if downgrade[:downgrade.index("+")] not in self.modifiers:
                    self.modifiers[downgrade[:downgrade.index("+")]] = 0
                self.modifiers[downgrade[:downgrade.index("+")]] += downgrade.count("+")
            except ValueError:
                if downgrade[:downgrade.index("-")] not in self.modifiers:
                    self.modifiers[downgrade[:downgrade.index("-")]] = 0
                self.modifiers[downgrade[:downgrade.index("-")]] -= downgrade.count("-")
    def get(self, modifier: str) -> int:
        try:
            return self.modifiers[modifier]
        except:
            return 0