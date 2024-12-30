from shapely import Polygon

def bounding_box_to_polygon(topX, topY, bottomX, bottomY):
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
    polygon = Polygon(coords)
    return polygon