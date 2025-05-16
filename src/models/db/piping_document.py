from beanie import Document
from datetime import datetime
from typing import List, Optional

from src.models.bounding_box import BoundingBox
from src.models.line import Line
from src.models.symbol import Symbol


class PipingDocument(Document):
    """
    Represents the piping and instrumentaiton diagram information.
    """
    name: Optional[str] = None
    image_name: str
    symbols: List[Symbol] = []
    lines: List[Line] = []
    words: List[BoundingBox] = []
    digitalized: bool = False
    created_at: datetime
    updated_at: datetime
    graphml_buffer: str = ""