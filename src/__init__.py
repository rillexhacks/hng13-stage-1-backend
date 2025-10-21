from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.router import string_router


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Starting up...")
    await init_db()
    yield
    print("Shutting down...")

app = FastAPI(title="Async String Analyzer API", lifespan=life_span)
app.include_router(string_router)
