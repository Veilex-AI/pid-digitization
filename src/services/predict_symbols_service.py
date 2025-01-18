from collections import defaultdict
from typing import Dict, List, Tuple
from config import config
import time
from ultralytics import YOLO
from src.services.crop_image_service import CropImageService
from src.utils.segment_image_dimensions import segment_image_dimensions
from src.utils.calculate_distance_between_rectangles import calculate_distance_between_rectangles
from src.utils.convert_points_to_bounding_box import convert_points_to_bounding_box
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
        if(self.model is None):
            self.load_model()

        start = time.time()

        total_bounding_boxes_with_shifts = []
        for shift in range(0, 500, 100):
            dimensions = segment_image_dimensions(
                image=self.get_image(),
                chunk_size=1088,
                shift=shift
            )
            total_bounding_boxes = []
            for index, dim in enumerate(dimensions):
                crop_service = CropImageService(
                    image_path=self.image_path,
                    cropped_dimensions=convert_points_to_bounding_box(dim)
                )
                # cropped image dimensions can come from here
                chunk = crop_service.crop_image()
                result = self.model(source=chunk)

                bboxes = result[0].boxes
                
                for box in bboxes:
                    # values of bounding box w.r.t the cropped image
                    x_min, y_min, x_max, y_max = box.xyxy[0].tolist()

                    c = self.model.names[int(box.cls[0])]
                    x1_full = x_min + dim[0]
                    y1_full = y_min + dim[1]
                    x2_full = x_max + dim[0]
                    y2_full = y_max + dim[1]

                    b = [x1_full, y1_full, x2_full, y2_full]

                    total_bounding_boxes.append((b, c))

            # the shifts are ignored for now, we only consider the first shift. 
            total_bounding_boxes_with_shifts = [*total_bounding_boxes_with_shifts, *total_bounding_boxes]

        updated_bbox_values = self.filter_largest_bbox_area(
            self.group_closest_points(total_bounding_boxes, 70)            
        )

        print(f"time took to finish prediction: { time.time() - start }")    
        
        return updated_bbox_values

    
    def group_closest_points(self, bounding_boxes: List[Tuple[List[int], str]], threshold: int) -> Dict[int, List[Tuple[List[int], str]]]:
        groups = defaultdict(list)
        visited = set()
        group_id = 0

        for i, bbox_from in enumerate(bounding_boxes):
            if i in visited:
                continue

            # Start a new group
            group_id += 1
            groups[group_id].append(bbox_from)
            visited.add(i)

            # Compare with remaining points
            for j, bbox_to in enumerate(bounding_boxes):
                bbox_from_point = bbox_from[0]
                bbox_to_point = bbox_to[0]
                if j not in visited and calculate_distance_between_rectangles(bbox_from_point, bbox_to_point) <= threshold:
                    groups[group_id].append(bbox_to)
                    visited.add(j)

        return dict(groups)
        
    def filter_largest_bbox_area(self, bbox_groups: Dict[int, Tuple[List[int], str]]) -> Tuple[List[int], str]:
        new_bounding_box_array = []

        def calculate_bbox_area(bbox):
            x, y, _x, _y = bbox
            return abs(_y - y) * abs(_x - x)

        for bbox_group in bbox_groups.values():
            max_area_index = 0
            for index, bbox in enumerate(bbox_group):
                if calculate_bbox_area(bbox[0]) > calculate_bbox_area(bbox_group[max_area_index][0]):
                    max_area_index = index
            
            new_bounding_box_array.append(
                bbox_group[max_area_index]
            )

        return new_bounding_box_array

    def load_model(self) -> None:
        """
            initialize the YOLO model
        """
        self.model = YOLO(self.model_path)



# class areas.
# class_sizes = {'21': 1985, '2': 5415, '18': 6969, '26': 17849, '8': 7037, '20': 6110, '25': 6532, '32': 16411, '28': 17179, '7': 6771, '9': 6689, '12': 5510, '22': 5795, '24': 2808, '11': 6129, '23': 8645, '29': 17181, '4': 6132, '31': 16001, '5': 4808, '15': 3737, '17': 5721, '19': 6769, '30': 11940, '16': 3564, '13': 6558, '1': 4575, '6': 3126, '10': 8179, '27': 18761, '14': 13607, '3': 6903}
