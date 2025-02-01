from beanie import init_beanie
import motor
from config import config
from src.models.db.piping_document import PipingDocument

async def connect_database():
    global client
    client = motor.motor_asyncio.AsyncIOMotorClient(config.mongo_uri)
    await init_beanie(database=client[config.db_name], document_models=[PipingDocument])