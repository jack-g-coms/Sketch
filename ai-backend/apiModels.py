from pydantic import BaseModel
from typing import List

Stroke = List[List[int]]
class DrawingInput(BaseModel):
    drawing: List[Stroke]