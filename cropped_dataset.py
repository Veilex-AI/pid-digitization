import os
from src.models.symbol import Symbol
from src.models.line import Line
from src.services.crop_image_service import CropImageService
from src.services.data_converter_service import DataConverterService
from src.utils.convert_points_to_bounding_box import convert_points_to_bounding_box

from config import config

pid_cropped_part_of_image = [0, (4946, 2101, 5307, 2880)]

upload_dir = "D:\\Volume C\\dataset\\cropped"
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
        for point in datapoint.lines:
            ann = crop_image.adjust_filtered_annotations(annotations=[point])
            if(len(ann) == 0): continue
            bbox = convert_points_to_bounding_box(
                ann[0]
            )
            all_filtered_lines.append(
                Line(
                    name= point.name,
                    line_type= point.line_type,
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
            ann = crop_image.adjust_filtered_annotations(annotations=[point])
            if(len(ann) == 0): continue
            bbox = convert_points_to_bounding_box(
                ann[0]
            )
            all_filtered_symbols.append(
                Symbol(
                    name= point.name,
                    label=point.label,
                    pointSrc=bbox.pointSrc,
                    pointDest=bbox.pointDest
                )
            )
        crop_image.save_symbol_annotated_result_in_npy_format(
            all_filtered_symbols,
            f"{upload_dir}\\annotations\\{s_index * num_columns + c_index}\\{s_index * num_columns + c_index}_symbols.npy"
        )
