from shapely import LineString, Polygon

def bounding_box_to_polygon(topX, topY, bottomX, bottomY, type = "Polygon"):
    '''Converts a bounding box to coordinates.

    :param bounding_box: The bounding box.
    :return: The coordinates.
    :rtype: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]
    '''
    coords = (
        (topX, topY),
        (bottomX, topY),
        (bottomX, bottomY),
        (topX, bottomY)
    )
    polygon = None

    if type == "LineString":
        polygon = LineString(coords)
    else:
        polygon = Polygon(coords)
    return polygon