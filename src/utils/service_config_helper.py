from pydantic import BaseModel
from config import config


class ServiceConfigHelper(BaseModel):
    dataset_path: str
    image_dir_name: str
    annotation_dir_name: str

    def load_config(self):
        self.dataset_path = config.dataset_path 
        self.image_dir_name = config.image_dir_name
        self.annotation_dir_name = config.annotation_dir_name