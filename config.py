import os
from pydantic_settings import BaseSettings, SettingsConfigDict 

class Settings(BaseSettings):
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
        param model_file_id: file id that references the file in the cloud
        param service_account_key_path: service account key for permission to download the file
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
    model_file_id: str = ""
    service_account_key_path: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        populate_by_name=True
    )

config = Settings()