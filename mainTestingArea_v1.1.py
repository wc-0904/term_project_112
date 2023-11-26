from cmu_graphics import *
from PIL import Image

def onAppStart(app):
    app.width = 288*4
    app.height = 192*4
    app.player = Player('player', app.width/2, app.height/2)
    app.c1x = app.width/2       #inner circle X
    app.c1y = app.height/2      #inner circle Y
    app.c2x = app.width/2       #outer circle X
    app.c2y = app.height/2      #outer circle Y
    app.c2r = 10                #outer circle radius
    app.lastMouseX = app.c1x
    app.lastMouseY = app.c1y
    app.spriteCounter = 0
    app.stepCount = 0
    app.player.currentMovement('idle')



class Player():

    def __init__(self, type, x, y):

        # set the player location
        self.x = x
        self.y = y

        # sprite animation stuff
        # name both idle and running animation
        self.imageIdle = f'images/{type}_idle.png'
        self.imageRunning = f'images/{type}_running.png'

        self.movingRight = False
        self.movingLeft = False
        self.idling = True

        # this is the list that'll contatin the current animation
        self.animationList = []
    
    # draw function to draw the player (using drawCircle for now)
    def draw(self, app):
        if self.idling:
            drawCircle(self.x, self.y, 7, fill='blue')
        else:
            currSprite = self.animationList[app.spriteCounter]
            drawImage(currSprite, self.x, self.y)
        
    
    # this checks what movement the player is doing (running or idling)
    def currentMovement(self, key):

        # you would add the "running right" animation here
        if key == 'right':
            self.movingRight = True
            self.movingLeft = False
            self.idling = False
            img = Image.open(self.imageRunning)
            for i in range(6):
                sprite = CMUImage(img.crop((50*i, 0, 50*(i+1), 50)))
                self.animationList.append(sprite)
        
        # you would add the "running left" animation here
        elif key == 'left':
            self.movingRight = False
            self.movingLeft = True
            self.idling = False
            img = Image.open(self.imageRunning)
            for i in range(6):
                sprite = CMUImage(img.crop((50*i, 0, 50*(i+1), 50)))
                self.animationList.append(sprite)
        
        # you would add the "idling" animation here
        elif key == 'idle':
            self.movingRight = False
            self.movingLeft = False
            self.idling = True
            img = Image.open(self.imageRunning)      # don't have idle animation yet, this where I'd put an idle animation
            for i in range(6):
                sprite = CMUImage(img.crop((50*i, 0, 50*(i+1), 50)))
                self.animationList.append(sprite)
                   
    

    def getPosition(self):
        return [self.x, self.y]


#function assigns cursor center to mouse location
def cursorUpdate(app, mouseX, mouseY, distFromRef):
    app.c1x = app.c2x = mouseX
    app.c1y = app.c2y = mouseY
    if distFromRef > 60:                #this determines how far the cursor goes without changing shape
        app.c2r = distFromRef/6         #this has to be updated along with distFromRef, divide by the 'threshold/10'
    else:
        app.c2r = 10

#helper
def distance(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y0-y1)**2)**0.5


def redrawAll(app):
    app.player.draw(app)
    drawCircle(app.c1x, app.c1y, 3, fill='black', border=None)      #draws inner circle
    drawCircle(app.c2x, app.c2y, app.c2r, fill=None, border='black') #draws outer circle


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
    distFromPlayer = distance(app.c2x,app.c2y, playerPosition[0], playerPosition[1])
    cursorUpdate(app, app.lastMouseX, app.lastMouseY, distFromPlayer)

    # updating spriteCounter as required (controls the fps)
    app.stepCount += 1
    if app.stepCount%3 == 0 or app.player.idling:
        app.spriteCounter = (1+app.spriteCounter) % len(app.player.animationList)





def onKeyHold(app, keys):

    #these update the player location
    if 'right' in keys:
        app.player.x += 5
        app.player.currentMovement('right')
    elif 'left' in keys:
        app.player.x -= 5
        app.player.currentMovement('left')
    else:
        app.player.currentMovement('idle')

    #add 'stair' logic below
    if 'up' in keys:
        app.player.y -= 5
        app.player.currentMovement('idle')
    elif 'down' in keys:
        app.player.y += 5
        app.player.currentMovement('idle')   


def main():
    runApp()
    
main()