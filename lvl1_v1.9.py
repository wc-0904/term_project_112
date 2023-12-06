from cmu_graphics import *
from PIL import Image
import math
import random
import time

# **CITATION**
# I've taken inspiration from a number of games and tutorials online
# I've also used sprites found online
# Please check the text file included in the folder for all the citations
# This game was insprired by the orignial game "Deadbolt"
# https://www.youtube.com/watch?v=SbcZ0GtPsvI&t=1733s
# I took many small ideas from this tutorial playlist:
# https://youtube.com/playlist?list=PLjcN1EyupaQm20hlUE11y9y8EY2aXLpnv&si=d5wfh5x85H8WbyaK

def onAppStart(app):
    app.width = 288*5
    app.height = 192*5

    # for the timer
    app.begin = 0
    app.end = 0

    app.backgroundImage = CMUImage(Image.open('images/background.png'))
    app.menuBackground = CMUImage(Image.open('images/menu_background.png'))
    app.painting1 = CMUImage(Image.open('images/painting1.png'))
    app.decor = CMUImage(Image.open('images/decor.png'))

    # welcome screen stuff
    app.buttonW = 600
    app.buttonH = 100
    app.lvl1Fill = 'darkBlue'
    app.InstrFill = 'darkGreen'
    app.lvl1Intersect = False
    app.InstrIntersect = False
# --------------game over stuff-------------------------------------------------
    app.gameOver_background = CMUImage(Image.open('images/background.png'))
    app.retryIntersect = False
    app.prevLvl = None
    app.menuIntersect = False

#--------------------lvl1 stuff-------------------------------------------------
    # lvl1 background
    app.lvl1_background = None

    # set ground and player Y levels
    app.lvl1groundList = []
    app.lvl1ground1 = None
    app.lvl1ground2 = None
    app.pGround = None
    
    # player and enemy instances on level creation
    app.player = None
    app.lvl1enemyList = []
    app.lvl1enemy1 = None
    app.lvl1enemy2 = None
    app.lvl1enemy3 = None

    # set walls
    app.lvl1vWallList = []
    app.lvl1vWall1 = None
    app.lvl1vWall2 = None
    app.lvl1vWall3 = None
    app.lvl1vWall4 = None

    # set stairs
    app.lvl1stairList = []
    app.lvl1stair1 = None
    app.lvl1stair2 = None
    app.lvl1stair3 = None
    app.lvl1stair4 = None


    # set doors
    app.lvl1doorList = []
    app.lvl1door2 = None
    app.lvl1door1 = None
    app.lvl1door3 = None
#-------------------------------------------------------------------------------
    # cursor stuff
    app.c1x = app.width/2       #cursor inner circle X
    app.c1y = app.height/2      #cursor inner circle Y
    app.c2x = app.width/2       #cursor outer circle X
    app.c2y = app.height/2      #cursor outer circle Y
    app.c2r = 10                #cursor outer circle radius
    app.lastMouseX = app.c1x
    app.lastMouseY = app.c1y

    # **CITATION**
    # based on Mike's 15-112 lecture demos
    # sprite animation stuff
    app.spriteCounter = 0
    app.stepCount = 0
    
    # **CITATION**
    # took inspiration from previous 15-112 tutorials for sidescrolling
    # throughout the app
    # https://www.cs.cmu.edu/~112-f22/notes/notes-animations-part4.html#sidescrollerExamples
    
    # side scrolling stuff and player width
    app.scrollX = 0
    app.scrollMargin = 250

    # bullet list, stores all the current bullets in-game
    app.bulletList = []

