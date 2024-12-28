

import os
from typing import List, Tuple
from PIL import Image
from PIL.ImageFile import ImageFile
import numpy as np

from src.models.line import Line
from src.models.symbol import Symbol
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
    
    def save_cropped_image(self, save_path: str):
        """
            thake the path of the image and save it to the desired directory that comes from the parameters.
        """
        image  = self.crop_image()
        if image is not None:
            image.save(save_path)
        else:
            raise Exception("Image file not available")
        

    # below there are three functions described but they are absolutely doing the same thing. this needs to be changed. 

    def save_line_annotated_result_in_npy_format(self, annotations: List[Line], save_path: str):
        arr = []
        for annotate in annotations:
            name = annotate.name
            line_type = annotate.line_type
            (x1, y1) = annotate.pointSrc.get_dimensions()
            (x2, y2) = annotate.pointDest.get_dimensions()

            arr.append([name, [x1, y1, x2, y2], line_type])

        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        
        np.save(save_path, np.array(arr, dtype=object))

    def save_symbol_annotated_result_in_npy_format(self, annotations: List[Symbol], save_path: str):
        arr = []
        for annotate in annotations:
            name = annotate.name
            label = annotate.label
            (x1, y1) = annotate.pointSrc.get_dimensions()
            (x2, y2) = annotate.pointDest.get_dimensions()

            arr.append([name, [x1, y1, x2, y2], label])
        
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        
        np.save(save_path, np.array(arr, dtype=object))

    def save_word_annotated_result_in_npy_format(self, word_annotations: List[BoundingBox], save_path: str):
        arr = []
        for annotate in word_annotations:
            name = annotate.name
            (x1, y1) = annotate.pointSrc.get_dimensions()
            (x2, y2) = annotate.pointDest.get_dimensions()

            arr.append([name, [x1, y1, x2, y2]])

        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))

        np.save(save_path, np.array(arr, dtype=object))