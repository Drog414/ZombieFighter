import pygame, sys

from Projectiles import *
from Weapons import *

from pygame.locals import *
from random import randint

pygame.init()

FPS = 60 # frames per second to update the screen
fpsClock = pygame.time.Clock()

infoObject = pygame.display.Info()
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)

pygame.display.set_caption("Zombie Fighter")


class Zombie(pygame.sprite.Sprite):

    def __init__(self, posX, posY, aSpeed, mSpeed, direction, playerPos, health, damage, waveNum):
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

        self.health = health
        self.damage = damage

        self.moneyUponDeath = int(randint(7, 13) / 10 * self.health)

    def switchDirection(self):
        self.direction *= -1

    def takeDamage(self, damage):
        self.health -= damage

    def dealDamage(self):
        return self.damage

    def getMoney(self):
        return self.moneyUponDeath

    def setSpawn(self, playerPos):
        posX = randint(0, PLAYAREA)
        spawn = False
        while not spawn:
            posX = randint(0, PLAYAREA)
            if 100 < playerPos < PLAYAREA - 100:
                if not (460 < posX - playerPos < 1460):
                    spawn = True
            else:
                spawn = True

        if posX < playerPos:
            self.direction = 1
        else:
            self.direction = -1
        print(posX)
        print(playerPos)
        self.posX = posX
        self.rect.midtop = [posX - playerPos, self.posY]

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
            if self.posX < player.playerPos + int(WIDTH / 2) and self.direction == -1:
                self.switchDirection()
            #self.posX > 1120
            elif self.posX > player.playerPos + int(WIDTH / 2) and self.direction == 1:
                self.switchDirection()


class Player(pygame.sprite.Sprite):

    def __init__(self, mSpeed):

        super().__init__()

        self.sprites = []
        self.sprites.append(pygame.image.load('Images/Player.png'))

        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.midtop = [int(WIDTH / 2), 500]

        self.playerPos = PLAYAREA / 2

        self.direction = 1

        self.health = 100
        self.armor = 0

        self.movingSpeed = mSpeed

        self.bulletSAmmo = 50
        self.bulletLAmmo = 0
        self.knifeAmmo = 0
        self.fireAmmo = 0

        self.hasWeapon = []
        self.hasWeapon.append(True)
        self.hasWeapon.append(False)
        self.hasWeapon.append(False)
        self.hasWeapon.append(False)
        self.hasWeapon.append(False)


        self.money = 0
        self.moneyUpgrade = 0

    def takeDamage(self, damage):
        self.health -= damage + int(self.armor * damage)

    def addMoney(self, money):
        self.money += money + int(money * self.moneyUpgrade)

class Grass(pygame.sprite.Sprite):

    def __init__(self, pos):

        super().__init__()

        self.sprites = []
        self.sprites.append(pygame.image.load('Images/Grass.png'))

        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = [pos, 750]

    def update(self, move):
        self.pos += move

        if self.pos < -300:
            self.pos += 2400
        elif self.pos > 2100:
            self.pos -= 2400

        self.rect.topleft = [self.pos, 750]



healthBar = pygame.image.load('Images/HealthBar.png')
armor = pygame.image.load('Images/Armor.png')
ammoBox = pygame.image.load('Images/AmmoBox.png')
money = pygame.image.load('Images/Money.png')
smallHealth = pygame.image.load('Images/SmallHealth.png')

font = pygame.font.SysFont(None, 100)
smallFont = pygame.font.SysFont(None, 50)

#Constants
PLAYAREA = 8000

