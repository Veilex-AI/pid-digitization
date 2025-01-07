import math

def calculate_distance_between_rectangles(box1, box2):
    """
        Use Euclidean distance to find distance between 2 rectangle center points.
    """
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2

    center1_x = (x1 + x2) / 2
    center1_y = (y1 + y2) / 2
    center2_x = (x3 + x4) / 2
    center2_y = (y3 + y4) / 2

    distance = math.sqrt((center2_x - center1_x) ** 2 + (center2_y - center1_y) ** 2)
    return distance