from typing import Tuple


def normalize_coordinates(pixel_box, image_width, image_height) -> Tuple[float, float, float, float]:
    (x1, y1, x2, y2) = pixel_box

    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    
    width = x2 - x1
    height = y2 - y1
    
    x_center_normalized = x_center / image_width
    y_center_normalized = y_center / image_height
    width_normalized = width / image_width
    height_normalized = height / image_height
    
    return (x_center_normalized, y_center_normalized, width_normalized, height_normalized)