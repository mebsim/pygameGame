import pygame
import math
import random

#  Colors #
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

# Init Pygame #
pygame.init()

# Display Dimensions #
display_width = 500
display_height = 500

# Pygame Variables #
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Shooter')
clock = pygame.time.Clock()

# Images to Load #
bImg = pygame.image.load('Bullet3.png')
sbImg = pygame.image.load('Bullet4.png')
icon = pygame.image.load('Logo3.png')
bg = pygame.image.load('Background2.png')
ammoPack = pygame.image.load('AmmoPack.png')
logo = pygame.image.load('SHOOTER.png')
startButton = pygame.image.load('StartButton.png')
shotgun = pygame.image.load('shotgun.png')
pause = pygame.image.load('pause.png')
quitButton = pygame.image.load('Quit.png')

pygame.display.set_icon(icon)

#  General Variables #
clickr = False
Failed = False
roundOver = 0
numofE = 1
paused = False
titlescreen = True
gameOver = False
chosingMode = False
insanityMode = False
highScore = []
hscoretoprint = 0

#  Player Specific Variables #
px = 250
py = 250
alive = True
score = 0
ammo = 10
ammoL = 6
maxLoad = 6
pistolEquiped = True
shotgunAvailable = False
dx = 0
dy = 0

# Font/text: I got this from this website -- http://www.nerdparadise.com/tech/python/pygame/basics/part5/ #
font = pygame.font.SysFont("timesnewroman", 24)
smallFont = pygame.font.SysFont("timesnewroman", 12)
Instructions = smallFont.render("'r' - Reload | 'c' - Change Weapons | 'wasd' - Movements | click - Shoot",True,(255,255,255))
fontLarge = pygame.font.SysFont("timesnewroman", 50)
fontMedium = pygame.font.SysFont("timesnewroman", 32)
scoreText = font.render("Score", True, (255, 255, 255))
highscoreText = font.render("Highscore", True, (255,255,255))
scoreNumber = font.render(str(score), True, (255,255,255))
pauseMessage = fontLarge.render("PAUSED", True, (255,255,255))
gameOverMessage = fontLarge.render("GAME OVER", True, (255,255,255))
chosingModeMessage = fontLarge.render("CHOOSE", True, (255,255,255))
backtoTitle = fontMedium.render("Main Menu", True, (255,255,255))
quitGame = fontMedium.render("Quit", True, (255,255,255))
startGame = fontMedium.render("Start", True, (255,255,255))
backtoGame = fontMedium.render("Unpause", True, (255,255,255))
classic = fontMedium.render("Classic", True, (255,255,255))
insane = fontMedium.render("Insane", True, (255,255,255))