def main():

    menu()

    global zombieGroup
    zombieGroup = pygame.sprite.Group()

    global player
    player = Player(10)
    playerGroup = pygame.sprite.Group()
    playerGroup.add(player)

    global grassGroup
    grassGroup = pygame.sprite.Group()
    grassGroup.add(Grass(-300))
    grassGroup.add(Grass(0))
    grassGroup.add(Grass(300))
    grassGroup.add(Grass(600))
    grassGroup.add(Grass(900))
    grassGroup.add(Grass(1200))
    grassGroup.add(Grass(1500))
    grassGroup.add(Grass(1800))
    grassGroup.add(Grass(2100))

    weapons = []
    weapons.append(Pistol(int(WIDTH / 2), 600, player.direction))
    weapons.append(Skorpian(int(WIDTH / 2), 600, player.direction))
    weapons.append(AssaultRifle(int(WIDTH / 2), 600, player.direction))
    weapons.append(Knife(int(WIDTH / 2), 600, player.direction))
    weapons.append(Flamethrower(int(WIDTH / 2), 600, player.direction))

    weaponGroup = pygame.sprite.Group()

    global currentWeapon
    currentWeapon = 0
    weaponGroup.add(weapons[currentWeapon])


    projectileGroup = pygame.sprite.Group()

    fireRateCounter = 0

    global lose
    lose = False

    waveNum = 0

    pygame.event.clear(eventtype = KEYDOWN)

    while not lose:

        waveNum += 1

        waitTime = int(pygame.time.get_ticks() / 1000) + 2
        while waitTime > int(pygame.time.get_ticks() / 1000):
            DISPLAYSURF.fill((69, 69, 69))
            img = font.render("Wave " + str(waveNum), True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 4)))
            DISPLAYSURF.blit(img, imgPos)

            pygame.display.update()


        pygame.event.clear(eventtype=KEYDOWN)

        zombieGroup.empty()
        projectileGroup.empty()

        shop()

        inLevel = True
        pauseState = False

        zombiesKilled = 0
        zombiesSpawned = 0

        zombieList = setWave(waveNum)

        #main game loop
        while inLevel:

            weapons[4].flameOn = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if event.key == K_p:
                        if not pauseState:
                            pauseState = True
                        else:
                            pauseState = False

                    if not pauseState:
                        if event.key == K_z and not weapons[currentWeapon].hold:
                            if currentWeapon == 0 and player.bulletSAmmo > 0:
                                if weapons[currentWeapon].numProj < weapons[currentWeapon].maxProj:
                                    projectileGroup.add(weapons[currentWeapon].getProj(player.direction))
                                    player.bulletSAmmo -= 1

                            elif currentWeapon == 3 and player.knifeAmmo > 0:
                                if weapons[currentWeapon].numProj < weapons[currentWeapon].maxProj:
                                    projectileGroup.add(weapons[currentWeapon].getProj(player.direction))
                                    player.knifeAmmo -= 1

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
                            while True:
                                if not player.hasWeapon[currentWeapon]:
                                    currentWeapon += 1
                                    if currentWeapon >= len(weapons):
                                        currentWeapon = 0
                                else:
                                    break
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
                            while True:
                                if not player.hasWeapon[currentWeapon]:
                                    currentWeapon -= 1
                                    if currentWeapon < 0:
                                        currentWeapon = len(weapons) - 1
                                else:
                                    break
                            weaponGroup.add(weapons[currentWeapon])
                            weapons[currentWeapon].direction = player.direction
                            fireRateCounter = 1


            if not pauseState:
                if pygame.key.get_pressed()[pygame.K_LEFT] and player.playerPos > 1000:
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
                    grassGroup.update(5)

                elif pygame.key.get_pressed()[pygame.K_RIGHT] and player.playerPos < PLAYAREA - 1000:
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
                    grassGroup.update(-5)

                if weapons[currentWeapon].hold:

                    if pygame.key.get_pressed()[pygame.K_z]:
                        if currentWeapon != 4:
                            fireRateCounter += weapons[currentWeapon].fireRate
                            if currentWeapon == 2 and player.bulletLAmmo > 0:
                                if weapons[currentWeapon].numProj < weapons[currentWeapon].maxProj and int(fireRateCounter) >= 1:
                                    projectileGroup.add(weapons[currentWeapon].getProj(player.direction))
                                    fireRateCounter = 0
                                    player.bulletLAmmo -= 1
                            elif currentWeapon == 1 and player.bulletSAmmo > 0:
                                if weapons[currentWeapon].numProj < weapons[currentWeapon].maxProj and int(fireRateCounter) >= 1:
                                    projectileGroup.add(weapons[currentWeapon].getProj(player.direction))
                                    fireRateCounter = 0
                                    player.bulletSAmmo -= 1
                        else:
                            if player.fireAmmo > 0:
                                weapons[currentWeapon].flameOn = True
                                player.fireAmmo -= 0.05

                if currentWeapon == 4:
                    if weapons[4].flameOn:
                        fireRateCounter += weapons[currentWeapon].fireRate
                        if weapons[currentWeapon].numProj < weapons[currentWeapon].maxProj and int(fireRateCounter) > 1:
                            projectileGroup.add(weapons[currentWeapon].getProj(player.direction))
                            fireRateCounter = 0
                    if not weapons[4].flameOn:
                        for proj in projectileGroup:
                            if type(proj) is FireP:
                                projectileGroup.remove(proj)
                                weapons[currentWeapon].numProj -= 1


                DISPLAYSURF.fill((42, 42, 42))
                pygame.draw.rect(DISPLAYSURF, (131, 101, 57), (860 - player.playerPos, 800, PLAYAREA + 200, 280))

                for zombie in zombieGroup:
                    if pygame.sprite.spritecollide(zombie, projectileGroup, False):
                        for proj in projectileGroup:
                            if pygame.sprite.spritecollide(proj, zombieGroup, False):
                                zombie.takeDamage(proj.getDamage())
                                if proj.deleteOnImpact:
                                    projectileGroup.remove(proj)
                                    weapons[currentWeapon].numProj -= 1
                                if zombie.health <= 0:
                                    player.addMoney(zombie.getMoney())
                                    zombieGroup.remove(zombie)
                                    zombiesKilled += 1

                    if pygame.sprite.spritecollide(zombie, playerGroup, False):
                        player.takeDamage(zombie.dealDamage())
                        if player.armor > 0:
                            player.armor -= 0.0001
                            if player.armor < 0:
                                player.armor = 0

                for proj in projectileGroup:
                    if proj.posX + player.playerPos > PLAYAREA + 1000 or proj.posX + player.playerPos < -100:
                        projectileGroup.remove(proj)

                dispStats()

                if player.health <= 0:
                    lose = True
                    inLevel = False

                if spawnZombie(waveNum) and zombiesSpawned < len(zombieList):
                    zombieList[zombiesSpawned].setSpawn(player.playerPos)
                    zombieGroup.add(zombieList[zombiesSpawned])
                    zombiesSpawned += 1

                playerGroup.draw(DISPLAYSURF)
                projectileGroup.draw(DISPLAYSURF)
                weaponGroup.draw(DISPLAYSURF)
                zombieGroup.draw(DISPLAYSURF)
                grassGroup.draw(DISPLAYSURF)


                playerGroup.update()
                weaponGroup.update()
                zombieGroup.update()
                projectileGroup.update(player.playerPos)
            else:
                img = font.render("PAUSED", True, (255, 255, 255))
                imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 3)))
                DISPLAYSURF.blit(img, imgPos)

            if zombiesKilled >= len(zombieList):
                inLevel = False

            pygame.display.update()

            fpsClock.tick(FPS)

        waitTime = int(pygame.time.get_ticks() / 1000) + 2
        while waitTime > int(pygame.time.get_ticks() / 1000):
            if not lose:
                img = font.render("You Survived!", True, (255, 255, 255))
            else:
                img = font.render("You Died!", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 3)))
            DISPLAYSURF.blit(img, imgPos)

            pygame.display.update()

    return True


