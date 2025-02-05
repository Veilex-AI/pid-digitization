def azure_polygon_to_bbox(polygon_data):
    """
        Get bounding box coordinates from datastructure provided by azure document inteligence
    """
    polygon_points = [(polygon_data[i], polygon_data[i + 1]) for i in range(0, len(polygon_data), 2)]

    all_x = [point[0] for point in polygon_points]
    all_y = [point[1] for point in polygon_points]

    return [min(all_x), min(all_y), max(all_x), max(all_y)]