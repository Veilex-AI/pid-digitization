from pydantic_settings import BaseSettings 
import os
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
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