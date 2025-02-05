import io
from PIL import ImageFile

def pil_image_to_byte(image: ImageFile, format: str = "PNG") -> bytes:
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=format)
    return img_byte_arr.getvalue()