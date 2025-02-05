from contextlib import asynccontextmanager
from fastapi import FastAPI
from matplotlib.image import BboxImage
from src.db.mongo import connect_database
from src.models.symbol import Symbol
from src.models.line import Line
from src.services.crop_image_service import CropImageService
from src.models.bounding_box import BoundingBox
from src.models.vertex import Vertex
from src.services.image_display_serivce import ImageDisplayService
from src.services.line_detection_service import LineDetectionService
from src.services.predict_symbols_service import PredictSymbolsService
from src.services.data_converter_service import DataConverterService
from src.utils.convert_points_to_bounding_box import convert_points_to_bounding_box
from fastapi.middleware.cors import CORSMiddleware
from src.routes.piping_document_route import router as pid_router
from config import config


"""
    TODO: before initializing the database and fast api server, ensure to load all the files first that are required to run this application.
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_database()
    yield


app = FastAPI(lifespan=lifespan)


# only used for development mode
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(pid_router, prefix="")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)