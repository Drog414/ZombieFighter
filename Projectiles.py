import pygame

class Projectile(pygame.sprite.Sprite):

    def __init__(self, sprites, posX, posY, aSpeed, mSpeed, direction, damage):

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

        self.isAnimating = True
        self.animationSpeed = aSpeed

        if mSpeed == 0:
            self.isMoving = False
        else:
            self.isMoving = True
        self.movingSpeed = mSpeed

        self.damage = damage

    def animate(self):
        self.isAnimating = True

    def stopAnimate(self):
        self.isAnimating

    def getDamage(self):
        return self.damage

    def update(self, playerPos, shift):
        if self.isAnimating:
            self.currentSprite += self.animationSpeed

            if self.currentSprite >= len(self.sprites):
                self.currentSprite = 0

            self.image = self.sprites[int(self.currentSprite)]

            self.rect = self.image.get_rect()

        if self.isMoving:
            self.posX += self.direction * self.movingSpeed

        self.rect.center = [int(self.posX), self.posY]


class KnifeP(Projectile):
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

        super().__init__(self.sprites, posX, posY, 0.4, 20, direction, 50)

class ExplosionP(Projectile):
    def __init__(self, posX, posY, direction):
        self.sprites = []
        for i in range(16):
            self.sprites.append(pygame.image.load('Images/Explosion' + str(i) + '.png'))

        #Explosion should eventually do 0 damage, maybe make a seperate effects class?
        super().__init__(self.sprites, posX, posY, 0.4, 0, direction, 50)