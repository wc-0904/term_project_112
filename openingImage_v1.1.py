from cmu_graphics import *
from PIL import Image

FILENAME = 'images/player_running.png'
OUTPUT_SIZE = (6*50, 50)

input_spritesheet = Image.open(FILENAME)
print(f'Size: {input_spritesheet.size}')

resized_spritesheet = input_spritesheet.resize((OUTPUT_SIZE[0], OUTPUT_SIZE[1]))

resized_spritesheet.save('resized_spritesheet.png')

flipped_spritesheet = input_spritesheet.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)

flipped_spritesheet.save('flipped_spritesheet.png')

flipped_spritesheet.show()

# Image.new("RGB", (OUTPUT_SIZE[0]*gif.n_frames, OUTPUT_SIZE[1]))
# gif.show()

# for frame in range(0, gif.n_frames):
#     gif.seek(frame)
#     extracted = gif.resize(OUTPUT_SIZE)
#     position = (frame*OUTPUT_SIZE[0], 0)
#     sprite_sheet.paste(extracted, position)

# sprite_sheet.save("spritesheet.bmp")


def onAppStart(app):
    app.spriteCounter = 0
    app.stepCount = 0
    # app.stepsPerSecond = 10

    player_spritesheet = Image.open('resized_spritesheet.png')

    app.sprites = []
    for i in range(6):
        sprite = CMUImage(player_spritesheet.crop((50*i, 0, 50*(i+1), 50)))
        app.sprites.append(sprite)

def onStep(app):
    app.stepCount +=1
    if app.stepCount%3 == 0:
        app.spriteCounter = (1+app.spriteCounter) % len(app.sprites)

def redrawAll(app):
    currSprite = app.sprites[app.spriteCounter]
    drawImage(currSprite, app.width/2, app.height/2)

def main():
    runApp(width=400, height=400)

main()