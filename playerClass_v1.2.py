# for citations, see latest "mainTestingArea"

# uncomment lines below to test here
# from cmu_graphics import *
# def onAppStart(app):
#     app.width = 288*4
#     app.height = 192*4
#     app.player = Player(app.width/2, app.height/2)

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

# uncomment lines below to test here
# def redrawAll(app):
#     app.player.draw()
#     drawLabel(f'{app.player.getPosition()}', 100, 100)

# def main():
#     runApp()
    
# main()