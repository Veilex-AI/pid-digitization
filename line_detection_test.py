# %%
from src.services.data_converter_service import DataConverterService

data_converter_service = DataConverterService()
datapoint = data_converter_service.load_single_datapoint(str(1))

# %%
from src.services.line_detection_service import LineDetectionService

line_detection_service = LineDetectionService(
    image_path=datapoint.image_path,
    bounding_boxes=[*datapoint.symbols, *datapoint.words]
)
line_segments = line_detection_service.detect_line_segments(True)



# %%
from src.models.bounding_box import BoundingBox
from src.models.vertex import Vertex


def convert_points_to_bbox(points):
    arr_list = []
    for point in points:
        [x1, y1, x2, y2] = point
        src = Vertex(x=x1, y=y1)
        dest = Vertex(x=x2, y=y2)
        arr_list.append(
            BoundingBox(
                name="",
                pointDest=dest,
                pointSrc=src
            )
        )

    return arr_list


segments_bbox = convert_points_to_bbox(line_segments)

# %%
from src.services.image_display_serivce import ImageDisplayService


dispaly = ImageDisplayService(
    image_path= datapoint.image_path,
    bounding_boxes= segments_bbox
)

dispaly.display_image_with_bbox(color='red', dpi=400)
# %%