class Enemy:
    """This is the enemy class, which is used to check for enemy position, draw them, check if they are dead and more."""
    x = [10]
    y = [10]
    drop = [1]
    health = [10]
    checked = False
    click = False

    def revertToOrginal(self):
        self.x = [10]
        self.y = [10]
        self.drop = [1]
        self.health = [10]
        self.checked = False
        self.click = False

    def addEnemy(self, x, y):
        self.x += [x]
        self.y += [y]
        self.health += [10]
        drop = random.randint(0,100)
        if drop >= 1 and drop <= 10:
            drop = 1
        elif drop == 13 or drop == 42:
            drop = 10
        else:
            drop = 0
        self.drop += [drop]

    def move(self, i):
        global px
        global py
        if px < self.x[i]:
            self.x[i] -= 1
        if px > self.x[i]:
            self.x[i] += 1
        if py > self.y[i]:
            self.y[i] += 1
        if py < self.y[i]:
            self.y[i] -= 1

    def main(self):
        global px
        global py
        global ammo
        global ammoL
        global roundOver
        global numofE
        global score
        global alive
        roundOver = False
        for i in range(len(self.x)):
            i -= 1
            if self.health[i] > 0:
                pygame.draw.circle(gameDisplay,red, ((int)(self.x[i]),(int)(self.y[i])), 10)
                self.move(i)
                self.giveHit(i)
                if clickr and alive and ammoL > 0:
                    self.checkhit(i)
            else:
                if self.drop[i] == 1:
                    gameDisplay.blit(ammoPack,(self.x[i],self.y[i]))
                    if px <= self.x[i] + 60 and px >= self.x[i] - 60 and py <= self.y[i] + 60 and py >= self.y[i] - 60:
                        self.drop[i] = 0
                        score += 5
                        ammo += 5
                if self.drop[i] == 10:
                    gameDisplay.blit(shotgun,(self.x[i],self.y[i]))
                    if px <= self.x[i] + 60 and px >= self.x[i] - 60 and py <= self.y[i] + 60 and py >= self.y[i] - 60:
                        global shotgunAvailable
                        shotgunAvailable = True
                        self.drop[i] = 0
                        score += 5
                        ammo += 5
            if self.health[i] > 0:
                roundOver = True
        if insanityMode:
            if roundOver == False:
                numofE += len(self.x)
        else:
            if roundOver == False:
                numofE += 1


    def checkhit(self, i):
        global px
        global py
        global score
        mouse = pygame.mouse.get_pos()
        mx = mouse[0]
        my = mouse[1]
        xDistance = mx - px
        yDistance = my - py
        rad = math.atan2(yDistance, xDistance)
        bx = px
        by = py
        sob = 5
        if pistolEquiped:
            for a in range(100):
                bx += 5 * math.cos(rad)
                by += 5 * math.sin(rad)
                bix = int(bx)
                biy = int(by)
                pygame.draw.circle(gameDisplay, green, (bix, biy), 5)
                if bx <= self.x[i] + 10 and bx >= self.x[i] - 10 and by <= self.y[i] + 10 and by >= self.y[i] - 10 and self.health[i] > 0:
                    self.health[i] -= 10
                    score += 5
                    break
        else:
            for a in range(50):
                bx += 5 * math.cos(rad)
                by += 5 * math.sin(rad)
                bix = int(bx)
                biy = int(by)
                pygame.draw.circle(gameDisplay, green, (bix, biy), sob)
                if bx <= self.x[i] + sob and bx >= self.x[i] - sob and by <= self.y[i] + sob and by >= self.y[i] - sob and self.health[i] > 0:
                    self.health[i] -= 10
                    score += 5
                    break
                sob = 5 + a

    def giveHit(self, i):
        global alive
        global px
        global py
        if self.x[i] < px + 40 and self.x[i] > px - 40 and self.y[i] < py + 40 and self.y[i] > py - 40:
            alive = False

e = Enemy()

# Thanks to http://www.python-course.eu/python3_file_management.php for telling me how to read and write files

def writeFile():
    hsfile = open("Highscore.txt", "w")
    if score > highScore[0]:
        scoretoPrint = str(score) + "\n"
    else:
        scoretoPrint = str(hscoretoprint)
    hsfile.write(scoretoPrint)
    hsfile.close()

def readFile():
    global hscoretoprint
    global highScore
    hsfile = open("Highscore.txt")
    for line in hsfile:
        highScore += [int(line)]
    highScore.sort()
    hscoretoprint = highScore[len(highScore)-1]
    print("HIGHSCORE:",hscoretoprint)
    hsfile.close()

