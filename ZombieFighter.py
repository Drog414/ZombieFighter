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

    def __init__(self, posX, posY, aSpeed, mSpeed, direction, playerPos):
        super().__init__()

        self.sprites = []
        self.sprites.append(pygame.image.load('Images/Person0.png'))
        self.sprites.append(pygame.image.load('Images/Person1.png'))
        self.sprites.append(pygame.image.load('Images/Person2.png'))
        self.sprites.append(pygame.image.load('Images/Person3.png'))
        self.sprites.append(pygame.image.load('Images/Person4.png'))
        self.sprites.append(pygame.image.load('Images/Person5.png'))

        #For when the sprite is reversed
        self.sprites1 = []
        for i in range(len(self.sprites)):
            self.sprites1.append(pygame.transform.flip(self.sprites[i], True, False))

        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]

        self.isAnimating = True
        self.animationSpeed = aSpeed

        self.isMoving = True
        self.movingSpeed = mSpeed

        self.direction = direction

        self.posX = posX
        self.posY = posY
        self.rect = self.image.get_rect()
        self.rect.midtop = [posX - playerPos, posY]

        self.health = 100
        self.damage = 0.25

    def switchDirection(self):
        self.direction *= -1

    def takeDamage(self, damage):
        self.health -= damage

    def dealDamage(self):
        return self.damage

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
            self.posX += (self.direction * self.movingSpeed)
            self.rect.midtop = [int(self.posX) - player.playerPos, self.posY]

            #self.posX < 800
            if self.posX < player.playerPos + 960 and self.direction == -1:
                self.switchDirection()
            #self.posX > 1120
            elif self.posX > player.playerPos + 960 and self.direction == 1:
                self.switchDirection()


class Player(pygame.sprite.Sprite):

    def __init__(self, width, height, mSpeed):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.midtop = [960, 500]

        self.playerPos = PLAYAREA / 2

        self.direction = 1

        self.health = 100
        self.armor = 0

        self.movingSpeed = mSpeed

        self.bulletSAmmo = 0
        self.bulletLAmmo = 0
        self.knifeAmmo = 0
        self.fireAmmo = 0

        self.money = 0

    def takeDamage(self, damage):
        self.health -= damage + int(self.armor * damage)

    #Might not be necessary?
    def switchDirection(self):
        self.direction *= -1

    #def upgrade(self):

healthBar = pygame.image.load('Images/HealthBar.png')

font = pygame.font.SysFont(None, 100)
smallFont = pygame.font.SysFont(None, 50)

#Constants
PLAYAREA = 6000

def main():

    menu()

    global zombieGroup
    zombieGroup = pygame.sprite.Group()

    global player
    player = Player(100, 300, 10)
    playerGroup = pygame.sprite.Group()
    playerGroup.add(player)

    weapons = []
    weapons.append(Pistol(960, 600, player.direction))
    weapons.append(Knife(960, 600, player.direction))
    weapons.append(Chainsaw(960, 600, player.direction))
    weapons.append(Skorpian(960, 600, player.direction))
    weapons.append(AssaultRifle(960, 600, player.direction))
    weapons.append(Flamethrower(960, 600, player.direction))

    weaponGroup = pygame.sprite.Group()

    currentWeapon = 0
    weaponGroup.add(weapons[currentWeapon])


    projectileGroup = pygame.sprite.Group()

    fireRateCounter = 0
    currentFlameSprite = 0

    pygame.event.clear()

    while True:

        weapons[5].flameOn = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == K_z and not weapons[currentWeapon].hold:
                    if weapons[currentWeapon].numProj < weapons[currentWeapon].maxProj:
                        projectileGroup.add(weapons[currentWeapon].getProj(player.direction))

                if event.key == K_SPACE:
                    spawnZombie()

                if event.key == K_x:
                    if type(weapons[currentWeapon]) is Flamethrower:
                        for proj in projectileGroup:
                            if type(proj) is FireP:
                                projectileGroup.remove(proj)
                                weapons[currentWeapon].numProj -= 1
                                break
                    weaponGroup.remove(weapons[currentWeapon])
                    currentWeapon += 1
                    if currentWeapon >= len(weapons):
                        currentWeapon = 0
                    weaponGroup.add(weapons[currentWeapon])
                    weapons[currentWeapon].direction = player.direction
                    fireRateCounter = 1


                if event.key == K_LSHIFT:
                    if type(weapons[currentWeapon]) is Flamethrower:
                        for proj in projectileGroup:
                            if type(proj) is FireP:
                                projectileGroup.remove(proj)
                                weapons[currentWeapon].numProj -= 1
                                break
                    weaponGroup.remove(weapons[currentWeapon])
                    currentWeapon -= 1
                    if currentWeapon < 0:
                        currentWeapon = len(weapons) - 1
                    weaponGroup.add(weapons[currentWeapon])
                    weapons[currentWeapon].direction = player.direction
                    fireRateCounter = 1



        if pygame.key.get_pressed()[pygame.K_LEFT] and player.playerPos > 0:
            player.playerPos -= player.movingSpeed
            player.direction = -1
            weapons[currentWeapon].direction = -1
            if type(weapons[currentWeapon]) is Flamethrower:
                if weapons[currentWeapon].projDirection == 1:
                    weapons[currentWeapon].projDirection = -1
                    for proj in projectileGroup:
                        if type(proj) is FireP:
                            projectileGroup.remove(proj)
                            projectileGroup.add(weapons[currentWeapon].getProj(player.direction))
                            weapons[currentWeapon].numProj -= 1
                            break

        elif pygame.key.get_pressed()[pygame.K_RIGHT] and player.playerPos < PLAYAREA:
            player.playerPos += player.movingSpeed
            player.direction = 1
            weapons[currentWeapon].direction = 1
            if type(weapons[currentWeapon]) is Flamethrower:
                if weapons[currentWeapon].projDirection == -1:
                    weapons[currentWeapon].projDirection = 1
                    for proj in projectileGroup:
                        if type(proj) is FireP:
                            projectileGroup.remove(proj)
                            projectileGroup.add(weapons[currentWeapon].getProj(player.direction))
                            weapons[currentWeapon].numProj -= 1
                            break

        if weapons[currentWeapon].hold:

            if pygame.key.get_pressed()[pygame.K_z]:
                print("z")
                if currentWeapon != 5:
                    fireRateCounter += weapons[currentWeapon].fireRate
                    if weapons[currentWeapon].numProj < weapons[currentWeapon].maxProj and int(fireRateCounter) >= 1:
                        projectileGroup.add(weapons[currentWeapon].getProj(player.direction))
                        fireRateCounter = 0
                else:
                    weapons[currentWeapon].flameOn = True

        if currentWeapon == 5:
            if weapons[5].flameOn:
                fireRateCounter += weapons[currentWeapon].fireRate
                if weapons[currentWeapon].numProj < weapons[currentWeapon].maxProj and int(fireRateCounter) > 1:
                    projectileGroup.add(weapons[currentWeapon].getProj(player.direction))
                    fireRateCounter = 0
            if not weapons[5].flameOn:
                for proj in projectileGroup:
                    if type(proj) is FireP:
                        projectileGroup.remove(proj)
                        weapons[currentWeapon].numProj -= 1


        DISPLAYSURF.fill((69, 69, 69))
        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (860 - player.playerPos, 800, PLAYAREA + 200, 280))
        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (860 - player.playerPos, 600, 10, 200))
        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (1050 - player.playerPos + PLAYAREA, 600, 10, 200))

        for zombie in zombieGroup:
            if pygame.sprite.spritecollide(zombie, projectileGroup, False):
                for proj in projectileGroup:
                    if pygame.sprite.spritecollide(proj, zombieGroup, False):
                        zombie.takeDamage(proj.getDamage())
                        if proj.deleteOnImpact:
                            projectileGroup.remove(proj)
                            weapons[currentWeapon].numProj -= 1
                        if zombie.health <= 0:
                            zombieGroup.remove(zombie)

            if pygame.sprite.spritecollide(zombie, playerGroup, False):
                player.takeDamage(zombie.dealDamage())

        for proj in projectileGroup:
            if proj.posX + player.playerPos > PLAYAREA + 1000 or proj.posX + player.playerPos < -100:
                projectileGroup.remove(proj)

        dispStats()

        projectileGroup.draw(DISPLAYSURF)
        playerGroup.draw(DISPLAYSURF)
        weaponGroup.draw(DISPLAYSURF)
        zombieGroup.draw(DISPLAYSURF)


        playerGroup.update()
        weaponGroup.update()
        zombieGroup.update()
        projectileGroup.update(player.playerPos)


        pygame.display.update()

        fpsClock.tick(FPS)

    return True

