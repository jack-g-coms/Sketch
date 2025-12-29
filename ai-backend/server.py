import utils.models as models
import utils.dataset as dataset
import utils.preprocess as preprocess
import numpy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apiModels import DrawingInput

app = FastAPI()
origins = [
    'http://localhost:3000',
    'https://sketch-murex.vercel.app'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*']
)
CATEGORY_INDEX = dataset.getCategoryIndex()

@app.post("/ai/predict/")
async def predict(data: DrawingInput):
    stableModel = models.getCurrentModel()
    img = preprocess.drawingStrokesToImage(data.drawing)

    input = dataset.getInput(img)
    input = (numpy.expand_dims(input, 0))

    singlePrediction = stableModel.predict(input)
    index = numpy.argmax(singlePrediction[0])
    prediction = CATEGORY_INDEX[index]

    return {'prediction': prediction}