from beanie import init_beanie
import motor

from src.models.db import PipingDocument
from config import config

async def connect_database():
    global client
    client = motor.motor_asyncio.AsyncIOMotorClient(config.mongo_uri)
    await init_beanie(database=client[config.db_name], document_models=[PipingDocument])