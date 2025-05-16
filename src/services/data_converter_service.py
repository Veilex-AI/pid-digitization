import os
from typing import List
import numpy as np

from src.enums import AnnotationType
from src.models import PidDataPoint
from src.utils import convert_raw_data_to_symbols, convert_raw_data_to_lines, convert_raw_data_to_bounding_box
from config import config

class DataConverterService:
    dataset_path: str
    image_dir_name: str
    annotation_dir_name: str

    def __init__(self):
        self.dataset_path = config.dataset_path
        self.image_dir_name = config.image_dir_name
        self.annotation_dir_name = config.annotation_dir_name

    def load_dataset(self) -> List[PidDataPoint]:
        """
            loads the pid dataset
        """
        pid_datapoints: List[PidDataPoint] = []
        annotation_path = '{}/{}'.format(self.dataset_path, self.annotation_dir_name)
        # list of directories with annotation labeled from 0 to N (number)
        annotation_dir = os.listdir(annotation_path)

        for dir_name in annotation_dir:
            datapoint = self.load_single_datapoint(dir_name)
            pid_datapoints.append(datapoint)

        return pid_datapoints
    
    def load_single_datapoint(self, path_to_load:str) -> PidDataPoint:
        """
            loads a single datapoint from the entire dataset.
        """
        annotation_path = '{}/{}'.format(self.dataset_path, self.annotation_dir_name)
        # list of directories with annotation labeled from 0 to N (number)

        line_path = os.path.join(annotation_path, path_to_load, f"{path_to_load}_{AnnotationType.LINES.value}.npy")
        symbols_path = os.path.join(annotation_path, path_to_load, f"{path_to_load}_{AnnotationType.SYMBOLS.value}.npy")
        words_path = os.path.join(annotation_path, path_to_load, f"{path_to_load}_{AnnotationType.WORDS.value}.npy")

        lines = np.load(line_path, allow_pickle=True)
        symbols = np.load(symbols_path, allow_pickle=True)
        words = np.load(words_path, allow_pickle=True)

        datapoint = PidDataPoint()
        datapoint.lines = convert_raw_data_to_lines(lines)
        datapoint.symbols = convert_raw_data_to_symbols(symbols)
        datapoint.words = convert_raw_data_to_bounding_box(words)

        # for the current dataset, all of the images are in jpg format
        datapoint.image_path = f"{self.dataset_path}/{self.image_dir_name}/{path_to_load}.jpg"
        
        return datapoint
