import pygame

from Projectiles import *

class Weapon(pygame.sprite.Sprite):

    def __init__(self, sprites, posX, posY, aSpeed, direction):

        super().__init__()
        self.sprites = sprites
        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]

        if direction != 0:
            # For when the sprite is reversed
            self.sprites1 = []
            for i in range(len(self.sprites)):
                self.sprites1.append(pygame.transform.flip(self.sprites[i], True, False))

            self.direction = direction

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

        if self.direction == -1:
            self.image = self.sprites1[int(self.currentSprite)]
        else:
            self.image = self.sprites[int(self.currentSprite)]


class Chainsaw(Weapon):

    def __init__(self, posX, posY, direction):
        self.sprites = []
        self.sprites.append(pygame.image.load('Images/Chainsaw1.png'))
        self.sprites.append(pygame.image.load('Images/Chainsaw2.png'))

        self.hold = True

        super().__init__(self.sprites, posX, posY, 0.35, direction)

class Knife(Weapon):
    def __init__(self, posX, posY, direction):
        self.sprites = []
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), 90))
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), 45))
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), 0))
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), -45))
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), -90))
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), -135))
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), -180))
        self.sprites.append(pygame.transform.rotate(pygame.image.load('Images/Knife.png'), -225))

        self.hold = False
        self.maxProj = 99999999999999999999999999999999999999999999999999999999999999999
        self.numProj = 0
        self.fireRate = 1

        self.switchProjDir = False

        super().__init__(self.sprites, posX, posY, 0.40, direction)

    def getProj(self, direction):
        return KnifeP(960, 600, direction)

class Pistol(Weapon):
    def __init__(self, posX, posY, direction):
        self.sprites = []
        self.sprites.append(pygame.image.load('Images/Pistol.png'))

        self.hold = False
        self.maxProj = 99999999999999999999999999999999999999999999999999999999999999999
        self.numProj = 0

        self.switchProjDir = False

        super().__init__(self.sprites, posX, posY, 0, direction)

    def getProj(self, direction):
        return BulletSmallP(960, 600, direction)

class Flamethrower(Weapon):
    def __init__(self, posX, posY, direction):
        self.sprites = []
        self.sprites.append(pygame.image.load('Images/Flamethrower.png'))

        self.hold = True
        self.maxProj = 1
        self.numProj = 0
        self.fireRate = 1

        self.flameOn = False
        self.flameFull = False

        self.projDirection = direction

        super().__init__(self.sprites, posX, posY, 0, direction)

    def getProj(self, direction):
        self.numProj += 1
        return FireP(960 + (75 * direction), 570, direction)

class Skorpian(Weapon):
    def __init__(self, posX, posY, direction):
        self.sprites = []
        self.sprites.append(pygame.image.load('Images/Skorpion.png'))

        self.hold = True
        self.maxProj = 99999999999999999999999999999999999999999999999999999999999999999
        self.numProj = 0
        self.fireRate = 0.15

        self.switchProjDir = False

        super().__init__(self.sprites, posX, posY, 0, direction)

    def getProj(self, direction):
        return BulletSmallP(960, 600, direction)

class AssaultRifle(Weapon):
    def __init__(self, posX, posY, direction):
        self.sprites = []
        self.sprites.append(pygame.image.load('Images/AssaultRifle1.png'))

        self.hold = True
        self.maxProj = 99999999999999999999999999999999999999999999999999999999999999999
        self.numProj = 0
        self.fireRate = 0.2

        self.switchProjDir = False

        super().__init__(self.sprites, posX, posY, 0, direction)

    def getProj(self, direction):
        return BulletLargeP(960, 600, direction)

