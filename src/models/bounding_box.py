from pydantic import BaseModel
from src.models.vertex import Vertex

class BoundingBox(BaseModel):
    """
        represents a bounding box with source and destination point.
    """
    name: str
    pointSrc: Vertex
    pointDest: Vertex