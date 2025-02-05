from pydantic_settings import BaseSettings 
import os
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    """
        param model_path: the path of YOLO model. used for symbol detection.
        param upload_path: the path where additional data can be uploaded.
        param dataset_path: the path of the original dataset.
        param image_dir_name: dir name where the images are stored in the dataset_path.
        param annotation_dir_name: dir name where the annoations (of images) are stored in the dataset_path.
        param monogo_uri: the uri of mongo db to connect to mongo no sql database.
        param db_name: the name of the database associated with the mongo server.
        param pid_upload_path: the dir where all pid documents will be uploaded via the API.
        param azure_di_endpoint: url endpoint for azure document inteligence service
        param azure_di_key: associaated key to access azure document inteliggence service
    """
    model_path: str
    upload_path: str
    dataset_path: str
    image_dir_name: str
    annotation_dir_name: str
    mongo_uri: str
    db_name: str
    pid_upload_path: str
    azure_di_endpoint: str
    azure_di_key: str

config = Config(
    model_path = os.getenv("MODEL_PATH"),
    upload_path = os.getenv("UPLOAD_PATH"),
    dataset_path = os.getenv("DATASET_PATH"),
    image_dir_name = os.getenv("IMAGE_DIR_NAME"),
    annotation_dir_name = os.getenv("ANNOTATION_DIR_NAME"),
    mongo_uri = os.getenv("MONGO_URI"),
    db_name = os.getenv("DB_NAME"),
    pid_upload_path = os.getenv("PID_UPLOAD_PATH"),
    azure_di_endpoint = os.getenv("AZURE_DI_ENDPONT"),
    azure_di_key = os.getenv("AZURE_DI_KEY")
)