def dispStats():
    DISPLAYSURF.blit(healthBar, (10, 0))
    pygame.draw.rect(DISPLAYSURF, (255, 0, 0), (170, 40, int(player.health * 13), 70))
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (1500, 0, 420, 150))
    DISPLAYSURF.blit(armor, (1508, 0))
    DISPLAYSURF.blit(ammoBox, (1648, 25))
    DISPLAYSURF.blit(money, (1788, 6))

    img = smallFont.render(str(int(player.armor * 2 * 100)) + "%", True, (255, 255, 255))
    imgPos = img.get_rect(center=(1570, 130))
    DISPLAYSURF.blit(img, imgPos)

    if currentWeapon == 0 or currentWeapon == 1:
        img = smallFont.render(str(player.bulletSAmmo), True, (255, 255, 255))
    elif currentWeapon == 2:
        img = smallFont.render(str(player.bulletLAmmo), True, (255, 255, 255))
    elif currentWeapon == 3:
        img = smallFont.render(str(player.knifeAmmo), True, (255, 255, 255))
    elif currentWeapon == 4:
        img = smallFont.render(str(int(player.fireAmmo)), True, (255, 255, 255))
    imgPos = img.get_rect(center=(1710, 130))
    DISPLAYSURF.blit(img, imgPos)

    img = smallFont.render("$" + str(player.money), True, (255, 255, 255))
    imgPos = img.get_rect(center=(1850, 130))
    DISPLAYSURF.blit(img, imgPos)


