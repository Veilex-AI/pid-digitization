from pydantic_settings import BaseSettings 
import os
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    """
        param model_path: the path of YOLO model. used for symbol detection.
        param upload_path: the path where additional data can be uploaded.
        param dataset_path: the path of the original dataset.
        param image_dir_name: dir name where the images are stored in the dataset_path
        param annotation_dir_name: dir name where the annoations (of images) are stored in the dataset_path.
    """
    model_path: str
    upload_path: str
    dataset_path: str
    image_dir_name: str
    annotation_dir_name: str

config = Config(
    model_path = os.getenv("MODEL_PATH"),
    upload_path = os.getenv("UPLOAD_PATH"),
    dataset_path = os.getenv("DATASET_PATH"),
    image_dir_name = os.getenv("IMAGE_DIR_NAME"),
    annotation_dir_name = os.getenv("ANNOTATION_DIR_NAME")
)