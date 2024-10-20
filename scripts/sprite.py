class Sprite:
    def __init__(self, x, y, image, speed):
        self.image = image
        self.speed = speed
        self.rect = image.get_rect(center=(x, y))

    def is_collide(self, other):
        return self.rect.colliderect(other.rect)

    def render(self, window):
        window.blit(self.image, self.rect)
