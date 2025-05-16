import time
from typing import List, Tuple
from config import config
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from PIL import Image

from src.utils import pil_image_to_byte, azure_polygon_to_bbox

class PredictWordService:

    def __init__(self, image_path: str, azure_endpoint: str = "", azure_key: str = ""):
        self.azure_endpoint: str = config.azure_di_endpoint if azure_endpoint == "" else azure_endpoint 
        self.azure_key: str = config.azure_di_key if azure_key == "" else azure_key
        self.image_path = image_path
        self.client = self.create_client()
    
    def create_client(self) -> DocumentIntelligenceClient:
        """
            creates document inteligence client.
        """
        return DocumentIntelligenceClient(
            endpoint=self.azure_endpoint, credential=AzureKeyCredential(self.azure_key)
        )
    
    def get_image(self):
        """
            returns a PIL Image
        """
        return Image.open(self.image_path)

    def predicit_bounding_boxes(self) -> List[List[float]]:
        """
            identify the words in the PID by using azure document inteligence service. 
        """
        if(self.client is None):
            raise ValueError("Azure service client is not defined")
        
        # normal PIL image converted to a buffer.
        image_bytes = pil_image_to_byte(self.get_image(), self.image_path.split(".")[-1])
        
        start = time.time()
        document = self.client.begin_analyze_document(
            "prebuilt-layout", AnalyzeDocumentRequest(bytes_source=image_bytes)
        )

        result = document.result()

        words_bounding_box: List = []

        if(len(result['pages']) == 0):
            print("no detection")
            return
        
        for word in result['pages'][0]['words']:
            words_bounding_box.append(
                azure_polygon_to_bbox(word['polygon'])
            )

        print(f"time took to finish word prediction: { time.time() - start }")
    
        return words_bounding_box