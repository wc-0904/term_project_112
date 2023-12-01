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
            drawCircle(self.x, self.y, 7, fill='blue')
        else:
            if self.animationList != []:
                currSprite = self.animationList[app.spriteCounter]
                drawImage(currSprite, self.x, self.y)
        
    
    # this checks what movement the player is doing (running or idling)
    def currentMovement(self, key):

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
                   
    

    def getPosition(self):
        return [self.x, self.y]

# uncomment lines below to test here
# def redrawAll(app):
#     app.player.draw()
#     drawLabel(f'{app.player.getPosition()}', 100, 100)

# def main():
#     runApp()
    
# main()