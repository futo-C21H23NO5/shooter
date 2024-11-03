# pyinstaller --add-data 'images;./images' -F -w main.py

import pygame, os
from time import time

from scripts.player import Player
from scripts.enemy import Enemy
from scripts.functions import load_image
from scripts.bullet import Bullet
from random import randint
pygame.init()

flags = pygame.RESIZABLE | pygame.SCALED
window = pygame.display.set_mode((600, 800), flags)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 52)

FPS = 60

background = load_image("images" , "background.png", size = (600, 800), colorkey = None)
spacescipe_image = load_image("images" , "spaceship.png", size = (50, 50), colorkey = None)
bullet_image = load_image("images" , "bullet.png", size = (30, 30), colorkey = None)
ufo_image = load_image("images" , "UFOsprite.gif", size = (100, 100), colorkey = None)

player = Player(400, 550, spacescipe_image, 3, 5)
bullets = list()
enemies = list()

spawn_delta = 3.5
timer = time()
score = 0
player.health = 5

game = True
died = False

while game:
    #Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:
            if died:
                died = False
                score = 0
                bullets.clear()
                enemies.clear()
                player.health = 5
                player.rect.center = (400, 550)

            if event.key == pygame.K_SPACE and not died:
                bullets.append(Bullet(player.rect.centerx, player.rect.y, bullet_image, 30))

    #Обновление событий
    if not died:
        player.update()
        for emeny in enemies:
            emeny.update()
            for bullet in bullets:
                if emeny.is_collide(bullet):
                    bullets.remove(bullet)
                    emeny.get_damage()
            if emeny.is_collide(player):
                player.get_damage()
                enemies.remove(emeny)
                died = player.health <= 0

            elif emeny.health <= 0:
                score += 1
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
    
    text = "Здоровье: " + str(player.health)
    image_text = font.render(text, True, (255, 255, 255))
    image_rect = image_text.get_rect(topleft = (0, 0))
    window.blit(image_text, image_rect)

    text = 'Очки: ' + str(score)
    image_text = font.render(text, True, (255, 255, 255))
    image_rect = image_text.get_rect(midtop = (400, 0))
    window.blit(image_text, image_rect)

    if died:
        text = 'Нажмите любую клавишу, чтобы начать заново'
        image_text = big_font.render(text, True, (250, 50, 50))
        image_rect = image_text.get_rect(center = (400, 300))
        window.blit(image_text, image_rect)

    pygame.display.update()
    clock.tick(FPS)