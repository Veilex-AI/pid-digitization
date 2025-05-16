import os

from src.models import Symbol, Line
from src.services import CropImageService, DataConverterService
from src.utils import convert_points_to_bounding_box
from config import config

"""
    A short code for providing an image with multiple but small cropped dimensions to select a subsection of pid for easy training.
    The images are stored in the upload dir path right after they have been cropped
"""

pid_cropped_part_of_image = [0, (4946, 2101, 5307, 2880)]

upload_dir = config.upload_path
cropped_image_samples = [0, (4946, 2101, 5307, 2880)]
cropped_image_coordinates = [
    [0, [(4946, 2101, 5307, 2880), (2523, 3827, 3466, 4043), (1650, 602, 2137, 1608)]],
    [1, [(4668, 3272, 5016, 4164), (720, 3335, 1846, 4183), (2662, 387, 3251, 634)]],
    [2, [(530, 3348, 1258, 4012), (555, 431, 1739, 1184), (3111, 1880, 3630, 2690)]],
]
num_columns = 3

dataService = DataConverterService()

for s_index, sample in enumerate(cropped_image_coordinates):
    datapoint = dataService.load_single_datapoint(str(sample[0]))

    for c_index, coordinates in enumerate(sample[1]):
        crop_image = CropImageService(
            datapoint.image_path,
            convert_points_to_bounding_box(
                coordinates
            )
        )

        # saving the image
        if not os.path.exists(f"{upload_dir}\\image_2"):
            os.makedirs(f"{upload_dir}\\image_2")
        crop_image.save_cropped_image(
            f"{upload_dir}\\image_2\\{s_index * num_columns + c_index}.jpg"
        )

        # saving those words that are associated with the image (those words that are within the cropped image are filtered in the npy file)
        crop_image.save_word_annotated_result_in_npy_format(
            [convert_points_to_bounding_box(an) for an in crop_image.adjust_filtered_annotations(annotations=datapoint.words)],
            f"{upload_dir}\\annotations\\{s_index * num_columns + c_index}\\{s_index * num_columns + c_index}_words.npy"
        )

        # save all the line annotations
        all_filtered_lines = []
        for line in datapoint.lines:
            ann = crop_image.adjust_filtered_annotations(annotations=[line])
            if(len(ann) == 0): continue
            bbox = convert_points_to_bounding_box(
                ann[0]
            )
            all_filtered_lines.append(
                Line(
                    name= line.name,
                    line_type= line.line_type,
                    pointSrc=bbox.pointSrc,
                    pointDest=bbox.pointDest
                )
            ) 
        crop_image.save_line_annotated_result_in_npy_format(
                all_filtered_lines,
                f"{upload_dir}\\annotations\\{s_index * num_columns + c_index}\\{s_index * num_columns + c_index}_lines.npy"
        )
    
        # save all the symbol annotations.
        all_filtered_symbols = []
        for symbol in datapoint.symbols:
            ann = crop_image.adjust_filtered_annotations(annotations=[symbol])
            if(len(ann) == 0): continue
            bbox = convert_points_to_bounding_box(
                ann[0]
            )
            all_filtered_symbols.append(
                Symbol(
                    name= symbol.name,
                    label=symbol.label,
                    pointSrc=bbox.pointSrc,
                    pointDest=bbox.pointDest
                )
            )
        crop_image.save_symbol_annotated_result_in_npy_format(
            all_filtered_symbols,
            f"{upload_dir}\\annotations\\{s_index * num_columns + c_index}\\{s_index * num_columns + c_index}_symbols.npy"
        )

