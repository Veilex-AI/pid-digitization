import os
from typing import List
import numpy as np
from src.models.pid_data_point import PidDataPoint
from src.utils.convert_raw_data_to_symbols import convert_raw_data_to_symbols
from src.utils.convert_raw_data_to_lines import convert_raw_data_to_lines
from src.utils.convert_raw_data_to_bounding_box import convert_raw_data_to_bounding_box
from config import config

class DataConverterService:
    dataset_path: str
    image_dir_name: str
    annotation_dir_name: str

    def __init__(self):
        self.dataset_path = config.dataset_path
        self.image_dir_name = config.image_dir_name
        self.annotation_dir_name = config.annotation_dir_name

    def load_dataset(self):
        """
            loads the entire pid dataset and stores it in PidDataPoint model that is defined in src.models directory
        """
        pid_datapoints: List[PidDataPoint] = []
        annotation_path = '{}/{}'.format(self.dataset_path, self.annotation_dir_name)
        # list of directories with annotation labeled from 0 to N (number)
        annotation_dir = os.listdir(annotation_path)

        for dir_name in annotation_dir:
            datapoint = self.load_single_datapoint(dir_name)
            pid_datapoints.append(datapoint)

        return pid_datapoints
    
    def load_single_datapoint(self, path_to_load:str):
        """
            loads only a single datapoint from the entire dataset.
            used only when a number of datapoints are required with optimization
        """
        annotation_path = '{}/{}'.format(self.dataset_path, self.annotation_dir_name)
        # list of directories with annotation labeled from 0 to N (number)

        line_path = os.path.join(annotation_path, path_to_load, "{}_lines.npy".format(path_to_load))
        symbols_path = os.path.join(annotation_path, path_to_load, "{}_symbols.npy".format(path_to_load))
        words_path = os.path.join(annotation_path, path_to_load, "{}_words.npy".format(path_to_load))

        lines = np.load(line_path, allow_pickle=True)
        symbols = np.load(symbols_path, allow_pickle=True)
        # not required for current version/implementation
        words = np.load(words_path, allow_pickle=True)

        datapoint = PidDataPoint()
        datapoint.lines = convert_raw_data_to_lines(lines)
        datapoint.symbols = convert_raw_data_to_symbols(symbols)
        datapoint.words = convert_raw_data_to_bounding_box(words)

        # for the current dataset, all of the images are in jpg format
        datapoint.image_path = f"{self.dataset_path}/{self.image_dir_name}/{path_to_load}.jpg"
        
        return datapoint
