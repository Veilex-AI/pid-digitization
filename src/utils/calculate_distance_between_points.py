import math


def calculate_distance_between_points(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    return math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )