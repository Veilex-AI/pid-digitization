import os
from PIL import Image

from src.services import CropImageService, DataConverterService
from src.utils import segment_image_dimensions, convert_points_to_bounding_box, normalize_coordinates
from config import config

def create_dataset_data_segments(chuck_size: int):
    """
        create small segments of each and every datapoint image and save them back in a different path alogside their filtered annoations in YOLO based text format.
    """
    data_converter_service = DataConverterService()
    datapoints = data_converter_service.load_dataset()


    for dp_index, datapoint in enumerate(datapoints):
        image = Image.open(datapoint.image_path)
        for s_index, segment_dimension in enumerate(segment_image_dimensions(chunk_size=chuck_size, image=image)):
            service = CropImageService(
                image_path=datapoint.image_path,
                cropped_dimensions=convert_points_to_bounding_box(segment_dimension)
            )

            filtered_symbols = service.adjust_filtered_symbols(
                annotations=[*datapoint.symbols]
            )

            if(len(filtered_symbols) == 0):
                continue

            (image_width, image_height) = service.get_image_dimensions()
            
            
            service.save_cropped_image(f"{config.upload_path}/images/{dp_index}_{s_index}.jpg")

            # save labeled annoations in text based format (for YOLO object detection training).
            # for every line, there is a label (type of symbol is also a label) followed by 4 normalized (with range 0-1) coordinates (i.e. '5' 0.4 0.2 0.5 0.1)
            label_path_file = f"{config.upload_path}/labels/{dp_index}_{s_index}.jpg.txt"
            os.makedirs(os.path.dirname(label_path_file), exist_ok=True)
            with open(label_path_file, 'w') as file:
                for fs in filtered_symbols:
                    (x1, x2, y1, y2) = normalize_coordinates(fs[1], image_width, image_height)
                    file.write(
                        f"{fs[0]} {x1} {x2} {y1} {y2}" + "\n" 
                    )

            print(
                f"datapoint {dp_index} with segment {s_index} has been saved with an image and annoatation."
            )
                    

if __name__ == "__main__":
    create_dataset_data_segments(1088)