#---------------------------CLASSES---------------------------------------------
# **CITATION**
# took inspiration from the videos below to create the bullet class
# https://www.youtube.com/watch?v=JmpA7TU_0Ms
# https://www.youtube.com/watch?v=glah2YjuY2A
class Bullet():

    def __init__(self, x, y, char, angle):
        
        # took inspiration from 15-112 class lecture demos for bullet physics
        # position, velocity, and acceleration
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.ddx = 0
        self.ddy = 0
        self.angle = angle
        self.diameter = 10
        self.r = self.diameter/2
        self.bounds = (self.x-self.r, self.y+self.r, self.x+self.r, self.y-self.r)
        self.char = char
        # for this, we know our stepsPerSec is 30, but other wise we'd multiply by app.stepsPerSecond
        self.timer = 2*30
        
        # homing stuff
        self.bulletVector = (0,0)
        self.origin = (0, 0)

        # set bullet pattern based on player/enemy here
        if char == 'player':
            # player bullet goes straight, no gravity
            # sets dx and dy based on angle
            self.pattern = 'straight'
            self.dx = math.cos(self.angle)*15
            self.dy = -(math.sin(self.angle)*15)
            self.ddy = 0
       
        # dx and dy are set similarly below
        if char == 'enemy1':
            self.pattern = 'parabolic'
            self.dx = math.cos(self.angle)*15
            self.dy = -(math.sin(self.angle)*15)
            self.ddy = 0.1
            self.playerSeen = False
            self.bulletVector = (self.dx, self.dy)
            self.timer = 3*30
            self.origin = (self.x, self.y)
        
        if char == 'enemy2':
            self.pattern = 'sinusoidal'
            self.dx = math.cos(self.angle)*10
            self.dy = -(math.sin(self.angle)*50)
            self.ddy = 0.1
            self.ddx = -0.05
            self.playerSeen = False
            self.bulletVector = (self.dx, self.dy)
            self.timer = 3*30
            self.origin = (self.x, self.y)

        if char == 'enemy3':
            self.pattern = 'parabolic'
            self.dx = math.cos(self.angle)*15
            self.dy = -(math.sin(self.angle)*15)
            self.ddy = 0.1
            self.playerSeen = False
            self.bulletVector = (self.dx, self.dy)
            self.timer = 3*30
            self.origin = (self.x, self.y)
    
    # **CITATION**
    # I got some ideas about using vectors like this from OH
    # homing function for enemy1 and enemy3
    def homing(self, app):
        if self.pattern == 'parabolic':
            playerVector = (app.player.x-app.scrollX-self.x, app.player.y-self.y)
            newVect = (playerVector[0]-self.bulletVector[0], playerVector[1]-self.bulletVector[1])
            normVect = normalizeVector(newVect)
            size = vectorSize(self.bulletVector)
            self.bulletVector = (normVect[0]*size, normVect[1]*size)
            self.dx = 0.5*self.bulletVector[0]
        
        if self.pattern == 'sinusoidal':
            if (self.y >= app.player.y+15):
                self.dy = -5
                self.ddy *= -1
            elif  (self.y <= app.player.y-15):
                self.dy = 5
                self.ddy *= -1
            

    # draws the bullet
    def draw(self):
        drawCircle(self.x, self.y, self.r, fill='blue')
    

    # step function
    def step(self, app):
        # **CITATION**
        # inspiration from mike's lecture demo
        # bullet physics stuff 
        self.x += self.dx
        self.y += self.dy
        if self.dx < 0:
            self.dx += self.ddx*(-1)
        else:
            self.dx += self.ddx
        self.dy += self.ddy
        self.bounds = (self.x-self.r, self.y+self.r, self.x+self.r, self.y-self.r)

        # decrement timer every step
        self.timer -= 1

        # 'kills' enemy
        for enemy in app.lvl1enemyList:
            if ((enemy.x-25-app.scrollX < self.x < enemy.x+25-app.scrollX) and
                (enemy.y-25 < self.y < enemy.y+25)) and self.char == 'player':
                app.lvl1enemyList.remove(enemy)
                app.bulletList.remove(self)
        self.x += (app.scrollX)
        checkWallHit(app, self)
        self.x -= (app.scrollX)
        
        if self.pattern != 'straight':
            self.homing(app)

        # self deletion logic
        if (self.timer == 0):
            if self in app.bulletList:
                app.bulletList.remove(self)
        

# **CITATION**        
# took inspiration from this tutorial to create player class and overall code
# organization: https://youtube.com/playlist?list=PLjcN1EyupaQm20hlUE11y9y8EY2aXLpnv&si=d5wfh5x85H8WbyaK
class Player():

    def __init__(self, type, x, y):

        # set the player location
        self.x = x
        self.y = y

        # player bounds and type
        self.width = 50
        self.height = 50
        self.type = type
        self.bounds = (self.x-25, self.y-25, self.x+25, self.y+25)
        self.health = 1
        
        
        # enemy attributes
        self.playerSeen = False
        self.shotTimer = 1*30
        self.anchor = self.x+100
        

        # **CITATION**
        # original sprites created using www.piskelapp.com
        # sprite animation stuff
        # name both idle and running animation
        self.imageIdle = (Image.open(f'images/{type}_idle.png')) #dont have this animation yet
        self.imageRunningRight = (Image.open(f'images/{type}_running_right.png'))
        self.imageRunningLeft = (Image.open(f'images/{type}_running_left.png'))

        # set direction values
        if self.type != 'player':
            self.movingRight = True
            self.movingLeft = False
            self.idling = False
        else:
            self.movingRight = False
            self.movingLeft = False
            self.idling = True
            self.health = 3

        # this is the list that'll contatin the current animation
        self.animationList = []
    
    # draw function to draw the player
    def draw(self, app):
        if self.animationList != []:
            currSprite = self.animationList[app.spriteCounter]
            drawImage(currSprite, self.x-25-app.scrollX, self.y-25)
    
    # this checks what movement the player is doing (running or idling)
    def currentMovement(self, key, app):

        # you would add the "running right" animation here
        if key == 'd':
            self.movingRight = True
            self.movingLeft = False
            self.idling = False
            img = self.imageRunningRight
            # img = Image.open(self.imageRunningRight)
            self.animationList = []
            for i in range(6):
                sprite = CMUImage(img.crop((50*i, 0, 50*(i+1), 50)))
                self.animationList.append(sprite)
        
        # you would add the "running left" animation here
        elif key == 'a':
            self.movingRight = False
            self.movingLeft = True
            self.idling = False
            img = (self.imageRunningLeft)
            self.animationList = []
            for i in range(6):
                sprite = CMUImage(img.crop((50*i, 0, 50*(i+1), 50)))
                self.animationList.append(sprite)
        
        # you would add the "idling" animation here
        elif key == 'idle_right':
            self.movingRight = True
            self.movingLeft = False
            self.idling = True
            img = (self.imageIdle)
            self.animationList = []
            for i in range(6):
                sprite = CMUImage(img.crop((50*i, 0, 50*(i+1), 50)))
                self.animationList.append(sprite)
        
        elif key == 'idle_left':
            self.movingRight = False
            self.movingLeft = True
            self.idling = True
            right_img = (self.imageIdle)
            img = right_img.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
            self.animationList = []
            for i in range(6):
                sprite = CMUImage(img.crop((50*i, 0, 50*(i+1), 50)))
                self.animationList.append(sprite)

        # function to account for sidescrolling (sidescrolling inspiration cited above)
        makePlayerVisible(app, app.player)

    def getPosition(self):
        return [self.x, self.y]

    def setPlayerBounds(self, app):
        self.bounds = (self.x-25-5-app.scrollX, self.y-25,
                       self.x+25+5-app.scrollX, self.y+25)
    

    # bullet drawing function, this only appends to the bullet list
    def drawBullet(self, app, mouseX, mouseY):
        if self.type == 'player':
            xDistance = (mouseX - (self.x-app.scrollX))
            yDistance = -(mouseY - self.y)
            bulletAngle = math.atan2(yDistance, xDistance)
            app.bulletList.append(Bullet(self.x-app.scrollX, self.y, self.type, bulletAngle))
        else:
            xDistance = (mouseX - (self.x-app.scrollX))
            yDistance = -(mouseY - self.y)
            bulletAngle = math.atan2(yDistance, xDistance)
            bullet = Bullet(self.x-app.scrollX, self.y-50, self.type, bulletAngle)
            bullet.bulletVector = (bullet.dx, bullet.dy)
            app.bulletList.append(bullet)

