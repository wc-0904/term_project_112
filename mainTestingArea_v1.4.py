from cmu_graphics import *
from PIL import Image
import math

# I've taken inspiration from a number of games and tutorials online
# I've also used sprites found online
# Please check the text file included in the folder for all the citations
# This game was insprired by the orignial game "Deadbolt"
# https://www.youtube.com/watch?v=SbcZ0GtPsvI&t=1733s
# I took many small ideas from this tutorial playlist:
# https://youtube.com/playlist?list=PLjcN1EyupaQm20hlUE11y9y8EY2aXLpnv&si=d5wfh5x85H8WbyaK

def onAppStart(app):
    app.width = 288*4
    app.height = 192*4

    # player and enemy instances on level creation
    app.player = Player('player', app.width/2, app.height/2 - 50)

    # cursor stuff
    app.c1x = app.width/2       #cursor inner circle X
    app.c1y = app.height/2      #cursor inner circle Y
    app.c2x = app.width/2       #cursor outer circle X
    app.c2y = app.height/2      #cursor outer circle Y
    app.c2r = 10                #cursor outer circle radius
    app.lastMouseX = app.c1x
    app.lastMouseY = app.c1y

    # sprite animation stuff
    app.spriteCounter = 0
    app.stepCount = 0

    # took inspiration from previous 15-112 tutorials for sidescrolling
    # throughout the app
    # https://www.cs.cmu.edu/~112-f22/notes/notes-animations-part4.html#sidescrollerExamples
    
    # side scrolling stuff and player width
    app.scrollX = 0
    app.scrollMargin = 50
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
    app.player.currentMovement('idle', app)


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
            self.dx = math.cos(self.angle)*5
            self.dy = -(math.sin(self.angle)*5)
            self.ddy = 0

            # for this, we know our stepsPerSec is 30, but other wise we'd multiply by app.stepsPerSecond
            self.timer = 5*30

        if char == 'enemy1':
            pass
        if char == 'enemy2':
            pass
        if char == 'enemy3':
            pass
        

    # draws the bullet
    def draw(self):
        drawCircle(self.x, self.y, 5, fill='blue')
    

    # step function
    def step(self, app):

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
        if (self.timer == 0):
            app.bulletList.remove(self)
    
        
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

        # 
        # used a sprite from this website:
        # https://www.codeandweb.com/texturepacker/tutorials/how-to-create-a-sprite-sheet
        # sprite animation stuff
        # name both idle and running animation
        self.imageIdle = f'images/{type}_idle.png' #dont have this animation yet
        self.imageRunningRight = f'images/{type}_running_right.png'
        self.imageRunningLeft = f'images/{type}_running_left.png'

        # set direction values
        self.movingRight = False
        self.movingLeft = False
        self.idling = True

        # this is the list that'll contatin the current animation
        self.animationList = []
    
    # draw function to draw the player (temporarily using drawCircle for idling)
    def draw(self, app):
        if self.idling:
            drawCircle(self.x-app.scrollX, self.y, 7, fill='blue')
        else:
            if self.animationList != []:
                currSprite = self.animationList[app.spriteCounter]
                drawImage(currSprite, self.x-app.scrollX, self.y)
        
    
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
        elif key == 'idle':
            self.movingRight = False
            self.movingLeft = False
            self.idling = True
            img = Image.open(self.imageRunningRight)   # don't have idle animation yet, this where I'd put an idle animation
            self.animationList = []
            for i in range(6):
                sprite = CMUImage(img.crop((50*i, 0, 50*(i+1), 50)))
                self.animationList.append(sprite)
        makePlayerVisible(app)
        checkForNewWallHit(app)            

    def getPosition(self):
        return [self.x, self.y]
    
    # def getWallBounds(self, app, wall):
    #     # returns absolute bounds, not taking scrollX into account
    #     (x0, y1) = ((1+wall) * app.wallSpacing, app.height/2)
    #     (x1, y0) = (x0 + app.wallWidth, y1 - app.wallHeight)
    #     return (x0, y0, x1, y1)

    def getPlayerBounds(self, app):
        #absolute bounds, without taking scrollX into account
        (x0, y0) = (self.x, self.y)
        (x1, y1) = (x0 + self.width, y0 + self.height)
        return (x0, y0, x1, y1)
    

    # Took inspiration from older 15-112 websites for collision logic below:
    # https://www.cs.cmu.edu/~112-f22/notes/notes-animations-part4.html#sidescrollerExamples


    # #function below should be adjust for doors
    # def getWallHit(self, app):
    #     playerBounds = self.getPlayerBounds(app)
    #     for wall in range(app.walls):
    #         wallBounds = getWallBounds(app, wall)
    #         if (boundsIntersect(playerBounds, wallBounds) == True):
    #             return wall
    #     return -1

    # def boundsIntersect(self, boundsA, boundsB):
    #     # return l2<=r1 and t2<=b1 and l1<=r2 and t1<=b2
    #     (ax0, ay0, ax1, ay1) = boundsA
    #     (bx0, by0, bx1, by1) = boundsB
    #     return ((ax1 >= bx0) and (bx1 >= ax0) and
    #             (ay1 >= by0) and (by1 >= ay0))
    
    # def checkForNewWallHit(self, app):
    #     # check if we are hitting a new wall for the first time
    #     wall = self.getWallHit(app)
    #     if (wall != app.currentWallHit):
    #         app.currentWallHit = wall
    #         if (wall >= 0):
    #             app.wallPoints[wall] += 1
    
    # def makePlayerVisible(self, app):
    #     # scroll to make player visible as needed
    #     if (self.x < app.scrollX + app.scrollMargin):
    #         app.scrollX = self.x - app.scrollMargin
    #     if (self.x > app.scrollX + app.width - app.scrollMargin):
    #         app.scrollX = self.x - app.width + app.scrollMargin


    # bullet drawing function, this only appends to the bullet list
    def drawBullet(self, app, mouseX, mouseY):
        xDistance = (mouseX - (self.x-app.scrollX))
        yDistance = -(mouseY - self.y)
        bulletAngle = math.atan2(yDistance, xDistance)
        app.bulletList.append(Bullet(self.x-app.scrollX, self.y, self.type, bulletAngle))


