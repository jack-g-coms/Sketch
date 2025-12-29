from PIL import Image, ImageDraw
from utils.dataset import PROCESSED_DIRECTORY, TESTING_DIRECTORY
import os
import json

RAW_DIRECTORY = './data/raw'
FIXED_SIZE = (36, 36)
CONTENT_SIZE = (36, 36)
MAX_SAMPLES = 820
PERCENT_TESTING_SAMPLES = 0.05

def drawingStrokesToImage(drawing):
    allX = [x for stroke in drawing for x in stroke[0]]
    allY = [y for stroke in drawing for y in stroke[1]]

    minX, maxX = min(allX), max(allX)
    minY, maxY = min(allY), max(allY)

    scaleX = (CONTENT_SIZE[0] - 1) / (maxX - minX) if maxX != minX else 1
    scaleY = (CONTENT_SIZE[1] - 1) / (maxY - minY) if maxY != minY else 1
    scale = min(scaleX, scaleY)

    tempImg = Image.new('L', CONTENT_SIZE, color=255)
    draw = ImageDraw.Draw(tempImg)

    for stroke in drawing:
        x, y = stroke
        coords = [
            (
                (xi - minX) * scale,
                (yi - minY) * scale
            )
            for xi, yi in zip(x, y)
        ]

        if len(coords) > 1:
            draw.line(coords, fill=0, width=1)

    finalImg = Image.new('L', FIXED_SIZE, color=255)
    offset = (FIXED_SIZE[0] - CONTENT_SIZE[0]) // 2
    finalImg.paste(tempImg, (offset, offset))

    return finalImg

def prepareImages():
    testingSamples = MAX_SAMPLES * PERCENT_TESTING_SAMPLES
    testingInterval = MAX_SAMPLES // testingSamples

    for name in os.listdir(RAW_DIRECTORY):
        if name.endswith('.ndjson'):
            filePath = os.path.join(RAW_DIRECTORY, name)
            splitName = name.split('.')

            category = splitName[0].title()
            os.makedirs(f'{PROCESSED_DIRECTORY}/{category}')
            os.makedirs(f'{TESTING_DIRECTORY}/{category}')

            count = 0
            
            with open(filePath, 'r') as file:
                for line in file:
                    if count >= MAX_SAMPLES:
                        break

                    data = json.loads(line.strip())
                    img = drawingStrokesToImage(data['drawing'])

                    if count % testingInterval == 0:
                        img.save(f'{TESTING_DIRECTORY}/{category}/{count}.png', 'PNG')
                    else:
                        img.save(f'{PROCESSED_DIRECTORY}/{category}/{count}.png', 'PNG')

                    count += 1

if __name__ == '__main__':
    prepareImages()