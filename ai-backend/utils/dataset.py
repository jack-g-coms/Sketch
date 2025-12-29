import os
import random
import numpy
from PIL import Image

PROCESSED_DIRECTORY = './data/processed'
TESTING_DIRECTORY = './data/testing'
CATEGORY_INDEX = sorted(os.listdir(PROCESSED_DIRECTORY))

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