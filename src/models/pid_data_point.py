from typing import List
from pydantic import BaseModel
from src.enums.annotation_type import AnnotationType
from src.models.line import Line
from src.models.symbol import Symbol
from src.models.bounding_box import BoundingBox

class PidDataPoint(BaseModel):
    symbols: List[Symbol] = []
    lines: List[Line] = []
    words: List[BoundingBox] = []
    image_path: str = ""

    def get_bounding_boxes(self, types: List[AnnotationType] = [AnnotationType.SYMBOLS, AnnotationType.LINES, AnnotationType.WORDS]) -> List[BoundingBox]:
        bounding_boxes = []
        if(AnnotationType.SYMBOLS in types): bounding_boxes.append(*self.symbols) 
        if(AnnotationType.LINES in types): bounding_boxes.append(*self.lines)
        if(AnnotationType.WORDS in types): bounding_boxes.append(*self.words)
        return bounding_boxes