import os
import json
import numpy
from PIL import Image

PROCESSED_DIRECTORY = './data/processed'
TESTING_DIRECTORY = './data/testing'

if os.path.isdir(PROCESSED_DIRECTORY) and not os.path.isfile('./categoryIndex.json'):
    with open('categoryIndex.json', 'w') as file:
        json.dump(sorted(os.listdir(PROCESSED_DIRECTORY)), file, indent=4)

def getInputsAndLabels(directory):
    inputs = []
    labels = []

    for i, categoryName in enumerate(sorted(os.listdir(directory))):
        categoryPath = f'{directory}/{categoryName}'
        for sketchName in os.listdir(categoryPath):
            sketchPath = f'{categoryPath}/{sketchName}'
            img = Image.open(sketchPath)

            arr = getInput(img)

            inputs.append(arr)
            labels.append(i)

    return numpy.array(inputs), numpy.array(labels)

def getInput(img):
    grayScaleImg = img.convert('L')

    arr = numpy.array(grayScaleImg) / 255.0
    arr = arr[..., numpy.newaxis]

    return arr

def getCategoryIndex():
    with open('categoryIndex.json', 'r') as file:
        return json.load(file)