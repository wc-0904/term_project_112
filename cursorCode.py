from cmu_graphics import *

def onAppStart(app):
    app.width = 288*4
    app.height = 192*4
    app.c1x = app.width/2       #inner circle X
    app.c1y = app.height/2      #inner circle Y
    app.c2x = app.width/2       #outer circle X
    app.c2y = app.height/2      #outer circle Y
    app.c2r = 10                #outer circle radius
    app.refX = app.width/2
    app.refY = app.height/2
    app.distFromRef = distance(app.c2x, app.c2y, app.refX, app.refY)

def cursorUpdate(app, mouseX, mouseY):      #assigns cursor center to mouse location
    app.c1x = app.c2x = mouseX
    app.c1y = app.c2y = mouseY
    app.distFromRef = distance(app.c2x, app.c2y, app.refX, app.refY)
    if app.distFromRef > 60:                #this determines how far the cursor goes without changing shape
        app.c2r = app.distFromRef/6         #this has to be updated along with distFromRef, divide by the 'threshold/10'
    else:
        app.c2r = 10

def distance(x0, y0, x1, y1):                   #helper
    return ((x1-x0)**2 + (y0-y1)**2)**0.5

def redrawAll(app):
    drawCircle(app.c1x, app.c1y, 3, fill='black', border=None)      #draws inner circle
    drawCircle(app.c2x, app.c2y, app.c2r, fill=None, border='black')
    drawCircle(app.refX, app.refY, 7, fill='blue')           #reference circle, this would be the players position in game

def onMouseMove(app, mouseX, mouseY):
    app.lastMouseX = mouseX
    app.lastMouseY = mouseY             #'remembers' last mouse location

def onMouseDrag(app, mouseX, mouseY):
    app.lastMouseX = mouseX
    app.lastMouseY = mouseY             #'remembers' last mouse location

def onStep(app):
    app.distFromRef = distance(app.c2x, app.c2y, app.refX, app.refY)    #updates ref distance on every step
    cursorUpdate(app, app.lastMouseX, app.lastMouseY)                   #calls update func on every step

def onKeyHold(app, keys):
    if 'right' in keys:
        app.refX += 5
    elif 'left' in keys:
        app.refX -= 5
    if 'up' in keys:
        app.refY -= 5
    elif 'down' in keys:
        app.refY += 5    

def main():
    runApp()

main()

