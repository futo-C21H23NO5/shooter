import pygame

def load_image(path, size, colorkey):
    image = pygame.image.load(path).convert()
    image = pygame.transform.scale(image, size)
    image.set_colorkey(colorkey)
    return image