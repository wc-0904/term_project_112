class Bullet():

    def __init__(self, x, y, char, angle):
        
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
        print(self.angle)

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

        # decrement timer
        self.timer -= 1

        # different pattern to be added below
        # ...

        # self deletion logic, ****add enemy collision logic here
        if (self.timer == 0):
            app.bulletList.remove(self)
