from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db import connect_database
from src.routes import router as pid_router
from config import config

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