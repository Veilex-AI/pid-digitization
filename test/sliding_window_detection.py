import math

from src.services import DataConverterService, PredictSymbolsService

def get_all_datapoints(dp_index = None):
    data_converter_service = DataConverterService()
    if dp_index is not None:
        datapoints = data_converter_service.load_single_datapoint(str(dp_index))
    else:
        datapoints = data_converter_service.load_dataset()

    return datapoints

def get_class_sizes():
    datapoints = get_all_datapoints()

    class_size = {}

    for d in datapoints:
        predict_service = PredictSymbolsService(
            image_path=d.image_path
        )
        
        bboxes = predict_service.predict_bounding_boxes()

        for box in bboxes:
            class_type = box[1]
            if class_type not in class_size:
                [x1, y1, x2, y2] = box[0]
                # get width and height of the bounding box
                print(abs(x2 - x1),  abs(y2 - y1))
                class_size[class_type] = abs(x2 - x1) * abs(y2 - y1)

        if (len(class_size.keys()) >= 32):
            break

        print(
            class_size
        )

    return class_size

def remove_decimal_values(class_sizes: dict):
    for class_type in class_sizes.keys():
        area = class_sizes[class_type]
        class_sizes[class_type] = math.floor(area)

    return class_sizes

class_sizes = {'21': 1985, '2': 5415, '18': 6969, '26': 17849, '8': 7037, '20': 6110, '25': 6532, '32': 16411, '28': 17179, '7': 6771, '9': 6689, '12': 5510, '22': 5795, '24': 2808, '11': 6129, '23': 8645, '29': 17181, '4': 6132, '31': 16001, '5': 4808, '15': 3737, '17': 5721, '19': 6769, '30': 11940, '16': 3564, '13': 6558, '1': 4575, '6': 3126, '10': 8179, '27': 18761, '14': 13607, '3': 6903}



sizes = get_class_sizes()
print(remove_decimal_values(sizes))