# vertical wall class, to create and place vertical walls throughout levels
# this make the creation of custom levels easier
class vWall():
    
    def __init__(self, name, botX, botY, topX, topY):
        self.name = name
        self.botX = botX
        self.botY = botY
        self.topX = topX
        self.topY = topY
        self.bounds = (self.botX-2.5, self.botY, self.topX+2.5, self.topY)

    def drawWall(self, app):
        drawLine(self.botX-app.scrollX, self.botY, 
                 self.topX-app.scrollX, self.topY, 
                 lineWidth = 5)

    def wallStep(self):
        self.bounds = (self.botX-2.5, self.botY, self.topX+2.5, self.topY)

    def __repr__(self):
        return self.name

# class to create and place stairs throughout the map
class Stair():

    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

        self.bounds = (self.x-5, self.y-22.5, self.x+5, self.y+22.5)
    
    def drawStair(self, app):
        if self.type == 'up':
            drawRect(self.x-17.5-app.scrollX, self.y-27.5, 35, 55, 
                     fill='black',border='black', borderWidth=1, opacity=80)
            drawLine(self.x+17.5-app.scrollX, self.y-27.5, self.x-17.5-app.scrollX, self.y+27.5)
            drawPolygon(self.x+17.5-app.scrollX, self.y-27.5, self.x-17.5-app.scrollX, self.y+27.5, self.x+17.5-app.scrollX, self.y+27.5, fill='black')
        if self.type == 'down':
            drawRect(self.x-17.5-app.scrollX, self.y-27.5, 35, 55, 
                     fill='black',border='black', borderWidth=1)
            
    # Took inspiration from older 15-112 websites for collision logic below:
    # https://www.cs.cmu.edu/~112-f22/notes/notes-animations-part4.html#sidescrollerExamples
    # for collision detection
    def setStairBounds(self, app):
        self.bounds = (self.x-5-app.scrollX, self.y-22.5,
                       self.x+5-app.scrollX, self.y+22.5)

# creates and draws door instances
class Door():

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.open = False
        self.bounds = (self.x, self.y-52.5, self.x+50, self.y)
    
    def drawDoor(self, app):
        if self.open:
            drawRect(self.x-app.scrollX-2.5, self.y-52.5, 50, 52.5, fill='brown', opacity=90, border='brown', borderWidth=5)
        else:
            drawLine(self.x-app.scrollX, self.y, self.x-app.scrollX, self.y-52.5, fill='brown', lineWidth=5)
    
    # # Took inspiration from older 15-112 websites for collision logic below:
    # https://www.cs.cmu.edu/~112-f22/notes/notes-animations-part4.html#sidescrollerExamples
    # for collision detection
    def setDoorBounds(self, app):
        self.bounds = (self.x-app.scrollX, self.y-52.5,
                       self.x+50-app.scrollX, self.y)

#-------------------------------------------------------------------------------


#------------------------Global Functions---------------------------------------