def setWave(waveNum):

    zombieList = []

    #Determine the number of zombies
    multiplier = 2.5 + (.25 * int(waveNum / 4))
    numZombies = int(multiplier * waveNum) + 3

    #Set other zombie attributes
    # - Health
    # - Damage
    # - Speed

    for i in range(numZombies):
        health = 100 + 5 * (waveNum - 1)
        damage = 0.25 + (randint(1, 10) / 100) * int(waveNum / 5)
        speed = 7 + randint(-1, 1) + int(1.5 * int(waveNum / 5))

        zombieList.append(Zombie(0, 500, 0.35, speed, 1, player.playerPos, health, damage, waveNum))

    return zombieList

def spawnZombie(waveNum):
    chance = randint(1, 100)
    limit = 2
    waveChance = randint(1, 3)
    if chance <= limit and waveChance <= 2:
        return True
    return False

def menu():

    pygame.event.clear(eventtype = KEYDOWN)

    mode = 0
    pos = 1
    showControls = False

    while mode == 0:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

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
            imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 4)))
            DISPLAYSURF.blit(img, imgPos)
    
            img = smallFont.render("Play", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 1:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
            img = smallFont.render("Controls", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2),  3 * int(HEIGHT / 4)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 2:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
        else:
            img = smallFont.render(" - Controls - ", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 4)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Use the arrow keys to move", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 4) + int(HEIGHT * 0.05) + int(HEIGHT * 0.05)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Either press or hold Z to fire your weapon", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 4) + int(HEIGHT * 0.05) + 2 * int(HEIGHT * 0.05)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Press Shift and X to change weapons", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 4) + int(HEIGHT * 0.05) + 3 * int(HEIGHT * 0.05)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Press P to pause", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 4) + int(HEIGHT * 0.05) + 4 * int(HEIGHT * 0.05)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Press Escape to quit", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 4) + int(HEIGHT * 0.05) + 5 * int(HEIGHT * 0.05)))
            DISPLAYSURF.blit(img, imgPos)

            img = smallFont.render("Press Z to return to the title screen", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 4) + 3 * int(HEIGHT * 0.05) + 11 * int(HEIGHT * 0.05)))
            DISPLAYSURF.blit(img, imgPos)


        pygame.display.update()
        fpsClock.tick(FPS)


