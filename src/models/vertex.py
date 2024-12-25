from pydantic import BaseModel

class Vertex(BaseModel):
    """
    Represents a vertext.
    """
    x: float
    y: float