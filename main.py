import pygame, os
from time import time

from scripts.player import Player
from scripts.enemy import Enemy
from scripts.functions import load_image
from scripts.bullet import Bullet
from random import randint

flags = pygame.RESIZABLE | pygame.SCALED
window = pygame.display.set_mode((600, 800), flags)
clock = pygame.time.Clock()

FPS = 60

background = load_image(os.path.abspath("images\\background.png"), (600, 800), None)
spacescipe_image = load_image("images\\spaceship.png", (50, 50), None)
bullet_image = load_image("images\\bullet.png", (30, 30), None)
ufo_image = load_image("images\\UFOsprite.gif", (100, 100), None)

player = Player(400, 550, spacescipe_image, 3)
bullets = list()
enemies = list()

spawn_delta = 3.5
timer = time()

game = True
while game:
    #Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.rect.centerx, player.rect.y, bullet_image, 30))

    #Обновление событий
    player.update()
    for emeny in enemies:
        emeny.update()
        for bullet in bullets:
            if emeny.is_collide(bullet):
                bullets.remove(bullet)
                emeny.get_damage()
        if emeny.health <= 0:
            enemies.remove(emeny)
    
    for bullet in bullets.copy():
        bullet.update()
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)  
        
    delta = time() - timer
    if delta > spawn_delta:
        timer = time()
        x = randint(ufo_image.get_width() // 2, 800 - ufo_image.get_width() // 2,)
        y = - ufo_image.get_height() / 2
        speed = randint(3000, 5000) / 1000
        health = randint(1, 3)
        enemies.append(Enemy(x, y, ufo_image, speed, health))
        
        
            


    #Отрисовка объектов
    window.blit(background, (0, 0))
    player.render(window)
    for emeny in enemies:
        emeny.render(window)
    for bullet in bullets:
        bullet.render(window)
    pygame.display.update()
    clock.tick(FPS)