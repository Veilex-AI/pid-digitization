from typing import Tuple


def denormalize_coordinates(normalized_box, image_width, image_height) -> Tuple[float, float, float, float]:
    (x_center_norm, y_center_norm, width_norm, height_norm) = normalized_box

    x_center = x_center_norm * image_width
    y_center = y_center_norm * image_height
    width = width_norm * image_width
    height = height_norm * image_height

    x1 = x_center - (width / 2)
    y1 = y_center - (height / 2)
    x2 = x_center + (width / 2)
    y2 = y_center + (height / 2)

    return (x1, y1, x2, y2)