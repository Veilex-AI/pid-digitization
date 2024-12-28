from typing import List, Union

from src.models.bounding_box import BoundingBox
from src.models.vertex import Vertex


def convert_raw_data_to_bounding_box(raw_bb_arr: List[Union[str, List[int], str, str]]):
    """
        converts raw PID dataset to python pydanctic bounding box array
    """
    bounding_box_list: List[BoundingBox] = []
    for bb in raw_bb_arr:
        name = bb[0]
        [x1, y1, x2, y2] = bb[1]
        bounding_box_list.append(
            BoundingBox(
                name = name,
                pointSrc = Vertex(x=x1, y=y1),
                pointDest = Vertex(x=x2, y=y2)
            )
        )

    return bounding_box_list