#def drawScreen():


def dispStats():
    DISPLAYSURF.blit(healthBar, (10, 0))
    pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (170, 40, int(player.health * 13), 70))
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (1500, 0, 420, 150))
    img = smallFont.render("Ammo", True, (255, 255, 255))
    imgPos = img.get_rect(center=(int(1920 / 2), int(1080 / 4)))
    DISPLAYSURF.blit(img, imgPos)


def spawnZombie():
    posX = randint(0, PLAYAREA)
    if posX < player.playerPos:
        direction = 1
    else:
        direction = -1
    zombieGroup.add(Zombie(posX, 500, 0.35, 7, direction, player.playerPos))

def menu():

    pygame.event.clear(eventtype = KEYDOWN)

    instructions = False

    mode = 0
    pos = 1
    showControls = False

    while mode == 0:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    if not showControls:
                        if pos == 1:
                            mode = 1
                        else:
                            showControls = True
                    else:
                        showControls = False

                if event.key == K_UP and pos > 1:
                    pos -= 1
                if event.key == K_DOWN and pos < 2:
                    pos += 1



        DISPLAYSURF.fill((69, 69, 69))
        if not showControls:
            img = font.render("Zombie Fighter", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(1920 / 2), int(1080 / 4)))
            DISPLAYSURF.blit(img, imgPos)
    
            img = smallFont.render("Play", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(1920 / 2), int(1080 / 2)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 1:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
            img = smallFont.render("Controls", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(1920 / 2),  3 * int(1080 / 4)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 2:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
        else:
            img = smallFont.render(" - Controls - ", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(1920 / 2), int(1080 / 4)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Use the arrow keys to move", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(1920 / 2), int(1080 / 4) + int(1080 * 0.05) + int(1080 * 0.05)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Press Z to fire your weapon", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(1920 / 2), int(1080 / 4) + int(1080 * 0.05) + 2 * int(1080 * 0.05)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Press Shift and X to change weapons", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(1920 / 2), int(1080 / 4) + int(1080 * 0.05) + 3 * int(1080 * 0.05)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Press Escape to quit", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(1920 / 2), int(1080 / 4) + int(1080 * 0.05) + 4 * int(1080 * 0.05)))
            DISPLAYSURF.blit(img, imgPos)

            img = smallFont.render("Press Z to return to the title screen", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(1920 / 2), int(1080 / 4) + 3 * int(1080 * 0.05) + 11 * int(1080 * 0.05)))
            DISPLAYSURF.blit(img, imgPos)


        pygame.display.update()
        fpsClock.tick(FPS)



if __name__ == '__main__':
    replay = True
    while replay:
        replay = main()