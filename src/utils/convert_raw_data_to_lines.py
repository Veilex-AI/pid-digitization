from typing import List, Union

from src.models.line import Line
from src.models.vertex import Vertex


def convert_raw_data_to_lines(raw_line_arr: List[Union[str, List[int], str, str]]):
    """
        converts raw PID dataset to python pydanctic line array
    """
    lines: List[Line] = []
    for s in raw_line_arr:
        type = s[3]
        name = s[0]
        [x1, y1, x2, y2] = s[1]
        lines.append(
            Line(
                name = name,
                line_type = type,
                pointSrc = Vertex(x=x1, y=y1),
                pointDest = Vertex(x=x2, y=y2)
            )
        )

    return lines