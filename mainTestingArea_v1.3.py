# for citations, see latest "mainTestingArea"

from cmu_graphics import *
from PIL import Image

def onAppStart(app):
    app.width = 288*4
    app.height = 192*4
    app.player = Player('player', app.width/2, app.height/2 - 50)
    app.c1x = app.width/2       #inner circle X
    app.c1y = app.height/2      #inner circle Y
    app.c2x = app.width/2       #outer circle X
    app.c2y = app.height/2      #outer circle Y
    app.c2r = 10                #outer circle radius
    app.lastMouseX = app.c1x
    app.lastMouseY = app.c1y
    app.spriteCounter = 0
    app.stepCount = 0
    

    #side scrolling stuff and player width
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

    app.player.currentMovement('idle', app)


class Player():

    def __init__(self, type, x, y):

        # set the player location
        self.x = x
        self.y = y

        # player bounds
        self.width = 50
        self.height = 50


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
        if key == 'right':
            self.movingRight = True
            self.movingLeft = False
            self.idling = False
            img = Image.open(self.imageRunningRight)
            self.animationList = []
            for i in range(6):
                sprite = CMUImage(img.crop((50*i, 0, 50*(i+1), 50)))
                self.animationList.append(sprite)
        
        # you would add the "running left" animation here
        elif key == 'left':
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
        # self.makePlayerVisible(app)
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
    
    drawCircle(app.c1x, app.c1y, 3, fill='black', border=None)          #draws cursor inner circle
    drawCircle(app.c2x, app.c2y, app.c2r, fill=None, border='black')    #draws cursor outer circle
    # drawRect(0, lineY, app.width, lineY+lineHeight,fill="black")

    #drawing the "ground" level
    drawLine(0, app.height/2, app.width, app.height/2)

    sx = app.scrollX
    for wall in range(app.walls):
        
        (x0, y0, x1, y1) = getWallBounds(app, wall)
        if (wall == app.currentWallHit):
            fill = "orange"
        else: fill = "pink"
        drawRect(x0-sx, y0, x1-x0, y1-y0, fill=fill)
        (cx, cy) = ((x0+x1)/2 - sx, (y0 + y1)/2)
        drawLabel(str(app.wallPoints[wall]), cx, cy)

    app.player.draw(app)

def onMouseMove(app, mouseX, mouseY):
    #'remembers' last mouse location when moving
    app.lastMouseX = mouseX
    app.lastMouseY = mouseY

def onMouseDrag(app, mouseX, mouseY):
    #'remembers' last mouse location when dragging
    app.lastMouseX = mouseX
    app.lastMouseY = mouseY


def onStep(app):
    # update player postion, distance from player to cursor, and update cursor size on every step
    playerPosition = app.player.getPosition()
    distFromPlayer = distance(app.c2x+app.scrollX,app.c2y, playerPosition[0], playerPosition[1])
    cursorUpdate(app, app.lastMouseX, app.lastMouseY, distFromPlayer)

    # updating spriteCounter as required (controls the fps)
    app.stepCount += 1
    if (app.stepCount%3 == 0) or (app.player.idling):
        app.spriteCounter = (1+app.spriteCounter) % len(app.player.animationList)





def onKeyHold(app, keys):

    #these update the player location
    if ('right' in keys) and ('left' in keys):
        app.player.currentMovement('idle', app)
    elif 'right' in keys:
        app.player.x += 5
        app.player.currentMovement('right', app)
    elif 'left' in keys:
        app.player.x -= 5
        app.player.currentMovement('left', app)
    
    
    #add 'stair' logic below
    if 'up' in keys:
        app.player.y -= 5
        app.player.currentMovement('idle', app)
    elif 'down' in keys:
        app.player.y += 5
        app.player.currentMovement('idle', app)   

def onKeyRelease(app, key):
    if (key == 'right') or (key == 'left'):
        app.player.currentMovement('idle', app)

def main():
    runApp()
    
main()