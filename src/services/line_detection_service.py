from typing import List
import cv2
import numpy as np

from src.models.bounding_box import BoundingBox

class LineDetectionService:
    image_path: str
    bounding_boxes: List[BoundingBox] = []

    def __init__(self, image_path, bounding_boxes):
        self.image_path = image_path
        self.bounding_boxes = bounding_boxes

    def detect_line_segments(self, enable_thining=True):
        preprocessed_image = self.pre_process_image(enable_thining)
        line_segments = cv2.HoughLinesP(
            preprocessed_image, rho=0.1,
            theta=np.pi / 1080,
            threshold=5,
            minLineLength=10,
            maxLineGap=None
        )

        return line_segments
    
    def pre_process_image(self, enable_thining=False):
        """
            pre process the image before the lines can be detected. makes the image black and white by removing the RGB vlaues.
            removes the bounding boxes (symbol and words) to only leave the lines behind so that they can be detected.
        """
        # 1. read image in cv2
        image = cv2.imread(self.image_path)

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