def shop():
    pygame.event.clear(eventtype=KEYDOWN)

    #shopArea codes
    #0 - main shop menu
    #1 - weapon purchase menu
    #2 - ammo purchase menu
    #3 - upgrades and health menu

    start = False

    shopArea = 0
    pos = 1

    maxPos = 4

    while not start:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == K_z:
                    if shopArea == 0:
                        shopArea = pos
                        pos = 1
                    else:
                        if pos == maxPos:
                            shopArea = 0
                            pos = 1
                        elif shopArea == 1:
                            #buy Skorpian
                            if pos == 1 and not player.hasWeapon[1] and player.money >= 1000:
                                player.hasWeapon[1] = True
                                player.money -= 1000
                            #buy assault Rifle
                            if pos == 2 and not player.hasWeapon[2] and player.money >= 5000:
                                player.hasWeapon[2] = True
                                player.money -= 5000
                            #buy Knife
                            if pos == 3 and not player.hasWeapon[3] and player.money >= 20000:
                                player.hasWeapon[3] = True
                                player.money -= 20000
                            #buy Flamethrower
                            if pos == 4 and not player.hasWeapon[4] and player.money >= 10000:
                                player.hasWeapon[4] = True
                                player.money -= 10000

                        elif shopArea == 2:
                            #buy Small Bullets
                            if pos == 1 and player.money >= 10:
                                player.bulletSAmmo += 10
                                player.money -= 10
                            #buy Large Bullets
                            if pos == 2 and player.money >= 25:
                                player.bulletLAmmo += 10
                                player.money -= 25
                            #buy Knives
                            if pos == 3 and player.money >= 200:
                                player.knifeAmmo += 1
                                player.money -= 200
                            #buy Flamethrower
                            if pos == 4 and player.money >= 100:
                                player.fireAmmo += 5
                                player.money -= 100

                        elif shopArea == 3:
                            #buy Armor
                            if pos == 1 and player.money >= 250 and player.armor < 0.50:
                                player.armor += 0.05
                                if player.armor > 0.5:
                                    player.armor = 0.5
                                player.money -= 250
                            #buy Health
                            if pos == 2 and player.money >= 50 and player.health < 100:
                                player.health += 10
                                if player.health > 100:
                                    player.health = 100
                                player.money -= 50
                            #buy Money Upgrade
                            if pos == 3 and player.money >= 500 and player.moneyUpgrade < 1:
                                player.moneyUpgrade += 0.05
                                if player.moneyUpgrade > 1:
                                    player.moneyUpgrade = 1
                                player.money -= 500




                if event.key == K_UP and pos > 1:
                    pos -= 1
                if event.key == K_DOWN and pos < maxPos:
                    pos += 1

        DISPLAYSURF.fill((69, 69, 69))

        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (0, 0, 420, 400))
        DISPLAYSURF.blit(armor, (8, 0))
        DISPLAYSURF.blit(smallHealth, (148, 0))
        DISPLAYSURF.blit(money, (288, 6))

        img = smallFont.render(str(int(player.armor * 2 * 100)) + "%", True, (255, 255, 255))
        imgPos = img.get_rect(center=(70, 130))
        DISPLAYSURF.blit(img, imgPos)

        img = smallFont.render(str(int(player.health)) + "%", True, (255, 255, 255))
        imgPos = img.get_rect(center=(210, 130))
        DISPLAYSURF.blit(img, imgPos)

        img = smallFont.render("$" + str(player.money), True, (255, 255, 255))
        imgPos = img.get_rect(center=(350, 130))
        DISPLAYSURF.blit(img, imgPos)

        img = smallFont.render("Small Bullets: " + str(player.bulletSAmmo), True, (255, 255, 255))
        imgPos = img.get_rect(center=(210, 190))
        DISPLAYSURF.blit(img, imgPos)
        img = smallFont.render("Large Bullets: " + str(player.bulletLAmmo), True, (255, 255, 255))
        imgPos = img.get_rect(center=(210, 230))
        DISPLAYSURF.blit(img, imgPos)
        img = smallFont.render("Knives: " + str(player.knifeAmmo), True, (255, 255, 255))
        imgPos = img.get_rect(center=(210, 270))
        DISPLAYSURF.blit(img, imgPos)
        img = smallFont.render("Flamethrower Gas: " + str(int(player.fireAmmo)), True, (255, 255, 255))
        imgPos = img.get_rect(center=(210, 310))
        DISPLAYSURF.blit(img, imgPos)

        img = smallFont.render("Money Upgrade: +" + str(int(player.moneyUpgrade * 100)) + "%", True, (255, 255, 255))
        imgPos = img.get_rect(center=(210, 370))
        DISPLAYSURF.blit(img, imgPos)

        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (1500, 0, 420, 400))


        if shopArea == 0:
            maxPos = 4
            img = font.render("- Shop - ", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Weapons", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 2 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 1:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                img = smallFont.render("Purchase Weapons", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 200))
                DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Ammo", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 3 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 2:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                img = smallFont.render("Purchase Ammo", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 200))
                DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Upgrades & Health", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 4 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 3:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                img = smallFont.render("Upgrades and Health", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 200))
                DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Play", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 5 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 4:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                img = smallFont.render("Start Wave", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 200))
                DISPLAYSURF.blit(img, imgPos)


        elif shopArea == 1:
            maxPos = 5
            img = font.render("- Weapons - ", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Skorpian", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 2 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 1:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                if player.hasWeapon[1]:
                    img = smallFont.render("Already Purchased", True, (255, 255, 255))
                else:
                    img = smallFont.render("Cost: $1000", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 200))
                DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Assault Rifle", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 2.5 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 2:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                if player.hasWeapon[2]:
                    img = smallFont.render("Already Purchased", True, (255, 255, 255))
                else:
                    img = smallFont.render("Cost: $5000", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 200))
                DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Knife", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 3 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 3:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                if player.hasWeapon[3]:
                    img = smallFont.render("Already Purchased", True, (255, 255, 255))
                else:
                    img = smallFont.render("Cost: $20000", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 200))
                DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Flamethrower", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 3.5 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 4:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                if player.hasWeapon[4]:
                    img = smallFont.render("Already Purchased", True, (255, 255, 255))
                else:
                    img = smallFont.render("Cost: $10000", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 200))
                DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Back", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 4 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 5:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                img = smallFont.render("Back", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 200))
                DISPLAYSURF.blit(img, imgPos)

        elif shopArea == 2:
            maxPos = 5
            img = font.render("- Ammo - ", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Small Bullets", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 2 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 1:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                img = smallFont.render("Cost: $10 for 10", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 100))
                DISPLAYSURF.blit(img, imgPos)
                img = smallFont.render("Pistol and Skorpian", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 300))
                DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Large Bullets", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 2.5 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 2:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                img = smallFont.render("Cost: $25 for 10", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 100))
                DISPLAYSURF.blit(img, imgPos)
                img = smallFont.render("Assault Rifle", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 300))
                DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Knife", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 3 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 3:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                img = smallFont.render("Cost: $200 for 1", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 100))
                DISPLAYSURF.blit(img, imgPos)
                img = smallFont.render("Insta-Kill Knife", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 300))
                DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Flamethrower Gas", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 3.5 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 4:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                img = smallFont.render("Cost: $100 for 5", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 100))
                DISPLAYSURF.blit(img, imgPos)
                img = smallFont.render("Flamethrower", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 300))
                DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Back", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 4 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 5:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                img = smallFont.render("Back", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 200))
                DISPLAYSURF.blit(img, imgPos)

        elif shopArea == 3:
            maxPos = 4
            img = font.render("- Upgrades & Health - ", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Armor", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 2 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 1:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                if player.armor == 0.5:
                    img = smallFont.render("Max Armor", True, (255, 255, 255))
                else:
                    img = smallFont.render("Cost: $250", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 200))
                DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Health", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 2.5 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 2:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                if player.health == 100:
                    img = smallFont.render("Max Health", True, (255, 255, 255))
                else:
                    img = smallFont.render("Cost: $50", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 200))
                DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Money Upgrade", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 3 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 3:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                if player.moneyUpgrade == 1:
                    img = smallFont.render("Max Upgrade", True, (255, 255, 255))
                else:
                    img = smallFont.render("Cost: $500", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 200))
                DISPLAYSURF.blit(img, imgPos)
            img = smallFont.render("Back", True, (255, 255, 255))
            imgPos = img.get_rect(center=(int(WIDTH / 2), 3.5 * int(HEIGHT / 6)))
            DISPLAYSURF.blit(img, imgPos)
            if pos == 4:
                pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (imgPos.x - 3, imgPos.y - 3, imgPos.width + 6, imgPos.height + 6), 2)
                img = smallFont.render("Back", True, (255, 255, 255))
                imgPos = img.get_rect(center=(1710, 200))
                DISPLAYSURF.blit(img, imgPos)

        elif shopArea == 4:
            start = True


        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    replay = True
    while replay:
        replay = main()