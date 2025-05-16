from src.models import BoundingBox, Vertex
from src.services import CropImageService, DataConverterService, ImageDisplayService, LineDetectionService


"""
    DEPRECATED:
    In this example we test out the line detection technique using hough transform.
    the lines are predicted by the opencv model. however, the opencv model requires that the other artifacts such as 
    symbols and words should be removed for only the lines to be remained so that they can traced in the image.

    hence, for this purposes only the symbols and the words are taken from training dataset itself. but in future we will use 
    our techniques (which already exist) to predict symbol and text recognition before performing line tracing through the pid document. 
"""

data_converter_service = DataConverterService()

original_datapoints = [
    data_converter_service.load_single_datapoint(str(0)),
    data_converter_service.load_single_datapoint(str(1)),
    data_converter_service.load_single_datapoint(str(2))
]

cropped_datapoints = [461, 368, 5358, 4309]


def get_shortning_images_data():
    """
        returns cropped image and filtered annoations of original sample image based on its cropped sized that is provided in the array (subjected to change).
    """

    cropped_datapoints = []

    shortened_images = [
        # [0, (4946, 2101, 5307, 2880)],
        # [0, (2523, 3827, 3466, 4043)],
        # [0, (1650, 602, 2137, 1608)],
        # [1, (4668, 3272, 5016, 4164)],
        # [1, (720, 3335, 1846, 4183)],
        [1, (2662, 387, 3251, 634)],
        # [2, (530, 3348, 1258, 4012)],
        # [2, (555, 431, 1739, 1184)],
        # [2, (3111, 1880, 3630, 2690)]
    ]

    for sm in shortened_images:
        
        crop_service = CropImageService(
            image_path=original_datapoints[sm[0]].image_path,
            cropped_dimensions=BoundingBox(
                name="",
                pointSrc=Vertex(x=sm[1][0], y=sm[1][1]),
                pointDest=Vertex(x=sm[1][2], y=sm[1][3])
            )
        )

        filtered_words= [
            BoundingBox(name="", pointSrc=Vertex(x=c[0], y=c[1]), pointDest=Vertex(x=c[2], y=c[3])) 
            for c in crop_service.adjust_filtered_annotations(
                original_datapoints[sm[0]].words
            )
        ]

        filtered_symbols= [
            BoundingBox(name="", pointSrc=Vertex(x=c[0], y=c[1]), pointDest=Vertex(x=c[2], y=c[3])) 
            for c in crop_service.adjust_filtered_annotations(
                original_datapoints[sm[0]].symbols
            )
        ]

        service = LineDetectionService(
            image_pil=crop_service.crop_image(),
            bounding_boxes=[*filtered_symbols, *filtered_words]
        )
        line_segments = service.detect_line_segments(True)

        # non bounding box format
        filtered_lines = [
            BoundingBox(name="", pointSrc=Vertex(x=e[0], y=e[1]), pointDest=Vertex(x=e[2], y=e[3]))
            for e in  service.extend_lines(
                line_segments
            )    
        ]

        cropped_datapoints.append(
            {
                'words': filtered_words,
                'symbols': filtered_symbols,
                'lines': filtered_lines,
                'image': crop_service.crop_image()
            }
        )

    return cropped_datapoints

cropped_datapoints = get_shortning_images_data()

for c in cropped_datapoints:
    display = ImageDisplayService(
        image_pil=c['image'],
        bounding_boxes=[ *c['words'], *c['symbols'], *c['lines'] ]
    )

    display.display_image_with_bbox()