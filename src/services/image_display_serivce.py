from typing import List
from PIL import Image
from PIL import ImageFile
import matplotlib.pyplot as plt
from src.models.bounding_box import BoundingBox


class ImageDisplayService:
    image_path: str = ""
    bounding_boxes: List[BoundingBox] = []
    labels: List[str] = []

    def __init__(self, image_path: str = "", bounding_boxes: List[BoundingBox] = []):
        self.image_path = image_path
        self.bounding_boxes = bounding_boxes

    def get_image(self):
        return Image.open(self.image_path)
    
    def display_image_with_bbox(self, color='red', dpi=200):
        """
            only supports matplot-lib.
        """
        plt.figure(figsize=(10, 8), dpi=dpi)
        plt.imshow(self.get_image())
        ax = plt.gca()

        for bbox in self.bounding_boxes:
            (x1, y1) = bbox.pointSrc.get_dimensions()
            (x2, y2) = bbox.pointDest.get_dimensions()

            width = x2 - x1
            height = y2 - y1

            rect = plt.Rectangle((x1, y1), width, height, fill=False, edgecolor=color, linewidth=0.2)
            ax.add_patch(rect)
            # ax.text(x1 + 8, y1 - 2, bbox=dict(facecolor=color, alpha=0.5, boxstyle="round,pad=0.2"), fontsize=8, color='white')

        plt.axis('off')
        plt.show()

    
