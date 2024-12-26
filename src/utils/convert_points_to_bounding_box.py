from typing import List

from models.bounding_box import BoundingBox
from models.vertex import Vertex


def convert_points_to_bounding_box(points: List[List[float, float, float, float]]):
    arr_list = []
    for point in points:
        [x1, y1, x2, y2] = point
        src = Vertex(x=x1, y=y1)
        dest = Vertex(x=x2, y=y2)
        arr_list.append(
            BoundingBox(
                name="",
                pointDest=dest,
                pointSrc=src
            )
        )

    return arr_list