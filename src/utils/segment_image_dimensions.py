from typing import List, Tuple
from PIL.ImageFile import ImageFile

def segment_image_dimensions(image: ImageFile, chunk_size=1080, shift = 0) -> List[List[Tuple[float, float, float, float]]]:
        """
            creates image segments for a given image with defined chuck size.
        """
        width, height = image.size

        x_chunks = ((width - shift) + chunk_size - 1) // chunk_size
        y_chunks = ((height - shift) + chunk_size - 1) // chunk_size

        x_size = [None for _ in range(x_chunks)]
        y_size = [None for _ in range(y_chunks)]

        chunks_2d_list = [[y for y in y_size] for _ in x_size]

        for i in range(x_chunks):
            for j in range(y_chunks):
                left = i * chunk_size + shift
                upper = j * chunk_size + shift
                right = min(left + chunk_size + shift, width)
                lower = min(upper + chunk_size + shift, height)

                chunks_2d_list[i][j] = (left, upper, right, lower)

        return [item for sublist in chunks_2d_list for item in sublist]