import matplotlib.pyplot as plt
import networkx as nx
from typing import List
from PIL import Image, ImageFile

from src.models import BoundingBox

class ImageDisplayService:
    image_path: str = ""
    bounding_boxes: List[BoundingBox] = []
    labels: List[str] = []

    def __init__(self, image_path: str = "", bounding_boxes: List[BoundingBox] = []):
        self.image_path = image_path
        self.bounding_boxes = bounding_boxes

    def get_image(self) -> ImageFile:
        """
            get the image
        """
        return Image.open(self.image_path)
    
    def display_image_with_bbox(self, color='red', dpi=200, show_text=True) -> None:
        """
            displays image using matplot lib
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
            if(show_text):
                ax.text(x1 + 8, y1 - 2, bbox.name, bbox=dict(facecolor=color, alpha=0.5, boxstyle="round,pad=0.2"), fontsize=8, color='white')

        plt.axis('off')
        plt.show()

    def display_graph(self, graph, node_size=100) -> None:
        """
            displays a graph in matplotlib with nx support.
        """
        plt.clf()
        plt.figure(figsize=(8, 6))
        nx.draw(graph, with_labels=True, node_size=node_size, node_color="lightgreen", font_size=10, font_weight="bold")
        plt.title("Undirected Graph")
        plt.show()

    
