from typing import Tuple

from src.models.bounding_box import BoundingBox
from src.models.vertex import Vertex


def convert_points_to_bounding_box(point: Tuple[float, float, float, float]):
    (x1, y1, x2, y2) = point
    src = Vertex(x=x1, y=y1)
    dest = Vertex(x=x2, y=y2)
    return BoundingBox(
        name="",
        pointDest=dest,
        pointSrc=src
    )