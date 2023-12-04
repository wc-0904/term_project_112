from cmu_graphics import *
from PIL import Image
import math

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

    app.backgroundImage = Image.open('images/background.png')
    app.menuBackground = Image.open('images/menu_background.png')

    # welcome screen stuff
    app.buttonW = 600
    app.buttonH = 100
    app.lvl1Fill = 'darkBlue'
    app.lvl2Fill = 'darkGreen'
    app.lvl1Intersect = False
    app.lvl2Intersect = False

#--------------------lvl1 stuff-------------------------------------------------
    # lvl1 background
    app.lvl1_background = Image.open('images/lvl1_background.png')

    # set ground and player Y levels
    app.lvl1groundList = []
    app.lvl1ground1 = 3*app.height/4
    app.lvl1ground2 = app.lvl1ground1-225
    app.lvl1groundList.append(app.lvl1ground1)
    app.lvl1groundList.append(app.lvl1ground2)
    app.pGround = app.lvl1groundList[0]
    
    # player and enemy instances on level creation
    app.player = Player('player', 100, app.pGround - 25 - 2.5)
    # app.enemy1 = Player('enemy1', 100, app.lvl1ground1 - 25)

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
    app.playerX = app.player.getPosition()[0]
    app.playerY = app.player.getPosition()[1]

    #walls/doors
    app.walls = 5
    app.wallPoints = [0]*app.walls
    app.wallWidth = 20
    app.wallHeight = 40
    app.wallSpacing = 90
    app.currentWallHit = -1

    # bullet list, stores all the current bullets in-game
    app.bulletList = []

    # calls to idle animations
    app.player.currentMovement('idle_right', app)
    # app.enemy1.currentMovement('idle_right', app)

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

        # set bullet pattern based on player/enemy here
        if char == 'player':
            # player bullet goes straight, no gravity
            # sets dx and dy based on angle
            self.pattern = 'straight'
            self.dx = math.cos(self.angle)*15
            self.dy = -(math.sin(self.angle)*15)
            self.ddy = 0

            # for this, we know our stepsPerSec is 30, but other wise we'd multiply by app.stepsPerSecond
            self.timer = 5*30

        if char == 'enemy1':
            self.pattern = 'parabolic'
            self.dx = math.cos(self.angle)*15
            self.dy = -(math.sin(self.angle)*15)
            self.ddy = 0.2
        
        if char == 'enemy2':
            pass
        if char == 'enemy3':
            pass
        

    # draws the bullet
    def draw(self):
        drawCircle(self.x, self.y, 5, fill='blue')
    

    # step function
    def step(self, app):
        if self.pattern == 'straight':
            bulletGround = app.pGround
            bulletRoof = app.pGround - 225
        # bullet physics stuff
        self.x += self.dx
        self.y += self.dy
        self.dx += self.ddx
        self.dy += self.ddy

        # decrement timer every step
        self.timer -= 1

        # different pattern to be added below
        # ...

        # self deletion logic, ****add enemy collision logic here
        if (self.timer == 0) or (self.y > bulletGround or self.y < bulletRoof):
            # angle bounce logic here
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

        # 
        # used a sprite from this website:
        # https://www.codeandweb.com/texturepacker/tutorials/how-to-create-a-sprite-sheet
        # sprite animation stuff
        # name both idle and running animation
        
        # **CITATION**
        # original sprites created using www.piskelapp.com
        # ****CURRENTLY TESTING****
        self.imageIdle = f'images/{type}_idle.png' #dont have this animation yet
        self.imageRunningRight = f'images/{type}_running_right.png'
        self.imageRunningLeft = f'images/{type}_running_left.png'

        # set direction values
        self.movingRight = False
        self.movingLeft = False
        self.idling = True

        # this is the list that'll contatin the current animation
        self.animationList = []
    
    # draw function to draw the player
    def draw(self, app):
        if self.animationList != []:
            currSprite = self.animationList[app.spriteCounter]
            drawImage(currSprite, self.x-app.scrollX-25, self.y-25)
        
    
    # this checks what movement the player is doing (running or idling)
    def currentMovement(self, key, app):

        # you would add the "running right" animation here
        if key == 'd':
            self.movingRight = True
            self.movingLeft = False
            self.idling = False
            img = Image.open(self.imageRunningRight)
            self.animationList = []
            for i in range(6):
                sprite = CMUImage(img.crop((50*i, 0, 50*(i+1), 50)))
                self.animationList.append(sprite)
        
        # you would add the "running left" animation here
        elif key == 'a':
            self.movingRight = False
            self.movingLeft = True
            self.idling = False
            img = Image.open(self.imageRunningLeft)
            self.animationList = []
            for i in range(6):
                sprite = CMUImage(img.crop((50*i, 0, 50*(i+1), 50)))
                self.animationList.append(sprite)
        
        # you would add the "idling" animation here
        elif key == 'idle_right':
            self.movingRight = False
            self.movingLeft = False
            self.idling = True
            img = Image.open(self.imageIdle)   # don't have idle animation yet, this where I'd put an idle animation
            self.animationList = []
            for i in range(6):
                sprite = CMUImage(img.crop((50*i, 0, 50*(i+1), 50)))
                self.animationList.append(sprite)
        
        elif key == 'idle_left':
            self.movingRight = False
            self.movingLeft = False
            self.idling = True
            right_img = Image.open(self.imageIdle)   # don't have idle animation yet, this where I'd put an idle animation
            img = right_img.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
            self.animationList = []
            for i in range(6):
                sprite = CMUImage(img.crop((50*i, 0, 50*(i+1), 50)))
                self.animationList.append(sprite)

        makePlayerVisible(app, app.player)
        # checkForNewWallHit(app)            

    def getPosition(self):
        return [self.x, self.y]

    def setPlayerBounds(self, app):
        self.bounds = (self.x-25-5-app.scrollX, self.y-25,
                       self.x+25+5-app.scrollX, self.y+25)
    
    def drawBounds(self, app):
        drawLine(*self.bounds)

    # def getPlayerBounds(self):
    #     #absolute bounds, without taking scrollX into account
    #     (x0, y0) = (self.x, self.y)
    #     (x1, y1) = (x0 + self.width, y0 + self.height)
    #     return (x0, y0, x1, y1)
    

    # Took inspiration from older 15-112 websites for collision logic below:
    # https://www.cs.cmu.edu/~112-f22/notes/notes-animations-part4.html#sidescrollerExamples

    # bullet drawing function, this only appends to the bullet list
    def drawBullet(self, app, mouseX, mouseY):
        xDistance = (mouseX - (self.x-app.scrollX))
        yDistance = -(mouseY - self.y)
        bulletAngle = math.atan2(yDistance, xDistance)
        app.bulletList.append(Bullet(self.x-app.scrollX, self.y, self.type, bulletAngle))

