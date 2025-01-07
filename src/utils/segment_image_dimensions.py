from typing import List, Tuple
from PIL.ImageFile import ImageFile

def segment_image_dimensions(image: ImageFile, chunk_size=1080) -> List[List[Tuple[float, float, float, float]]]:
        """
            creates image segments for a given image with defined chuck size.
        """
        width, height = image.size

        x_chunks = (width + chunk_size - 1) // chunk_size
        y_chunks = (height + chunk_size - 1) // chunk_size

        x_size = [None for _ in range(x_chunks)]
        y_size = [None for _ in range(y_chunks)]

        chunks_2d_list = [[y for y in y_size] for _ in x_size]

        for i in range(x_chunks):
            for j in range(y_chunks):
                left = i * chunk_size
                upper = j * chunk_size
                right = min(left + chunk_size, width)
                lower = min(upper + chunk_size, height)

                chunks_2d_list[i][j] = (left, upper, right, lower)

        return [item for sublist in chunks_2d_list for item in sublist]