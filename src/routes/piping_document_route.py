from fastapi import APIRouter


router = APIRouter(
    prefix='/api/pid',
    tags=['pid', 'piping and instrumentation diagram']
)

@router.get(
    '/',
)
async def test_piping_instrumentation_diagram():
    return "test string success"