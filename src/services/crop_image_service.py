

from typing import List, Tuple
from PIL import Image
from PIL.ImageFile import ImageFile

from src.models.bounding_box import BoundingBox


class CropImageService:
    image_path: str
    cropped_dimensions: BoundingBox = None

    def __init__(self, image_path: str, cropped_dimensions: BoundingBox):
        self.image_path = image_path
        self.cropped_dimensions = cropped_dimensions


    def get_image(self):
        return Image.open(self.image_path)

    def crop_image(self) -> ImageFile:
        (x1, y1) = self.cropped_dimensions.pointSrc.get_dimensions()
        (x2, y2) = self.cropped_dimensions.pointDest.get_dimensions()

        cropped_image = self.get_image().crop((x1, y1, x2, y2))

        return cropped_image
        

    def adjust_filtered_annotations(self, annotations: List[BoundingBox]):
        new_annotations: List[Tuple[float, float, float, float]] = []
        for annotate in annotations:
            (x1, y1) = annotate.pointSrc.get_dimensions()
            (x2, y2) = annotate.pointDest.get_dimensions()

            (_x1, _y1) = self.cropped_dimensions.pointSrc.get_dimensions()
            (_x2, _y2) = self.cropped_dimensions.pointDest.get_dimensions()

            if x1 >= _x1 and y1 >= _y1 and x2 <= _x2 and y2 <= _y2:
                new_annotations.append(
                    [x1 - _x1, y1 - _y1, x2 - _x1, y2 - _y1]
                )

        return new_annotations
    
    def save_cropped_image():
        pass