# stores all information about level 1, "loads" when called
def loadLvl1(app):
    # start timer
    app.begin = time.time()
    # lvl1 background
    app.lvl1_background = CMUImage(Image.open('images/lvl1_background.png'))

    # set ground and player Y levels
    app.lvl1groundList = []
    app.lvl1ground1 = 3*app.height/4
    app.lvl1ground2 = app.lvl1ground1-225
    app.lvl1groundList.append(app.lvl1ground1)
    app.lvl1groundList.append(app.lvl1ground2)
    app.pGround = app.lvl1groundList[0]
    
    # player and enemy instances on level creation
    app.player = Player('player', 100, app.pGround - 25 - 2.5)
    app.lvl1enemyList = []
    app.lvl1enemy1 = Player('enemy1', 660+260+260, app.lvl1ground1 - 25-2.5)
    app.lvl1enemy2 = Player('enemy2', 660+260, app.lvl1ground1 - 25-2.5)
    app.lvl1enemy3 = Player('enemy3', 660, app.lvl1ground2 - 25-2.5)
    app.lvl1enemy4 = Player('enemy3', 660+260+285, app.lvl1ground2 - 25-2.5)
    app.lvl1enemy5 = Player('enemy1', 425, app.lvl1ground1 - 25-2.5)
    app.lvl1enemyList.append(app.lvl1enemy1)
    app.lvl1enemyList.append(app.lvl1enemy2)
    app.lvl1enemyList.append(app.lvl1enemy3)
    app.lvl1enemyList.append(app.lvl1enemy4)
    app.lvl1enemyList.append(app.lvl1enemy5)

    # set walls
    app.lvl1vWallList = []
    app.lvl1vWall1 = vWall('wall1', 400, app.lvl1ground1-50-2.5, 400, app.lvl1ground1 - 450)
    app.lvl1vWall2 = vWall('wall2', 660, app.lvl1ground1-50-2.5, 660, app.lvl1ground2)
    app.lvl1vWall3 = vWall('wall3', 1180, app.lvl1ground2-50-2.5, 1180, app.lvl1ground1 - 450)
    app.lvl1vWall4 = vWall('wall4', 1440, app.lvl1ground1, 1440, app.lvl1ground1 - 450)
    app.lvl1vWallList.append(app.lvl1vWall1)
    app.lvl1vWallList.append(app.lvl1vWall2)
    app.lvl1vWallList.append(app.lvl1vWall3)
    app.lvl1vWallList.append(app.lvl1vWall4)

    # set stairs
    app.lvl1stairList = []
    app.lvl1stair1 = Stair(530, app.lvl1ground1-27.5-2.5, 'up')
    app.lvl1stair2 = Stair(530, app.lvl1ground2-27.5-2.5, 'down')
    app.lvl1stair3 = Stair(1180+130, app.lvl1ground1-27.5-2.5, 'up')
    app.lvl1stair4 = Stair(1180+130, app.lvl1ground2-27.5-2.5, 'down')
    app.lvl1stairList.append(app.lvl1stair1)
    app.lvl1stairList.append(app.lvl1stair2)
    app.lvl1stairList.append(app.lvl1stair4)
    app.lvl1stairList.append(app.lvl1stair3)

    # set doors
    app.lvl1doorList = []
    app.lvl1door1 = Door('door1', 400, app.lvl1ground1)
    app.lvl1door2 = Door('door2', 660, app.lvl1ground1)
    app.lvl1door3 = Door('door3', 1180, app.lvl1ground2)
    app.lvl1doorList.append(app.lvl1door1)
    app.lvl1doorList.append(app.lvl1door2)
    app.lvl1doorList.append(app.lvl1door3)

    # calls to idle animations
    app.player.currentMovement('idle_right', app)
    for enemy in app.lvl1enemyList:
        enemy.currentMovement('idle_right', app)

# helper function
def normalizeVector(vector):
    size = (vector[0]**2 + vector[1]**2)**0.5
    normalized = (vector[0]/size, vector[1]/size)
    return normalized

# helper function
def vectorSize(vector):
    return (vector[0]**2 + vector[1]**2)**0.5

# accounts for sidescrolling (for sidescrolling citation, see top)
def makePlayerVisible(app, player):
        # scroll to make player visible as needed
        if player.type == 'player': 
            if (app.player.x < app.scrollX + app.scrollMargin):
                app.scrollX = app.player.x - app.scrollMargin
            if (app.player.x > app.scrollX + app.width - app.scrollMargin):
                app.scrollX = app.player.x - app.width + app.scrollMargin

# # Took inspiration from older 15-112 websites for collision logic below:
# https://www.cs.cmu.edu/~112-f22/notes/notes-animations-part4.html#sidescrollerExamples
# for collision detection
def boundsIntersect(boundsA, boundsB):
        # return l2<=r1 and t2<=b1 and l1<=r2 and t1<=b2
        (ax0, ay0, ax1, ay1) = boundsA
        (bx0, by0, bx1, by1) = boundsB
        return ((ax1 >= bx0) and (bx1 >= ax0) and
                (ay1 >= by0) and (by1 >= ay0))