def titleScreen():
    global ammo
    global ammoL
    global chosingMode
    global Failed
    global titlescreen
    readFile()
    gameDisplay.fill(white)
    while titlescreen == True:
        gameDisplay.blit(bg,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(logo, (0,10))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if mouse[0] > 0 and mouse[0] < 200 and mouse[1] > 370 and mouse[1] < 500:
            if click[0] == True:
                ammo = 10
                ammoL = 6
                titlescreen = False
                chosingMode = True
        if mouse[0] > 300 and mouse[0] < 500 and mouse[1] > 370 and mouse[1] < 500:
            if click[0] == True:
                Failed = True
                titlescreen = False
        gameDisplay.blit(quitButton, (300,450))
        gameDisplay.blit(quitButton, (300,430))
        gameDisplay.blit(quitButton, (300,410))
        gameDisplay.blit(quitButton, (300,390))
        gameDisplay.blit(quitButton, (300,370))
        gameDisplay.blit(startButton, (0,450))
        gameDisplay.blit(startButton, (0,430))
        gameDisplay.blit(startButton, (0,410))
        gameDisplay.blit(startButton, (0,390))
        gameDisplay.blit(startButton, (0,370))
        gameDisplay.blit(startGame, (70,410))
        gameDisplay.blit(quitGame, (370,410))
        clock.tick(10)
        pygame.display.update()

timesPaused = 0

def pausemenu():
    global ammo
    global ammoL
    global pistolEquiped
    global shotgunAvailable
    global paused
    global timesPaused
    global titlescreen
    while paused == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    paused = False
        gameDisplay.blit(pauseMessage, (250 - pauseMessage.get_width()/2, 100))
        if timesPaused == 1:
            gameDisplay.blit(pause, (0,0))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if mouse[0] > 0 and mouse[0] < 200 and mouse[1] > 370 and mouse[1] < 500:
            if click[0] == True:
                paused = False
        if mouse[0] > 300 and mouse[0] < 500 and mouse[1] > 270 and mouse[1] < 500:
            if click[0] == True:
                paused = False
                titlescreen = True
                e.revertToOrginal()
                ammo = 10
                ammoL = 6
                pistolEquiped = True
                shotgunAvailable = False
        gameDisplay.blit(quitButton, (300,450))
        gameDisplay.blit(quitButton, (300,430))
        gameDisplay.blit(quitButton, (300,410))
        gameDisplay.blit(quitButton, (300,390))
        gameDisplay.blit(quitButton, (300,370))
        gameDisplay.blit(startButton, (0,450))
        gameDisplay.blit(startButton, (0,430))
        gameDisplay.blit(startButton, (0,410))
        gameDisplay.blit(startButton, (0,390))
        gameDisplay.blit(startButton, (0,370))
        gameDisplay.blit(backtoGame, (50,410))
        gameDisplay.blit(backtoTitle, (330,410))
        clock.tick(10)
        pygame.display.update()
        timesPaused += 1

def GameOver():
    global ammo
    global ammoL
    global pistolEquiped
    global shotgunAvailable
    global gameOver
    global titlescreen
    global Failed
    global alive
    global insanityMode
    global score
    global px
    global py
    global dx
    global dy
    global numofE
    writeFile()
    while gameOver == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    paused = False
        gameDisplay.blit(gameOverMessage, (250 - gameOverMessage.get_width()/2, 100))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if mouse[0] > 0 and mouse[0] < 200 and mouse[1] > 370 and mouse[1] < 500:
            if click[0] == True:
                score = 0
                gameOver = False
                titlescreen = True
                e.revertToOrginal()
                ammo = 10
                ammoL = 6
                pistolEquiped = True
                shotgunAvailable = False
                alive = True
                insanityMode = False
                px = 250
                py = 250
                dx = 0
                dy = 0
                numofE = 1
        if mouse[0] > 300 and mouse[0] < 500 and mouse[1] > 270 and mouse[1] < 500:
            if click[0] == True:
                Failed = True
                gameOver = False
        gameDisplay.blit(quitButton, (300,450))
        gameDisplay.blit(quitButton, (300,430))
        gameDisplay.blit(quitButton, (300,410))
        gameDisplay.blit(quitButton, (300,390))
        gameDisplay.blit(quitButton, (300,370))
        gameDisplay.blit(startButton, (0,450))
        gameDisplay.blit(startButton, (0,430))
        gameDisplay.blit(startButton, (0,410))
        gameDisplay.blit(startButton, (0,390))
        gameDisplay.blit(startButton, (0,370))
        gameDisplay.blit(backtoTitle, (30,410))
        gameDisplay.blit(quitGame, (370,410))
        clock.tick(10)
        pygame.display.update()

def choseGameMode():
    global ammo
    global ammoL
    global insanityMode
    global chosingMode
    gameDisplay.fill(white)
    while chosingMode == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    paused = False
        gameDisplay.blit(bg,(0,0))
        gameDisplay.blit(chosingModeMessage, (250 - chosingModeMessage.get_width()/2, 100))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if mouse[0] > 0 and mouse[0] < 200 and mouse[1] > 370 and mouse[1] < 500:
            if click[0] == True:
                chosingMode = False
                e.revertToOrginal()
                insanityMode = True
                ammo = 10
                ammoL = 6
        if mouse[0] > 300 and mouse[0] < 500 and mouse[1] > 270 and mouse[1] < 500:
            if click[0] == True:
                chosingMode = False
                e.revertToOrginal()
                insanityMode = False
                ammo = 10
                ammoL = 6
        gameDisplay.blit(startButton, (300,450))
        gameDisplay.blit(startButton, (300,430))
        gameDisplay.blit(startButton, (300,410))
        gameDisplay.blit(startButton, (300,390))
        gameDisplay.blit(startButton, (300,370))
        gameDisplay.blit(startButton, (0,450))
        gameDisplay.blit(startButton, (0,430))
        gameDisplay.blit(startButton, (0,410))
        gameDisplay.blit(startButton, (0,390))
        gameDisplay.blit(startButton, (0,370))
        gameDisplay.blit(insane, (50,410))
        gameDisplay.blit(classic, (350,410))
        clock.tick(10)
        pygame.display.update()

def player():
    global px
    global py
    pygame.draw.circle(gameDisplay,black, (px,py), 50)

def displayAmmo():
    for a in range(ammoL):
        if pistolEquiped:
            gameDisplay.blit(bImg,(400,500 - (a * 35)))
        else:
            gameDisplay.blit(sbImg, (400,500 - (a * 35)))

def reload():
    global ammoL
    global ammo
    global maxLoad
    if ammoL <= maxLoad and ammo > 0:
        ammo -= 1
        ammoL += 1

while not Failed:
    if titlescreen == True:
        titleScreen()
    if chosingMode == True:
        choseGameMode()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            writeFile()
            Failed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                dx = -5
            elif event.key == pygame.K_d:
                dx = 5
            if event.key == pygame.K_w:
                dy = - 5
            elif event.key == pygame.K_s:
                dy = 5
            if event.key == pygame.K_r:
                reload()
            if event.key == pygame.K_c:
                if shotgunAvailable == True:
                    if pistolEquiped:
                        pistolEquiped = False
                    else:
                        pistolEquiped = True
        if event.type == pygame.MOUSEBUTTONUP:
            clickr = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickr = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                dx = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                dy = 0
            if event.key == pygame.K_p:
                timesPaused = 0
                paused = True
                pausemenu()
    px += dx
    py += dy
    highscoreNumber = font.render(str(hscoretoprint), True, (255,255,255))
    gameDisplay.fill(white)
    gameDisplay.blit(bg, (0, 0))
    if alive:
        player()
    if alive != True:
        gameOver = True
        GameOver()
    if clickr and alive and ammoL > 0:
        ammoL -= 1
    if roundOver == False:
        print("ROUND OVER, NEXT ROUND: ", numofE, "------------------------------------------------------------------------------------------------------------------------------------------")
        for a in range(numofE):
            side = random.randint(1,4)
            #print(side)
            ex = 0
            ey = 0
            if side == 1:
                ex = random.randint(0, 500)
                ey = random.randint(-200,-10)
            elif side == 2:
                ex = random.randint(0, 500)
                ey = random.randint(510,700)
            elif side == 3:
                ex = random.randint(-200, -10)
                ey = random.randint(0,500)
            else:
                ex = random.randint(510, 700)
                ey = random.randint(0, 500)
            e.addEnemy(ex, ey)
        roundOver = True
    gameDisplay.blit(scoreText,(400, 10))
    gameDisplay.blit(scoreNumber,(460,10))
    gameDisplay.blit(highscoreText,(10, 10))
    gameDisplay.blit(highscoreNumber,(110,10))
    e.main()
    displayAmmo()
    clickr = False
    if highScore[0] <= score:
        writeFile()
        highScore[0] = score
        hscoretoprint = score
    clock.tick(30)
    gameDisplay.blit(Instructions, (10,480))
    pygame.display.update()
    scoreNumber = font.render(str(score), True, (255,255,255))
    # Thanks to this website (https://pythonprogramming.net/pygame-python-3-part-1-intro/) for giving the basic tutorials for making this game
pygame.quit()
quit()