class vWall():
    
    def __init__(self, name, botX, botY, topX, topY):
        self.name = name
        self.botX = botX
        self.botY = botY
        self.topX = topX
        self.topY = topY

    def drawWall(self, app):
        drawLine(self.botX-app.scrollX, self.botY, 
                 self.topX-app.scrollX, self.topY, 
                 lineWidth = 5)

    def __repr__(self):
        return self.name
    
class Stair():

    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

        self.bounds = (self.x-5, self.y-22.5, self.x+5, self.y+22.5)
    
    def drawStair(self, app):
        if self.type == 'up':
            drawRect(self.x-17.5-app.scrollX, self.y-27.5, 35, 55, 
                     fill='black',border='black', borderWidth=1, opacity=85)
            drawLine(self.x+17.5-app.scrollX, self.y-27.5, self.x-17.5-app.scrollX, self.y+27.5)
            drawPolygon(self.x+17.5-app.scrollX, self.y-27.5, self.x-17.5-app.scrollX, self.y+27.5, self.x+17.5-app.scrollX, self.y+27.5, fill='black')
            # drawLine()
        if self.type == 'down':
            drawRect(self.x-17.5-app.scrollX, self.y-27.5, 35, 55, 
                     fill='black',border='black', borderWidth=1)
    
    def setStairBounds(self, app):
        self.bounds = (self.x-5-app.scrollX, self.y-22.5,
                       self.x+5-app.scrollX, self.y+22.5)

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
    
    def setDoorBounds(self, app):
        self.bounds = (self.x-app.scrollX, self.y-52.5,
                       self.x+50-app.scrollX, self.y)


#-------------------------------------------------------------------------------

#------------------------Global Functions---------------------------------------

# #function below should be adjust for doors
# def checkForNewWallHit(app):
#     # check if we are hitting a new wall for the first time
#     wall = getWallHit(app)
#     if (wall != app.currentWallHit):
#         app.currentWallHit = wall
#         if (wall >= 0):
#             app.wallPoints[wall] += 1

def makePlayerVisible(app, player):
        # scroll to make player visible as needed
        if player.type == 'player': 
            if (app.player.x < app.scrollX + app.scrollMargin):
                app.scrollX = app.player.x - app.scrollMargin
            if (app.player.x > app.scrollX + app.width - app.scrollMargin):
                app.scrollX = app.player.x - app.width + app.scrollMargin

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
    if distFromRef > 150:                #this determines how far the cursor goes without changing shape
        app.c2r = distFromRef/15         #this has to be updated along with distFromRef, divide by the 'threshold/10'
    else:
        app.c2r = 10

# collision logic for walls
def checkWallHit(app):
    for vWall in app.lvl1vWallList:
        if ((app.player.x+25 >= vWall.botX) 
             and (app.player.x-25 <= vWall.botX) 
             and (app.player.y-25 >= vWall.topY)
             and (app.player.y+25 <= vWall.botY)):
            print(f'{vWall.botX}')
            print(vWall)
            print(f'right: {app.player.x+25}, left: {app.player.x-25}')
            return True

# collision logic for doors
def checkDoorHit(app):
    for door in app.lvl1doorList:
        if not door.open:
            if ((app.player.x+25 >= door.x) 
             and (app.player.x-25 <= door.x)
             and (app.player.y-25 >= door.y-52.5)
             and (app.player.y+25 <= door.y)):
                return True
    return False

    # playerBounds = app.player.bounds
    # for wall in range(app.walls):
    #     wallBounds = getWallBounds(app, wall)
    #     if (boundsIntersect(playerBounds, wallBounds) == True):
    #         return wall
    # return -1
    
#helper
def distance(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y0-y1)**2)**0.5

# #function below should be adjust for doors
def getWallBounds(app, wall):
    # returns absolute bounds, not taking scrollX into account
    (x0, y1) = ((1+wall) * app.wallSpacing, app.height/2)
    (x1, y0) = (x0 + app.wallWidth, y1 - app.wallHeight)
    return (x0, y0, x1, y1)

def drawButton(label, x, y, width, height, color):
    drawRect(x-width/2, y-height/2, width, height, border='black', borderWidth=5, fill=color)
    drawLabel(label, x, y, font='monospace', size=90)
# ------------------------------------------------------------------------------


# **CITATION**
# Based on screens logic from Mike's 15-112 lecture demo
# -----------------------lvl1 Screen--------------------------------------------
def lvl1_redrawAll(app):
    # TESTING*****
    app.player.drawBounds(app)
    # wall collision and update logic ***replace with doors
    # sx = app.scrollX
    # for wall in range(app.walls):        
    #     (x0, y0, x1, y1) = getWallBounds(app, wall)
    #     if (wall == app.currentWallHit):
    #         fill = "orange"
    #     else: fill = "pink"
    #     drawRect(x0-sx, y0, x1-x0, y1-y0, fill=fill)
    #     (cx, cy) = ((x0+x1)/2 - sx, (y0 + y1)/2)
    #     drawLabel(str(app.wallPoints[wall]), cx, cy)

    # draw backgrounds
    drawImage(CMUImage(app.backgroundImage), 0, 0)
    drawImage(CMUImage(app.lvl1_background), 400-app.scrollX, app.lvl1ground1-450)

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
    # app.enemy1.draw(app)   
    
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

    if app.player.getPosition()[0] >= mouseX+app.scrollX:
        app.player.currentMovement('idle_left', app)
    else:
        app.player.currentMovement('idle_right', app)
    app.player.drawBullet(app, mouseX, mouseY)

    # print(app.enemy1.getPosition())

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
    
    # updates stair bounds
    for stair in app.lvl1stairList:
        stair.setStairBounds(app)
    
    # updates door bounds
    for door in app.lvl1doorList:
        door.setDoorBounds(app)
    
    
    # updates player bounds
    app.player.setPlayerBounds(app)

    
def lvl1_onKeyHold(app, keys):

    #these update the player location
    if ('d' in keys) and ('a' in keys):
        app.player.currentMovement('idle_right', app)
    elif 'd' in keys:
        app.player.x += 10
        if (not checkWallHit(app)) and (not checkDoorHit(app)):
            app.player.currentMovement('d', app)
        else:
            app.player.x -=10
    elif 'a' in keys:
        app.player.x -= 10
        if (not checkWallHit(app)) and (not checkDoorHit(app)):
            app.player.currentMovement('a', app)
        else:
            app.player.x += 10
    
    
    # add 'stair' logic below
    if 'w' in keys:
        # app.player.y -= 5
        # app.player.currentMovement('idle', app)
        pass
    elif 's' in keys:
        # app.player.y += 5
        # app.player.currentMovement('idle', app)   
        pass

def lvl1_onKeyRelease(app, key):
    if (key == 'd'):
        app.player.currentMovement('idle_right', app)
    elif (key == 'a'):
        app.player.currentMovement('idle_left', app)
    
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
    
    if (key == 'e'):
        for door in app.lvl1doorList:
            if boundsIntersect(app.player.bounds, door.bounds):
                door.open = not door.open

    
    if key == 'p': print(app.scrollX)
    if key == 'x': print(app.player.x)
    if key == 'y': print(app.player.y)
# ------------------------------------------------------------------------------


# **CITATION**
# Based on screens logic from Mike's 15-112 lecture demo
# ---------------------Main Menu------------------------------------------------

def menu_redrawAll(app):
    # drawLabel("Ghost of Downtown", app.width/2, app.height/8, size=45)
    drawImage(CMUImage(app.menuBackground), 0, 0)
    drawButton('Level 1', 3*app.width/4, app.height/3, app.buttonW, app.buttonH, app.lvl1Fill)
    drawButton('Level 2', 3*app.width/4, 2*app.height/3, app.buttonW, app.buttonH, app.lvl2Fill)

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
            app.lvl2Fill = 'orange'
            app.lvl2Intersect = True
        else: app.lvl2Fill, app.lvl2Intersect = 'darkGreen', False
    else: 
        app.lvl1Fill, app.lvl2Fill = 'darkBlue', 'darkGreen'
        app.lvl1Intersect, app.lvl2Intersect = False, False

def menu_onMousePress(app, mouseX, mouseY):
    if app.lvl1Intersect:
        setActiveScreen('lvl1')
    if app.lvl2Intersect:
        # setActiveScreen('Level 2')
        pass

    

# ------------------------------------------------------------------------------

def main():
    runAppWithScreens(initialScreen='menu')

    
main()