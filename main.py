from config import config
from src.services.line_detection_service import LineDetectionService
from src.services.predict_symbols_service import PredictSymbolsService
from src.services.data_converter_service import DataConverterService


# get the datapoint
data_converter_service = DataConverterService()
datapoint = data_converter_service.load_single_datapoint(str(1))

# predict symbols of the datapoint
# predict_symbol_service = PredictSymbolsService(
#     image_path=datapoint.image_path
# )
# symbol_bounding_boxes = predict_symbol_service.predict_bounding_boxes()


# detect lines of the datapoint
# for current purposes we are only using the training data
# however, in real life usecase, we will have to detect the lines after predicting the symbols and words by ourselves.

line_detection_service = LineDetectionService(
    image_path=datapoint.image_path,
    bounding_boxes=[*datapoint.symbols, *datapoint.words]
)
line_segments = line_detection_service.detect_line_segments(True)

print(
    len(line_segments)
)