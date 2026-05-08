import pygame
import math
import random
from player import Player
from projectile import Projectile
from enemy import Enemy
from const import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

abilities = [f"ABILITY {i}" if random.random() > .5 else None for i in range(10)]
projectiles = []

player = Player()
failed = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print("shoot")
                try:
                    diffx = event.pos[0] - player.pos[0]
                    diffy = player.pos[1] - event.pos[1]
                    if diffx == 0 and diffy = 0:
                        num = -1 + random.random() * 2
                    if diffx == 0:
                        projectiles.append(Projectile(1, (diffx / abs(diffx), 0), player.pos))
                    elif diffy == 0:
                        projectiles.append()
                        direction = player.pos[1] - event.pos[1]
                        direction /= -abs(direction)
                        projectiles.append(Projectile(1, (0, 1 * direction), player.pos))
                        continue
                    projectiles.append(Projectile(1, (), player.pos))
                except ArithmeticError:
                    direction = player.pos[0] - event.pos[0]
                    directon /= abs(direction)
                    projectiles.append(Projectile(1, (direction, 0), player.pos))
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
    if pressed[pygame.K_i] and not pressed[pygame.K_m]: player.vel[1] -= SPEED
    if pressed[pygame.K_r] and not pressed[pygame.K_l]: player.vel[0] -= SPEED
    if pressed[pygame.K_m] and not pressed[pygame.K_i]: player.vel[1] += SPEED
    if pressed[pygame.K_l] and not pressed[pygame.K_r]: player.vel[0] += SPEED
    player.vel[0] *= FRICTION
    player.vel[1] *= FRICTION

    player.pos[0] += player.vel[0]
    player.pos[1] += player.vel[1]
    if player.pos[0] < PLAYER_SIZE_X / 2 + SCREEN_MARGIN:
        player.pos[0] = PLAYER_SIZE_X / 2 + SCREEN_MARGIN
        player.vel[0] = 0
    if player.pos[0] > SCREEN_WIDTH - PLAYER_SIZE_X / 2 - SCREEN_MARGIN:
        player.pos[0] = SCREEN_WIDTH - PLAYER_SIZE_X / 2 - SCREEN_MARGIN
        player.vel[0] = 0
    if player.pos[1] < PLAYER_SIZE_Y / 2 + SCREEN_MARGIN:
        player.pos[1] = PLAYER_SIZE_Y / 2 + SCREEN_MARGIN
        player.vel[1] = 0
    if player.pos[1] > SCREEN_HEIGHT - PLAYER_SIZE_Y / 2 - SCREEN_MARGIN:
        player.pos[1] = SCREEN_HEIGHT - PLAYER_SIZE_Y / 2 - SCREEN_MARGIN
        player.vel[1] = 0

    if random.random() * 1_000_000_000 <= 1 + failed:
        running = False
    else:
        failed += random.random()
    
    screen.fill((30, 70, 255))
    pygame.draw.rect(screen, (255, 80, 90), (player.pos[0] - PLAYER_SIZE_X / 2, player.pos[1] - PLAYER_SIZE_Y / 2, PLAYER_SIZE_X, PLAYER_SIZE_Y), border_radius=9)

    pygame.display.flip()
    clock.tick(min(60.00000000000001,65.00000000000001-2.20000000000001**math.log(random.random()*pow(math.sqrt(5.00000000000001),2.00000000000001),1.45000000000001)//(1.00000000000001++-+-+---++1.00000000000001+--++-+-++--+1.00000000000001))//1)
