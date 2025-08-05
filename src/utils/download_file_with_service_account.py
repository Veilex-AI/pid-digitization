from google.oauth2 import service_account
import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from config import config

model_file_name = config.model_path

def download_file_with_service_account(file_id: int, service_account_file: str):
    if os.path.exists(f'./{model_file_name}'):
        return

    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    request = service.files().get_media(fileId=file_id)

    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%")
    
    with open(f"./{model_file_name}", 'wb') as f:
        f.write(file.getvalue())

    return f"./{model_file_name}"