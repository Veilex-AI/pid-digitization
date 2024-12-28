import math


def get_slope_between_points(x1, y1, x2, y2):
    '''
    Returns the slope between two points.
    '''
    x_delta = x2 - x1
    if x_delta == 0:
        return math.inf
    return (y2 - y1) / x_delta