def checkForNewWallHit(app):
    # check if we are hitting a new wall for the first time
    wall = getWallHit(app)
    if (wall != app.currentWallHit):
        app.currentWallHit = wall
        if (wall >= 0):
            app.wallPoints[wall] += 1

def makePlayerVisible(app):
        # scroll to make player visible as needed
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
    if distFromRef > 60:                #this determines how far the cursor goes without changing shape
        app.c2r = distFromRef/6         #this has to be updated along with distFromRef, divide by the 'threshold/10'
    else:
        app.c2r = 10

#function below should be adjust for doors
def getWallHit(app):
    playerBounds = app.player.getPlayerBounds(app)
    for wall in range(app.walls):
        wallBounds = getWallBounds(app, wall)
        if (boundsIntersect(playerBounds, wallBounds) == True):
            return wall
    return -1
    
#helper
def distance(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y0-y1)**2)**0.5

def getWallBounds(app, wall):
    # returns absolute bounds, not taking scrollX into account
    (x0, y1) = ((1+wall) * app.wallSpacing, app.height/2)
    (x1, y0) = (x0 + app.wallWidth, y1 - app.wallHeight)
    return (x0, y0, x1, y1)

def redrawAll(app):
    #draws cursor inner & outer circle
    drawCircle(app.c1x, app.c1y, 3, fill='black', border=None)          
    drawCircle(app.c2x, app.c2y, app.c2r, fill=None, border='black')    
    
    #drawing the "ground" level
    drawLine(0, app.height/2, app.width, app.height/2)

    # wall collision and update logic ***replace with doors
    sx = app.scrollX
    for wall in range(app.walls):        
        (x0, y0, x1, y1) = getWallBounds(app, wall)
        if (wall == app.currentWallHit):
            fill = "orange"
        else: fill = "pink"
        drawRect(x0-sx, y0, x1-x0, y1-y0, fill=fill)
        (cx, cy) = ((x0+x1)/2 - sx, (y0 + y1)/2)
        drawLabel(str(app.wallPoints[wall]), cx, cy)

    # draw bullets
    for bullet in app.bulletList:
        bullet.draw()

    # draw player/enemies
    app.player.draw(app)

def onMouseMove(app, mouseX, mouseY):
    #'remembers' last mouse location when moving
    app.lastMouseX = mouseX
    app.lastMouseY = mouseY

def onMouseDrag(app, mouseX, mouseY):
    #'remembers' last mouse location when dragging
    app.lastMouseX = mouseX
    app.lastMouseY = mouseY

def onMousePress(app, mouseX, mouseY):
    app.player.drawBullet(app, mouseX, mouseY)

def onStep(app):
    # update player postion, distance from player to cursor, and update cursor size on every step
    playerPosition = app.player.getPosition()
    distFromPlayer = distance(app.c2x+app.scrollX,app.c2y, playerPosition[0], playerPosition[1])
    cursorUpdate(app, app.lastMouseX, app.lastMouseY, distFromPlayer)

    # updating spriteCounter as required (controls the sprite fps)
    app.stepCount += 1
    if (app.stepCount%3 == 0) or (app.player.idling):
        app.spriteCounter = (1+app.spriteCounter) % len(app.player.animationList)
    
    # update the bullet
    for bullet in app.bulletList:
        bullet.step(app) 
    
    




def onKeyHold(app, keys):

    #these update the player location
    if ('d' in keys) and ('a' in keys):
        app.player.currentMovement('idle', app)
    elif 'd' in keys:
        app.player.x += 5
        app.player.currentMovement('d', app)
    elif 'a' in keys:
        app.player.x -= 5
        app.player.currentMovement('a', app)
    
    
    # add 'stair' logic below
    if 'w' in keys:
        # app.player.y -= 5
        # app.player.currentMovement('idle', app)
        pass
    elif 's' in keys:
        # app.player.y += 5
        # app.player.currentMovement('idle', app)   
        pass

def onKeyRelease(app, key):
    if (key == 'd') or (key == 'a'):
        app.player.currentMovement('idle', app)
    
    if key == 'p': print(app.scrollX)
    if key == 'x': print(app.player.x)
    if key == 'y': print(app.player.y)

def main():
    runApp()
    
main()