#function assigns cursor center to mouse location
def cursorUpdate(app, mouseX, mouseY, distFromRef):
    app.c1x = app.c2x = mouseX
    app.c1y = app.c2y = mouseY

    # this threshold number (150) below determines how far the cursor goes without changing shape
    # this has to be updated along with the number that divides distFromRef,
    # divide by the 'threshold/10'
    if distFromRef > 150:                
        app.c2r = distFromRef/15         
    else:
        app.c2r = 10

# collision logic for walls
def checkWallHit(app, object):
    if type(object) == Player:
        for vWall in app.lvl1vWallList:
            if ((object.x+object.width/2 >= vWall.botX) 
                and (object.x-object.width/2 <= vWall.botX) 
                and (object.y-object.height/2 >= vWall.topY)
                and (object.y+object.height/2 <= vWall.botY)):
                return True
    if type(object) == Bullet:
        for vWall in app.lvl1vWallList:
            if ((distance(object.x, object.y, vWall.botX, object.y) <= 
                 object.diameter/2+5) and 
                 (object.y >= vWall.topY and object.y <= vWall.botY)):
                object.dx *= -1
                return True
            if ((object.x > app.lvl1vWallList[0].botX) and 
                (object.y +10 >= app.pGround or app.pGround-225 >= object.y -10)):
                object.dy *= -1
                return True
        
        for door in app.lvl1doorList:
            if not door.open:
                if ((distance(object.x, object.y, door.x, object.y) <= 
                    object.diameter/2+5) and 
                    (object.y >= door.y-52.5 and object.y <= door.y)):
                    object.dx *= -1
                    return True

# collision logic for doors
def checkDoorHit(app, object):
    for door in app.lvl1doorList:
        if not door.open:
            if ((object.x+25 >= door.x) 
             and (object.x-25 <= door.x)
             and (object.y-25 >= door.y-52.5)
             and (object.y+25 <= door.y)):
                return True
    return False
    
#helper
def distance(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y0-y1)**2)**0.5

# used to draw buttons for the menus
def drawButton(label, x, y, width, height, color):
    drawRect(x-width/2, y-height/2, width, height, border='black', borderWidth=5, fill=color)
    drawLabel(label, x, y, font='monospace', size=80)
# ------------------------------------------------------------------------------


# **CITATION**
# Based on screens logic from Mike's 15-112 lecture demo
# -----------------------lvl1 Screen--------------------------------------------
def lvl1_redrawAll(app):

    # draw backgrounds
    drawImage(app.backgroundImage, 0, 0)
    drawImage(app.lvl1_background, 400-app.scrollX, app.lvl1ground1-450)
    drawImage(app.painting1, 800-app.scrollX, app.lvl1ground1-160)
    drawImage(app.decor, 1200-app.scrollX, app.lvl1ground1-160)
    drawImage(app.decor, 500-app.scrollX, app.lvl1ground2-160)
    drawImage(app.decor, 1000-app.scrollX, app.lvl1ground2-160)
    drawImage(app.painting1, 1200-app.scrollX, app.lvl1ground2-160)

    # drawing the "base ground"
    drawLine(0, app.lvl1ground1, app.width, app.lvl1ground1, lineWidth = 5)

    # ---------------******LEVEL SPECIFIC******---------------------------------
    # draw vertical walls
    for vWall in app.lvl1vWallList:
        vWall.drawWall(app)

    # draw stairs
    for stair in app.lvl1stairList:
        stair.drawStair(app)

    # draw doors
    for door in app.lvl1doorList:
        door.drawDoor(app)

    # draw floor 1, floor 2, and roof
    drawLine(400-app.scrollX, app.lvl1ground1, 1440-app.scrollX, app.lvl1ground1, lineWidth = 5)
    drawLine(400-app.scrollX, app.lvl1ground2, 1440-app.scrollX, app.lvl1ground2, lineWidth = 5)
    drawLine(400-app.scrollX-2.5, app.lvl1ground1-450, 1440-app.scrollX+2.5, app.lvl1ground1-450, lineWidth = 5)
    
    # underground
    drawRect(0, app.lvl1ground1, app.width, app.height-app.lvl1ground1, fill='black')

    # draw player/enemies
    app.player.draw(app)
    
    for enemy in app.lvl1enemyList:
        enemy.draw(app)
    
    # draw bullets
    for bullet in app.bulletList:
        bullet.draw()
    # --------------------------------------------------------------------------
    #draws cursor inner & outer circle
    drawCircle(app.c1x, app.c1y, 3, fill='darkRed', border=None)          
    drawCircle(app.c2x, app.c2y, app.c2r, fill=None, border='darkRed') 

def lvl1_onMouseMove(app, mouseX, mouseY):
    #'remembers' last mouse location when moving
    app.lastMouseX = mouseX
    app.lastMouseY = mouseY

def lvl1_onMouseDrag(app, mouseX, mouseY):
    #'remembers' last mouse location when dragging
    app.lastMouseX = mouseX
    app.lastMouseY = mouseY

def lvl1_onMousePress(app, mouseX, mouseY):

    # makes sure player faces the same way as bullet is shot
    if app.player.getPosition()[0] >= mouseX+app.scrollX:
        app.player.currentMovement('idle_left', app)
    else:
        app.player.currentMovement('idle_right', app)
    app.player.drawBullet(app, mouseX, mouseY)

