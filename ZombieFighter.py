import pygame, sys

from Projectiles import *
from Weapons import *

from pygame.locals import *
from random import randint

pygame.init()

FPS = 60 # frames per second to update the screen
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((1920, 1080), FULLSCREEN)

pygame.display.set_caption("Zombie Fighter")


class Zombie(pygame.sprite.Sprite):

    def __init__(self, posX, posY, aSpeed, mSpeed):
        super().__init__()

        self.sprites = []
        self.sprites.append(pygame.image.load('Images/Person0.png'))
        self.sprites.append(pygame.image.load('Images/Person1.png'))
        self.sprites.append(pygame.image.load('Images/Person2.png'))
        self.sprites.append(pygame.image.load('Images/Person3.png'))
        self.sprites.append(pygame.image.load('Images/Person4.png'))
        self.sprites.append(pygame.image.load('Images/Person5.png'))

        self.sprites1 = []
        for i in range(len(self.sprites)):
            self.sprites1.append(pygame.transform.flip(self.sprites[i], True, False))


        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]

        self.isAnimating = True
        self.animationSpeed = aSpeed

        self.isMoving = True
        self.movingSpeed = mSpeed

        self.direction = -1

        self.posX = posX
        self.posY = posY
        self.rect = self.image.get_rect()
        self.rect.midtop = [posX, posY]

    def switchDirection(self):
        self.direction *= -1

    def update(self):
        if self.isAnimating:
            self.currentSprite += self.animationSpeed

            if self.currentSprite >= len(self.sprites):
                self.currentSprite = 0
            if self.direction == 1:
                self.image = self.sprites[int(self.currentSprite)]
            else:
                self.image = self.sprites1[int(self.currentSprite)]

        if self.isMoving:
            self.posX += self.direction * self.movingSpeed
            self.rect.midtop = [int(self.posX), self.posY]

            if self.posX < 800 and self.direction == -1:
                self.switchDirection()
            elif self.posX > 1120 and self.direction == 1:
                self.switchDirection()


class Player(pygame.sprite.Sprite):

    def __init__(self, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([width, height])
        #self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.midtop = [960, 500]

        self.health = 1

    #def upgrade(self):

healthBar = pygame.image.load('Images/HealthBar.png')

def main():

    print("print")

    zombieGroup = pygame.sprite.Group()
    zombieGroup.add(Zombie(700, 500, 0.35, 7))

    global player
    player = Player(250, 300)
    playerGroup = pygame.sprite.Group()
    playerGroup.add(player)

    weapon = Chainsaw(400, 400)
    weaponGroup = pygame.sprite.Group()
    weaponGroup.add(weapon)


    projectileGroup = pygame.sprite.Group()
    knife = KnifeP(400, 600)
    projectileGroup.add(knife)

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
                    knife.animate()

        DISPLAYSURF.fill((69, 69, 69))
        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (0, 800, 1920, 280))



        dispHealth()

        playerGroup.draw(DISPLAYSURF)
        weaponGroup.draw(DISPLAYSURF)
        zombieGroup.draw(DISPLAYSURF)
        projectileGroup.draw(DISPLAYSURF)

        playerGroup.update()
        weaponGroup.update()
        zombieGroup.update()
        projectileGroup.update()


        pygame.display.update()

        fpsClock.tick(FPS)

#def drawScreen():


def dispHealth():
    DISPLAYSURF.blit(healthBar, (10, 0))
    pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (170, 40, int(player.health * 1300), 70))

if __name__ == '__main__':
    main()