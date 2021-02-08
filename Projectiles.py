import pygame

class Projectile(pygame.sprite.Sprite):

    def __init__(self, sprites, posX, posY, speed):

        super().__init__()
        self.sprites = sprites
        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]

        self.rect = self.image.get_rect()
        self.posX = posX
        self.posY = posY
        self.rect.center = [posX, posY]

        self.isAnimating = False
        self.speed = speed

    def animate(self):
        self.isAnimating = True

    def stopAnimate(self):
        self.isAnimating

    def update(self):
        if self.isAnimating:
            self.currentSprite += self.speed

            if self.currentSprite >= len(self.sprites):
                self.currentSprite = 0

            self.image = self.sprites[int(self.currentSprite)]
            self.rect = self.image.get_rect()
            self.rect.center = [self.posX, self.posY]

class KnifeP(Projectile):
    def __init__(self, posX, posY):
        self.sprites = []
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), 90))
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), 45))
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), 0))
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), -45))
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), -90))
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), -135))
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), -180))
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), -225))

        super().__init__(self.sprites, posX, posY, 0.40)