def lvl1_onStep(app):
    # update player postion, distance from player to cursor, and update cursor size on every step
    playerPosition = app.player.getPosition()
    distFromPlayer = distance(app.c2x+app.scrollX,app.c2y, playerPosition[0], playerPosition[1])
    cursorUpdate(app, app.lastMouseX, app.lastMouseY, distFromPlayer)

    # updating spriteCounter as required (controls the sprite fps)
    app.stepCount += 1
    if (app.stepCount%3 == 0):
        app.spriteCounter = (1+app.spriteCounter) % len(app.player.animationList)
    
    # update the bullet
    for bullet in app.bulletList:
        bullet.step(app)

        # "damages" the player
        if bullet.char != 'player' and ((app.player.x-25-app.scrollX < bullet.x < app.player.x+25-app.scrollX) and
            (app.player.y-25 < bullet.y < app.player.y+25)):
            app.player.health -= 1
            if bullet.timer != 0:
              app.bulletList.remove(bullet)
        # sets to game over screen
        if app.player.health <= 0:
            setActiveScreen('gameOver')
            app.prevLvl = 'lvl1'

    # logic for when the enemy can "see" the player
    for enemy in app.lvl1enemyList:
        if (((app.player.x-app.scrollX <= enemy.x-app.scrollX and enemy.movingLeft) or
                (app.player.x-app.scrollX >= enemy.x-app.scrollX and enemy.movingRight)) and
                (app.player.y == enemy.y)):
                if distance(app.player.x, app.player.y, enemy.x, enemy.y) < 300:
                    enemy.playerSeen = True
        else:
            enemy.playerSeen = False

        # enemy shooting logic
        if enemy.playerSeen:
            if enemy.shotTimer == 0:
                if enemy.type == 'enemy1':
                    enemy.drawBullet(app, random.randint(0, app.width), random.randint(app.pGround-225, app.pGround))
                    enemy.shotTimer = 3*30
                if enemy.type == 'enemy2' or enemy.type == 'enemy3':
                    enemy.drawBullet(app, app.player.x-app.scrollX, app.player.y)
                    enemy.shotTimer = 3*30
            else:
                enemy.shotTimer -= 1
        
        # this sets the enemies' set path when player isn't seen
        else:
            if ((enemy.x-app.scrollX <= enemy.anchor-app.scrollX) or 
                (enemy.x-app.scrollX < enemy.anchor-app.scrollX+100)) and enemy.movingRight:
                enemy.x += 5
                enemy.currentMovement('d', app)
            else: enemy.currentMovement('a', app)
            if ((enemy.x-app.scrollX >= enemy.anchor-app.scrollX) or 
                (enemy.x-app.scrollX > enemy.anchor-app.scrollX-100)) and enemy.movingLeft:
                enemy.x -= 5
                enemy.currentMovement('a',app)
            else: enemy.currentMovement('d', app)
    
    # updates stair bounds
    for stair in app.lvl1stairList:
        stair.setStairBounds(app)
    
    # updates door bounds
    for door in app.lvl1doorList:
        door.setDoorBounds(app)
    
    # updates player bounds
    app.player.setPlayerBounds(app)

    if app.lvl1enemyList == []:
        app.end = time.time()
        app.prevLvl = 'lvl1'
        setActiveScreen('win')

    
def lvl1_onKeyHold(app, keys):

    #these update the player location
    if ('d' in keys) and ('a' in keys):
        app.player.currentMovement('idle_right', app)
    elif 'd' in keys:
        app.player.x += 10
        if (not checkWallHit(app, app.player)) and (not checkDoorHit(app, app.player)):
            app.player.currentMovement('d', app)
        else:
            app.player.x -=10
    elif 'a' in keys:
        app.player.x -= 10
        if (not checkWallHit(app, app.player)) and (not checkDoorHit(app, app.player)):
            app.player.currentMovement('a', app)
        else:
            app.player.x += 10

def lvl1_onKeyPress(app, key):
    # pause screen
    if key == 'p':
        app.prevLvl = 'lvl1'
        setActiveScreen('pause')            

def lvl1_onKeyRelease(app, key):

    # makes sure player is facing the right direction when stopping movememnt
    if (key == 'd'):
        app.player.currentMovement('idle_right', app)
    elif (key == 'a'):
        app.player.currentMovement('idle_left', app)
    
    # allows players to go upstairs or downstairs
    if (key == 'w'):
        for stair in app.lvl1stairList:
            if boundsIntersect(app.player.bounds, stair.bounds):
                if stair.type == 'up':
                    app.pGround = app.lvl1groundList[app.lvl1groundList.index(app.pGround)+1]
                    app.player.y -= 225
    if (key == 's'):
        for stair in app.lvl1stairList:
            if boundsIntersect(app.player.bounds, stair.bounds):
                if stair.type == 'down':
                    app.pGround = app.lvl1groundList[app.lvl1groundList.index(app.pGround)-1]
                    app.player.y += 225
    
    # pressing e to open doors
    if (key == 'e'):
        for door in app.lvl1doorList:
            if boundsIntersect(app.player.bounds, door.bounds):
                door.open = not door.open

    
