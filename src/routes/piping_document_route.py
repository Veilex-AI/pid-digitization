import asyncio
from datetime import datetime
import io
from typing import List
from uuid import uuid4
from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image

from src.models import BoundingBox, Vertex, Symbol
from src.services import PredictWordService, GraphConstructionService, LineDetectionService, PredictSymbolsService
from src.repository import pid_repository
from src.utils import convert_points_to_bounding_box
from config import config

# key-value pair document.id: thread_id
thread_pid_jobs = []

router = APIRouter(
    prefix='/api/pid',
    tags=['pid']
)

@router.get(
    "/"
)
async def get_pid(
    id: str
):
    result = await pid_repository.find_pid_document_by_id(id)
    if(result is None):
        raise HTTPException(status_code=404, detail="The document is not found")
    return result


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
    
    # asyncio.create_task(digitize_pid_document(id))

    await digitize_pid_document(id)
    
    return None


# PRIVATE FUNCTIONS
async def between_callback(args):
    """
        running thread based pid processing.
    """
    thread_pid_jobs.append(args)
    asyncio.to_thread(await digitize_pid_document(args))


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

    w,h = predict_symbol_service.get_image().size

    prediction_results = predict_symbol_service.predict_bounding_boxes(shifting=(True if w > 1088 and h > 1088 else False))

    symbols: List[Symbol] = []
    for index, pr in enumerate(prediction_results):
        bbox = pr[0]
        label = pr[1]

        [x, y, _x, _y] = bbox
        symbols.append(
            Symbol(
                label=label,
                name=f"s-{index}",
                pointSrc=Vertex(x=x, y=y),
                pointDest=Vertex(x=_x, y=_y)
            )
        )

    pid_document.symbols = symbols

    # get word bounding box from the document.
    predict_word_service = PredictWordService(
        image_path=image_path
    )
    word_prediction = predict_word_service.predicit_bounding_boxes()

    words_bbox: List[BoundingBox] = []
    for index, w_bbox in enumerate(word_prediction):
        [x, y, _x, _y] = w_bbox
        words_bbox.append(
            BoundingBox(
                name=f"w-{index}",
                pointSrc=Vertex(x=x, y=y),
                pointDest=Vertex(x=_x, y=_y)
            )
        )
    
    pid_document.words = words_bbox

    await pid_document.save()


    # get all lines from the document
    line_detection_service = LineDetectionService(
        image_path=image_path,
        bounding_boxes=[*symbols, *words_bbox]
    )

    line_segments = [
        convert_points_to_bounding_box(l) for l in line_detection_service.merge_lines(
            line_segments = line_detection_service.extend_lines(
                line_detection_service.detect_line_segments(enable_thining=True)       
            )
        )
    ]

    for index, l in enumerate(line_segments):
        l.name = f"l-{str(index)}"

    pid_document.lines = line_segments

    await pid_document.save()

    # construct a graph based on symbols and lines.

    graph_service = GraphConstructionService(symbols=symbols, line_segments=line_segments)
    graph_service.initialize_graph()
    graph_service.define_graph_edges()

    graph_service.reduce_line_cycles()
    graph_service.remove_connected_line_nodes()

    # optimize this part.
    for _ in range(100):
        graph_service.remove_zero_or_single_connection_line_nodes()

    # not needed anymore
    # the reason for using this function was to remove redundent line nodes but now it has handled by merging the same slope based lines which is taken care via the cartesian based operation that comes before any graph operations.
    # graph_service.prune_multiple_path_nodes(
    #     graph_service.find_valid_paths()
    # )

    graphml_result = graph_service.generate_graphml()

    pid_document.graphml_buffer = graphml_result
    pid_document.digitalized = True

    await pid_document.save()