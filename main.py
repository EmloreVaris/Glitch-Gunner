import pygame
import asyncio
import random
import time
from player import Player
from projectile import Projectile
from enemy import Enemy #type:ignore
from const import *
from enemydata import enemy_data
from projectiledata import projectile_data
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
async def main():
    highscore = 0
    running = True
    while running:
        title = True
        abilities = [f"ABILITY {i}" if random.random() > .5 else None for i in range(10)]
        projectiles: list[Projectile] = []
        player = Player()
        failed = 0
        enemies: list[Enemy] = []
        hit_cooldown = 0
        tick = 0
        tick_speed = round(random.random() * 51 + 10)
        trip_countdown = 0
        enemychances = [1 for _ in range(10)]
        while title and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SCREEN_WIDTH / 3 <= event.pos[0] <= SCREEN_WIDTH / 3 + 1000 and SCREEN_HEIGHT / 3 * 2 <= event.pos[1] <= SCREEN_HEIGHT / 3 * 2 + 70:
                        title = False
            screen.fill((122, 122, 122))
            pygame.draw.rect(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (random.randint(-SCREEN_WIDTH, SCREEN_WIDTH), random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT), random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
            text = pygame.font.SysFont("arial", 90).render("Glitch Gunner", True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH / 2 - text.get_width() / 2 - 5, SCREEN_HEIGHT / 2 - 50, text.get_width() + 10, 100))
            screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - 45))
            pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3 * 2, 1000, 70))
            text = pygame.font.SysFont("arial", 45).render("PLAY OR DON'T I doN't ReallY CaRE", True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            screen.blit(text, (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
            text = pygame.font.SysFont("arial", 145).render(f"Highscore: {highscore}", True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            screen.blit(text, (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
            pygame.display.update()
            clock.tick(60)
            await asyncio.sleep(0)
        gaming = True
        stime = time.time()
        while gaming and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        diffx = event.pos[0] - player.pos[0]
                        diffy = player.pos[1] - event.pos[1]
                        offset = 0
                        pid = 1
                        if player.get("blt"):
                            pid += player.get("blt")
                        if player.get("sprd"):
                            if player.get("sprd") > 0: offset = (random.random() * 2 - 1) * player.get("sprd") / 10
                        if diffx == 0 and diffy == 0:
                            pass
                        elif diffx == 0:
                            projectiles.append(Projectile(max(1, min(pid, max(projectile_data.keys()))), (0, -diffy / abs(diffy)), player.pos))
                        elif diffy == 0:
                            projectiles.append(Projectile(max(1, min(pid, max(projectile_data.keys()))), (diffx / abs(diffx), 0), player.pos))
                        else:
                            projectiles.append(Projectile(max(1, min(pid, max(projectile_data.keys()))), ((diffx + offset) / (abs(diffx) + abs(diffy) + offset), (-diffy + offset) / (abs(diffx) + abs(diffy) + offset)), player.pos))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP0: print(abilities[0])
                    if event.key == pygame.K_KP1: print(abilities[1])
                    if event.key == pygame.K_KP2: print(abilities[2])
                    if event.key == pygame.K_KP3: print(abilities[3])
                    if event.key == pygame.K_KP4: print(abilities[4])
                    if event.key == pygame.K_KP5: print(abilities[5])
                    if event.key == pygame.K_KP6: print(abilities[6])
                    if event.key == pygame.K_KP7: print(abilities[7])
                    if event.key == pygame.K_KP8: print(abilities[8])
                    if event.key == pygame.K_KP9: print(abilities[9])
            pressed = pygame.key.get_pressed()
            direction = 0
            if pressed[pygame.K_i]: direction += 1
            if pressed[pygame.K_r]: direction += 3
            if pressed[pygame.K_m]: direction -= 1
            if pressed[pygame.K_l]: direction -= 3
            if trip_countdown:
                trip_countdown -= 1
            else:
                player.apply_vel(direction)
                if player.get("trip"):
                    trip_countdown = tick_speed if random.random() * 100 < player.get('trip') / 5 else 0
            player.slow()
            screen.fill((0, 0, 0))
            player.move()
            for projectile in projectiles:
                projectile.display(screen)
                spd = 1
                if player.get("bspd"):
                    spd *= pow(1.05, player.get("bspd"))
                projectile.move(spd)
                if not 0 <= projectile.pos[0] <= SCREEN_WIDTH or not 0 <= projectile.pos[1] <= SCREEN_HEIGHT:
                    projectiles.remove(projectile)
                    continue
                if projectile.effects(projectiles):
                    projectiles.remove(projectile)
                    continue
                for enemy in enemies:
                    if enemy.hit_by_bullet(projectile):
                        if player.get("dmg"):
                            player.exp += enemy.damage(projectile.damage * pow(1.05, player.get("dmg")), enemies)
                        else:
                            player.exp += enemy.damage(projectile.damage, enemies)
                        projectiles.remove(projectile)
                        break
            for enemy in enemies:
                enemy.display(screen)
                enemy.move(player.pos)
                if enemy.touching_player(player.pos):
                    if hit_cooldown <= 0:
                        hit_cooldown = 20
                        defense = 1
                        if player.get("def"):
                            defense = pow(.99, player.get("def") - 1)
                        player.health -= enemy.dmg * defense
                        if player.health <= 0:
                            gaming = False
            hit_cooldown -= 1
            if random.random() * 1_000_000_000 <= 1 + failed:
                running = False
            else:
                failed += random.random()
            if player.exp >= round(20 * pow(1.1, player.lvl - 1)):
                await player.levelup(screen)
            pygame.draw.rect(screen, (255, 80, 90), (player.pos[0] - PLAYER_SIZE_X / 2, player.pos[1] - PLAYER_SIZE_Y / 2, PLAYER_SIZE_X, PLAYER_SIZE_Y), border_radius=9)
            pygame.draw.rect(screen, (20, 20, 20), (10, 10, SCREEN_WIDTH - 20, 30), border_radius=7)
            pygame.draw.rect(screen, (20, 200, 20), (10, 10, (SCREEN_WIDTH - 20) * (player.exp / round(20 * pow(1.1, player.lvl - 1))), 30), border_radius=7)
            timetext = pygame.font.SysFont("arial", 20).render(str(round(time.time() - stime, 2)), True, (122, 122, 122))
            screen.blit(timetext, (5, SCREEN_HEIGHT - 25))
            pygame.display.flip()
            clock.tick(tick_speed)
            tick += 1
            if tick >= tick_speed:
                tick = 0
                tick_speed = round(random.random() * 51 + 10)
                enemies.append(Enemy(random.choice(enemychances), (random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT)))
                enemychances = enemychances[1:]
                enemychances.append(random.randint(1, max(min(round(player.lvl // 5), max(enemy_data.keys())), 1)))
            await asyncio.sleep(0)
        etime = time.time()
        dead = True
        while dead and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: dead = False
            screen.fill((0, 0, 0))
            text = pygame.font.SysFont("arial", 100).render("Game Over", True, (255, 25, 2))
            highscore = max(highscore, round(etime - stime, 2))
            highscoretext = pygame.font.SysFont("arial", 40).render(f"Highscore: {highscore}", True, (255, 25, 2))
            currentscoretext = pygame.font.SysFont("arial", 30).render(f"Score: {round(etime - stime, 2)}", True, (255, 25, 2))
            pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH / 2 - text.get_width() / 2 - 5, SCREEN_HEIGHT / 2 - 55, text.get_width() + 10, 110), border_radius=27)
            pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH / 2 - highscoretext.get_width() / 2 - 5, SCREEN_HEIGHT / 2 + 60, highscoretext.get_width() + 10, 50), border_radius=27)
            pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH / 2 - currentscoretext.get_width() / 2 - 5, SCREEN_HEIGHT / 2 + 120, currentscoretext.get_width() + 10, 40), border_radius=27)
            screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - 50))
            screen.blit(highscoretext, (SCREEN_WIDTH / 2 - highscoretext.get_width() / 2, SCREEN_HEIGHT / 2 + 65))
            screen.blit(currentscoretext, (SCREEN_WIDTH / 2 - currentscoretext.get_width() / 2, SCREEN_HEIGHT / 2 + 125))
            pygame.display.update()
            await asyncio.sleep(0)
asyncio.run(main())