# ------------------------------------------------------------------------------


# **CITATION**
# Based on screens logic from Mike's 15-112 lecture demo
# ---------------------Main Menu------------------------------------------------

def menu_redrawAll(app):
    drawImage(app.menuBackground, 0, 0)
    drawButton('Level 1', 3*app.width/4, app.height/3, app.buttonW, app.buttonH, app.lvl1Fill)
    drawButton('Instructions', 3*app.width/4, 2*app.height/3, app.buttonW, app.buttonH, app.InstrFill)

    #draws cursor inner & outer circle
    drawCircle(app.c1x, app.c1y, 3, fill='darkRed', border=None)          
    drawCircle(app.c2x, app.c2y, app.c2r, fill=None, border='darkRed') 

def menu_onMouseMove(app, mouseX, mouseY):
    app.c1x, app.c2x = mouseX, mouseX
    app.c1y, app.c2y = mouseY, mouseY

    if (3*app.width/4 - app.buttonW/2 < mouseX < 3*app.width/4 + app.buttonW/2):
        if (app.height/3 - app.buttonH/2 < mouseY < app.height/3 + app.buttonH/2):
            app.lvl1Fill = 'orange'
            app.lvl1Intersect = True
        else: app.lvl1Fill, app.lvl1Intersect = 'darkBlue', False
        if (2*app.height/3 - app.buttonH/2 < mouseY < 2*app.height/3 + app.buttonH/2):
            app.InstrFill = 'orange'
            app.InstrIntersect = True
        else: app.InstrFill, app.InstrIntersect = 'darkGreen', False
    else: 
        app.lvl1Fill, app.InstrFill = 'darkBlue', 'darkGreen'
        app.lvl1Intersect, app.InstrIntersect = False, False

def menu_onMousePress(app, mouseX, mouseY):
    if app.lvl1Intersect:
        loadLvl1(app)
        setActiveScreen('lvl1')
    if app.InstrIntersect:
        setActiveScreen('instructions')
        pass

# ------------------------------------------------------------------------------

# -----------------------instructions screen------------------------------------
def instructions_redrawAll(app):
    drawImage(app.backgroundImage, 0, 0)
    drawRect(0,0,app.width,app.height, fill='black', opacity=85)
    drawLabel("Your goal is to eliminate all the enemies.", app.width/2, app.height/3, font='monospace', fill='white', size=25, bold=True)
    drawLabel("When near a door, press 'e' to open it.", app.width/2, app.height/3+50, font='monospace', fill='white', size=25, bold=True)
    drawLabel("When near stairs, press 'w' or 's' to use them accordingly.", app.width/2, app.height/3+100, font='monospace', fill='white', size=25, bold=True)
    drawLabel("Left Click the mouse buttons to shoot.", app.width/2, app.height/3+150, font='monospace', fill='white', size=25, bold=True)
    drawLabel("Good Luck!", app.width/2, app.height/3+200, font='monospace', fill='white', size=25, bold=True)

    if app.menuIntersect:
        drawButton('Menu', app.width/2, 3*app.height/4, app.buttonW, app.buttonH, 'orange')
    else:
        drawButton('Menu', app.width/2, 3*app.height/4, app.buttonW, app.buttonH, 'darkblue')
    
def instructions_onMouseMove(app, mouseX, mouseY):
    app.c1x, app.c2x = mouseX, mouseX
    app.c1y, app.c2y = mouseY, mouseY
    if ((app.width/2 - app.buttonW/2 < mouseX < app.width/2 + app.buttonW/2) and 
        (3*app.height/4 - app.buttonH/2 < mouseY < 3*app.height/4 + app.buttonH/2)):
            app.menuIntersect = True
    else: app.menuIntersect = False


def instructions_onMousePress(app, mouseX, mouseY):
    if app.retryIntersect:
        loadLvl1(app)
        setActiveScreen(app.prevLvl)
    if app.menuIntersect:
        setActiveScreen('menu')
# ------------------------------------------------------------------------------

# -----------------------win screen---------------------------------------------
def win_redrawAll(app):
    drawImage(app.backgroundImage, 0, 0)
    drawRect(0,0,app.width,app.height, fill='black', opacity=85)
    drawLabel("You Won!", app.width/2, app.height/3, font='monospace', fill='white', size=25, bold=True)
    drawLabel(f"Your elapsed time was around {pythonRound(app.end-app.begin)} seconds!", app.width/2, app.height/3+50, font='monospace', fill='white', size=25, bold=True)
    
    if app.retryIntersect:
        drawButton('Retry', app.width/2, app.height/2, app.buttonW, app.buttonH, 'orange')
    else:
        drawButton('Retry', app.width/2, app.height/2, app.buttonW, app.buttonH, 'darkBlue')
    if app.menuIntersect:
        drawButton('Menu', app.width/2, 3*app.height/4, app.buttonW, app.buttonH, 'orange')
    else:
        drawButton('Menu', app.width/2, 3*app.height/4, app.buttonW, app.buttonH, 'darkblue')
    
