import os
from src.services.crop_image_service import CropImageService
from src.services.data_converter_service import DataConverterService
from src.utils.segment_image_dimensions import segment_image_dimensions
from src.utils.convert_points_to_bounding_box import convert_points_to_bounding_box
from src.utils.normalize_coordinates import normalize_coordinates
from PIL import Image
from config import config

def create_dataset_data_segments(chuck_size: int):
    """
        create small segments of each and every datapoint image and save them back in a different path.
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

            labels_with_normalized_coordinates = []
            (image_width, image_height) = service.get_image_dimensions()
            
            
            service.save_cropped_image(f"{config.upload_path}/images/{dp_index}_{s_index}.jpg")

            # save labeled annoations in text based format.
            # for every line, there is a label followed by 4 coordinates (i.e. '5' 0.4 0.2 0.5 0.1)
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
    create_dataset_data_segments(3200)