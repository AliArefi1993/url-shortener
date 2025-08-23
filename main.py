import os
from contextlib import asynccontextmanager

from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.apis import router
from app.models import URL
from app.rate_limit import limiter

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/url_shortener")
MONGO_DB = os.getenv("MONGO_DB", "url_shortener")


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB]
    await init_beanie(database=db, document_models=[URL])
    yield


app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(router)