def win_onMouseMove(app, mouseX, mouseY):
    if ((app.width/2 - app.buttonW/2 < mouseX < app.width/2 + app.buttonW/2) and 
        (app.height/2 - app.buttonH/2 < mouseY < app.height/2 + app.buttonH/2)):
            app.retryIntersect = True
    else: app.retryIntersect = False
    if ((app.width/2 - app.buttonW/2 < mouseX < app.width/2 + app.buttonW/2) and 
        (3*app.height/4 - app.buttonH/2 < mouseY < 3*app.height/4 + app.buttonH/2)):
            app.menuIntersect = True
    else: app.menuIntersect = False


def win_onMousePress(app, mouseX, mouseY):
    if app.retryIntersect:
        loadLvl1(app)
        setActiveScreen(app.prevLvl)
    if app.menuIntersect:
        setActiveScreen('menu')

# --------------------------pause menu------------------------------------------

def pause_redrawAll(app):
    if app.prevLvl == 'lvl1':
        # draw backgrounds
        drawImage(app.backgroundImage, 0, 0)
        drawImage(app.lvl1_background, 400-app.scrollX, app.lvl1ground1-450)
        drawImage(app.painting1, 800-app.scrollX, app.lvl1ground1-160)
        drawImage(app.decor, 1200-app.scrollX, app.lvl1ground1-160)
        drawImage(app.decor, 500-app.scrollX, app.lvl1ground2-160)
        drawImage(app.decor, 1000-app.scrollX, app.lvl1ground2-160)
        drawImage(app.painting1, 1200-app.scrollX, app.lvl1ground2-160)

        # drawing the "base ground"
        drawLine(0, app.lvl1ground1, app.width, app.lvl1ground1, lineWidth = 5)

        # ---------------******LEVEL SPECIFIC******-----------------------------
        # draw vertical walls
        for vWall in app.lvl1vWallList:
            vWall.drawWall(app)

        # draw stairs
        for stair in app.lvl1stairList:
            stair.drawStair(app)

        # draw doors
        for door in app.lvl1doorList:
            door.drawDoor(app)

        # draw floor 1, floor 2, and roof
        drawLine(400-app.scrollX, app.lvl1ground1, 1440-app.scrollX, app.lvl1ground1, lineWidth = 5)
        drawLine(400-app.scrollX, app.lvl1ground2, 1440-app.scrollX, app.lvl1ground2, lineWidth = 5)
        drawLine(400-app.scrollX-2.5, app.lvl1ground1-450, 1440-app.scrollX+2.5, app.lvl1ground1-450, lineWidth = 5)
        
        # underground
        drawRect(0, app.lvl1ground1, app.width, app.height-app.lvl1ground1, fill='black')

        # draw player/enemies
        app.player.draw(app)
        
        for enemy in app.lvl1enemyList:
            enemy.draw(app)
        
        # draw bullets
        for bullet in app.bulletList:
            bullet.draw()
    
    drawRect(0,0,app.width,app.height, fill='black', opacity=60)
    drawLabel('Game Paused! Press p to resume.', app.width/2, app.height/4,
              font='monospace', size=24, fill='white')
    
def pause_onKeyPress(app, key):
    if key == 'p':
        setActiveScreen('lvl1')


# ------------------------------------------------------------------------------

# ---------------game over screen-----------------------------------------------

def gameOver_redrawAll(app):

    
    drawImage(app.gameOver_background, 0, 0)
    if app.retryIntersect:
        drawButton('Retry', app.width/2, app.height/2, app.buttonW, app.buttonH, 'orange')
    else:
        drawButton('Retry', app.width/2, app.height/2, app.buttonW, app.buttonH, 'blue')
    
    if app.menuIntersect:
        drawButton('Menu', app.width/2, 3*app.height/4, app.buttonW, app.buttonH, 'orange')
    else:
        drawButton('Menu', app.width/2, 3*app.height/4, app.buttonW, app.buttonH, 'blue')

def gameOver_onMouseMove(app, mouseX, mouseY):
    app.c1x, app.c2x = mouseX, mouseX
    app.c1y, app.c2y = mouseY, mouseY
    if ((app.width/2 - app.buttonW/2 < mouseX < app.width/2 + app.buttonW/2) and 
        (app.height/2 - app.buttonH/2 < mouseY < app.height/2 + app.buttonH/2)):
            app.retryIntersect = True
    else: app.retryIntersect = False
    if ((app.width/2 - app.buttonW/2 < mouseX < app.width/2 + app.buttonW/2) and 
        (3*app.height/4 - app.buttonH/2 < mouseY < 3*app.height/4 + app.buttonH/2)):
            app.menuIntersect = True
    else: app.menuIntersect = False

def gameOver_onMousePress(app, mouseX, mouseY):
    if app.retryIntersect:
        loadLvl1(app)
        setActiveScreen(app.prevLvl)
    if app.menuIntersect:
        setActiveScreen('menu')



# ------------------------------------------------------------------------------

def main():
    runAppWithScreens(initialScreen='menu')

    
main()