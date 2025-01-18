from typing import List, Tuple
from config import config
import time
from ultralytics import YOLO
from src.utils.segment_image import segment_image
from PIL import ImageFile, Image


class PredictSymbolsService:
    model_path: str
    image_path: str = ""
    model: YOLO = None

    def __init__(self, image_path: str = ""):
        self.image_path = image_path
        self.model_path = config.model_path

    def get_image(self) -> ImageFile:
        """
            retunrs a PIL Image
        """
        return Image.open(self.image_path)

    def predict_bounding_boxes(self) -> List[Tuple[Tuple[float, float, float, float], str]]:
        """
            identify the symbols through bounding boxes (x1, x2, y1, y2) using a pretrained YOLO model. 
            update: use the window shift method (remove this bracket comment if this is completed )
        """
        if(self.model is None): self.load_model()

        start = time.time()
        chunks_arr = segment_image(self.get_image(), chunk_size=1800)
        bboxes: List[Tuple[Tuple[float, float, float, float], str]] = []
        for i, row in enumerate(chunks_arr):
            for j, chunk in enumerate(row):
                result: list[YOLO] = self.model(source=chunk)

                # offset the chunks to the image of original size.
                chunk_width, chunk_height = chunk.size
                x_offset = i * chunk_width
                y_offset = j * chunk_height

                boxes = result[0].boxes
                for box in boxes:
                    x_min, y_min, x_max, y_max = box.xyxy[0].tolist()
                    c = box.cls

                    width = x_max - x_min
                    height = y_max - y_min
                    updated_x_min = x_min + x_offset
                    updated_y_min = y_min + y_offset

                    b = [updated_x_min, updated_y_min, updated_x_min + width, updated_y_min + height]

                    bboxes.append((b, self.model.names[int(c)]))

        print(f"time took to finish prediction: { time.time() - start }")

        return bboxes
    
    def load_model(self) -> None:
        """
            initialize the YOLO model
        """
        self.model = YOLO(self.model_path)