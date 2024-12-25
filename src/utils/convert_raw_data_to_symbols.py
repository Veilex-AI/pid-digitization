from typing import List, Union

from src.models.vertex import Vertex
from src.models.symbol import Symbol


def convert_raw_data_to_symbols(raw_symbol_arr: List[Union[str, List[int], str]]):
    """
        converts raw PID dataset to python pydanctic symbol array
    """
    symbols: List[Symbol] = []
    for s in raw_symbol_arr:
        label = s[2]
        name = s[0]
        [x1, y1, x2, y2] = s[1]
        symbols.append(
            Symbol(
                name = name,
                label = str(label),
                pointSrc = Vertex(x=x1, y=y1),
                pointDest = Vertex(x=x2, y=y2)
            )
        )

    return symbols