import math
import cv2
import numpy as np
from shapely.geometry import Point
from typing import List

from src.models import BoundingBox
from src.utils import get_slope_between_points, calculate_distance_between_points

class LineDetectionService:
    image_path: str = ""
    # the bounding boxes are used to clean the symbols and the words that are present in the document.
    bounding_boxes: List[BoundingBox] = []
    line_padding: float = 8
    line_thickness: float = 2
    

    def __init__(self, image_path: str = "", bounding_boxes: List[BoundingBox] = []):
        self.image_path = image_path
        self.bounding_boxes = bounding_boxes

    def get_image(self):
        """
            get the image in OpenCV compatible format.
        """
        return cv2.imread(self.image_path)
        

    def detect_line_segments(self, enable_thining=True):
        preprocessed_image = self.pre_process_image(enable_thining)
        line_segments = cv2.HoughLinesP(
            preprocessed_image, rho=0.1,
            theta=np.pi / 1080,
            threshold=5,
            minLineLength=10,
            maxLineGap=None
        )

        return [ ls[0] for ls in line_segments ]
        
    
    def pre_process_image(self, enable_thining=False):
        """
            pre process the image before the lines can be detected. makes the image black and white by removing the RGB vlaues.
            removes the bounding boxes (symbol and words) to only leave the lines behind so that they can be detected.
        """
        # 1. read image in cv2
        image = self.get_image()

        # 2. Clear symbol and word bounding boxes
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        background_value = int(np.argmax(hist))

        if(len(self.bounding_boxes) == 0):
            return
        
        for bb in self.bounding_boxes:
            topX, topY, bottomX, bottomY = bb.pointSrc.x, bb.pointSrc.y, bb.pointDest.x, bb.pointDest.y
            points = np.array([[bottomX, topY],
                               [bottomX, bottomY],
                               [topX, bottomY],
                               [topX, topY]],
                              np.int32)
            cv2.fillPoly(image, [points], (background_value, background_value, background_value))

        # 3. Convert to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 4. Binarization
        image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        if enable_thining:
            processed_image_with_thining = cv2.ximgproc.thinning(image, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
            image = processed_image_with_thining

        return image

    def extend_lines(self, line_segments = []):
        '''
            Increases the length of the line segments for easier interaction detection beteween line to line and line to symbol interconnections.
            vertical line increases vertically.
            horizontal line increases horizontally.

            param line_segments: List[(startX, startY, endX, endY)] (0, 1, 2, 3)
            param line_segment_padding_default: padding provided in the config
        '''
        padding = self.line_padding
        thickness = self.line_thickness
        extended_line_segments = []

        for line in line_segments:
            slope = get_slope_between_points(line[0], line[1],
                                            line[2], line[3])
            
            startX, startY, endX, endY = line[0], line[1], line[2], line[3]

            updated_padding = self.get_line_padding(startX, startY, endX, endY)

            b = 0
            if slope != math.inf:
                b = startY - slope * startX
            
            if slope == math.inf:
                start_x = startX - thickness
                end_x = endX + thickness

                y1 = startY + updated_padding
                y2 = endY - updated_padding
                first = Point(start_x, y1)
                second = Point(end_x, y2)
                
                source_line_distance_after_padding = first.distance(second)

                _y1 = startY - updated_padding
                _y2 = endY + updated_padding

                _first = Point(start_x, _y1)
                _second = Point(end_x, _y2)

                dest_line_distance_after_padding = _first.distance(_second)

                if source_line_distance_after_padding > dest_line_distance_after_padding:            
                    start_y = y1
                    end_y = y2
                else:
                    start_y = _y1
                    end_y = _y2
            else:
                start_x = startX - updated_padding
                start_y = slope * start_x + b + thickness
                end_x = endX + updated_padding
                end_y = slope * end_x + b - thickness

            extended_line_segments.append(
                [
                    start_x,
                    start_y,
                    end_x,
                    end_y
                ]
            )

        return extended_line_segments
    
    def get_line_padding(self, startX, startY, endX, endY, multiplier = 2):
        """
            increase the padding with a multiplier if the line is too short.
        """
        distance = calculate_distance_between_points((startX, startY), (endX, endY))
        if distance < 40:
            return self.line_padding * multiplier
        return self.line_padding
