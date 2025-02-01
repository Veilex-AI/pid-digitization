import asyncio
from datetime import datetime
import io
from typing import List
from uuid import uuid4
from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image
from config import config
from src.models.vertex import Vertex
from src.models.symbol import Symbol
from src.services.predict_symbols_service import PredictSymbolsService
from src.repository import pid_repository
import threading

# key-value pair document.id: thread_id
thread_pid_jobs = []

router = APIRouter(
    prefix='/api/pid',
    tags=['pid']
)

@router.get(
    "/"
)
async def test():
    return "hello world"

@router.post(
    '/upload'
)
async def upload_pid(
    file: UploadFile = File(..., description="PID document")
):
    """
        uploads a piping and instrumentation document with timestamp
    """
    # verify extension of the file
    if file.filename is not None or file.filename != '':
       if (file.filename.split('.')[1] in ['png', 'jpg']) is False:
           raise HTTPException(status_code=400, detail="Bad request") 
    
    file_ext = file.filename.split('.')[1]
    new_file_name = f"{uuid4()}.{file_ext}"

    # upload the file 
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    image.save(f"{config.pid_upload_path}/{new_file_name}")

    # save it to the databse
    image_name = f"{new_file_name}"
    created_at=datetime.now()

    pid = await pid_repository.create_pid_document(image_name, created_at)
       
    return { "id": str(pid.id) }

@router.post(
    '/digitalize/{id}',
)
async def digitalize_pid_graph(
    id: str
):
    if((await pid_repository.find_pid_document_by_id(id)) is None):
        raise HTTPException(status_code=404, detail="Not Found")
    
    if(id in thread_pid_jobs):
        print(f"a thread with pid {id} is already in progress")
        raise HTTPException(status_code=409, detail="A similar thread with the associated id is already running.")
    
    asyncio.create_task(between_callback(id))
    
    # task = asyncio.to_thread(digitize_pid_document(id))

    # thread_pid_jobs.append(task)

    return None

@router.get(
    "/graph-xml"
)
async def get_graph_based_xml(
    id: str
):
    return "this route will donwload an xml file, having a digitzlied PID document."



# PRIVATE FUNCTIONS
async def between_callback(args):
    """
        running thread based pid processing.
    """

    thread_pid_jobs.append(args)

    asyncio.to_thread(await digitize_pid_document(args))
    


    # thread_pid_jobs.append(args)

    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)

    # loop.run_until_complete(digitize_pid_document(args))
    # loop.close()

    # thread_pid_jobs.remove(args)



async def digitize_pid_document(id: str):
    """
        used by a thread to digitize pid documents.
    """

    pid_document = await pid_repository.find_pid_document_by_id(id)

    if(pid_document is None):
        # should use a logger here btw. a better way to program.
        print(f"pid document with associated id {pid_document.id} Not found")

    image_path = f"{config.pid_upload_path}/{pid_document.image_name}"

    # get all symbols from the document.

    model_path="./yolo-model-pid.pt"
    predict_symbol_service = PredictSymbolsService(
        image_path=image_path,
        model_path=model_path
    )
    bboxes_with_labels = predict_symbol_service.predict_bounding_boxes()

    symbols: List[Symbol] = []
    for bbl in bboxes_with_labels:
        bbox = bbl[0]
        label = bbl[1]

        [x, y, _x, _y] = bbox
        symbols.append(
            Symbol(
                label=label,
                name="",
                pointSrc=Vertex(x=x, y=y),
                pointDest=Vertex(x=_x, y=_y)
            )
        )

    pid_document.symbols = symbols

    await pid_document.save()

    thread_pid_jobs.remove(id)






def get_symbols_from_pid():
    pass

def get_lines_from_pid():
    pass

def create_graph_result_from_pid():
    pass