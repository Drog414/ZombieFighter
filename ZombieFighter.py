import pygame, sys

from pygame.locals import *
from time import sleep
from random import randint

pygame.init()

FPS = 60 # frames per second to update the screen
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((1920, 1080), FULLSCREEN)

pygame.display.set_caption("Zombie Fighter")


class Zombie(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.topleft = [50, 50]

    #def upgrade(self):

class Player(pygame.sprite.Sprite):

    def __init__(self, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([width, height])
        #self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.center

        self.health = 1

    #def upgrade(self):

    def dispHealth(self):
        DISPLAYSURF.blit(healthBar, (10, 0))
        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (170, 40, 1300, 70))
        pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (170, 40, int(self.health * 1300), 70))

class Weapon(pygame.sprite.Sprite):

    def __init__(self, sprites, posX, posY, speed):

        super().__init__()
        self.sprites = sprites
        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [posX, posY]

        self.isAnimating = False
        self.speed = speed

    def animate(self):
        self.isAnimating = True

    def update(self):
        if self.isAnimating:
            self.currentSprite += self.speed

            if self.currentSprite >= len(self.sprites):
                self.currentSprite = 0

            self.image = self.sprites[int(self.currentSprite)]

class Chainsaw(Weapon):

    def __init__(self, posX, posY):
        self.sprites = []
        self.sprites.append(pygame.image.load('Images/Chainsaw1.png'))
        self.sprites.append(pygame.image.load('Images/Chainsaw2.png'))

        super().__init__(self.sprites, posX, posY, 0.35)

class Pistol(Weapon):
    def __init__(self, posX, posY):
        self.sprites = []
        self.sprites.append(pygame.image.load('Images/Pistol.png'))

        super().__init__(self.sprites, posX, posY, 0.35)



background = pygame.image.load('Images/Background.png')
healthBar = pygame.image.load('Images/HealthBar.png')

def main():

    print("print")

    zombieGroup = pygame.sprite.Group()
    zombieGroup.add(Zombie((255, 255, 255), 50, 50))

    player = Player(50, 50)
    playerGroup = pygame.sprite.Group()
    playerGroup.add(player)

    weapon = Chainsaw(400, 400)
    weaponGroup = pygame.sprite.Group()
    weaponGroup.add(weapon)

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == K_z:
                    weapon.animate()

        DISPLAYSURF.blit(background, (0, 150))
        DISPLAYSURF.blit(pygame.transform.rotate(background, 180), (960, 150))

        #zombieGroup.draw(DISPLAYSURF)
        if player.health > 0:
            player.health -= .01
        player.dispHealth()

        weaponGroup.draw(DISPLAYSURF)
        weaponGroup.update()

        pygame.display.update()

        fpsClock.tick(FPS)

def drawScreen():
    DISPLAYSURF.blit(background, (0, 0))


if __name__ == '__main__':
    main()