from cmu_graphics import *

def onAppStart(app):
    app.width = 288*4
    app.height = 192*4
    app.player = Player(app.width/2, app.height/2)

class Player():

    def __init__(self, x, y):

        # set the player location
        self.x = x
        self.y = y

        # insert player image here (empty for now)
        self.image = None
    
    # draw function to draw the player (using drawCircle for now)
    def draw(self):
        drawCircle(self.x, self.y, 7, fill='blue')
    
    def getPosition(self):
        return [self.x, self.y]

def redrawAll(app):
    app.player.draw()
    drawLabel(f'{app.player.getPosition()}', 100, 100)

def main():
    runApp()
    
main()