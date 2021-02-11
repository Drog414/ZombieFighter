import pygame


class Weapon(pygame.sprite.Sprite):

    def __init__(self, sprites, posX, posY, aSpeed, direction):

        super().__init__()
        self.sprites = sprites
        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]

        self.rect = self.image.get_rect()
        self.posX = posX
        self.posY = posY
        self.rect.center = [posX, posY]

        self.isAnimating = False
        self.animationSpeed = aSpeed

    def animate(self):
        self.isAnimating = True

    def stopAnimate(self):
        self.isAnimating

    def update(self):
        if self.isAnimating:
            self.currentSprite += self.animationSpeed

            if self.currentSprite >= len(self.sprites):
                self.currentSprite = 0

            self.image = self.sprites[int(self.currentSprite)]
            self.rect = self.image.get_rect()
            self.rect.center = [self.posX, self.posY]

class Chainsaw(Weapon):

    def __init__(self, posX, posY):
        self.sprites = []
        self.sprites.append(pygame.image.load('Images/Chainsaw1.png'))
        self.sprites.append(pygame.image.load('Images/Chainsaw2.png'))

        super().__init__(self.sprites, posX, posY, 0.35, 1)

class Knife(Weapon):
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

        super().__init__(self.sprites, posX, posY, 0.40, 1)

class Pistol(Weapon):
    def __init__(self, posX, posY):
        self.sprites = []
        self.sprites.append(pygame.image.load('Images/Pistol.png'))

        super().__init__(self.sprites, posX, posY, 0, 1)
