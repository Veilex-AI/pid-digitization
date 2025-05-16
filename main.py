from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db import connect_database
from src.routes import router as pid_router
from config import config
from src.utils import download_file_with_service_account

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_database()
    yield

download_file_with_service_account(config.model_file_id, config.service_account_key_path)

app = FastAPI(lifespan=lifespan)

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
    uvicorn.run(app, host="0.0.0.0", port=8000)