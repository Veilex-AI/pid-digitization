from beanie import WriteRules
from bson import ObjectId
import datetime

from src.models.db import PipingDocument


async def create_pid_document(
    image_url: str,
    created_at: datetime.datetime
):
    pid_model = PipingDocument(
        image_name=image_url,
        created_at=created_at,
        updated_at=created_at
    )

    result = await pid_model.insert(link_rule=WriteRules.WRITE)
    return result


async def find_pid_document_by_id(id: str) -> PipingDocument:
    document = await PipingDocument.find_one(PipingDocument.id == ObjectId(id))
    return document