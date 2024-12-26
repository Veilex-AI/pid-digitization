from pydantic import BaseModel

class Vertex(BaseModel):
    """
    Represents a vertext.
    """
    x: float
    y: float

    def get_dimensions(self):
        return (self.x, self.y)