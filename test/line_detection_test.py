# %%
from src.services import DataConverterService, LineDetectionService, ImageDisplayService
from src.utils import convert_points_to_bounding_box


def detect_line_segments():
    # %%
    data_converter_service = DataConverterService()
    datapoint = data_converter_service.load_single_datapoint(str(1))

    # %%
    line_detection_service = LineDetectionService(
        image_path=datapoint.image_path,
        bounding_boxes=[*datapoint.symbols, *datapoint.words]
    )
    line_segments = line_detection_service.detect_line_segments(True)

    # %%
    segments_bbox = [convert_points_to_bounding_box(ls) for ls in line_segments]

    # %%
    dispaly = ImageDisplayService(
        image_path= datapoint.image_path,
        bounding_boxes= segments_bbox
    )

    dispaly.display_image_with_bbox(color='red', dpi=400)



if __name__ == "__main__":
    detect_line_segments()