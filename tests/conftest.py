import os

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from redis import Redis  # type: ignore

from main import app


@pytest.fixture
def client():
    """Provide a TestClient. DB is initialized in app lifespan."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def check_test_db():
    test_db = os.getenv("MONGO_TEST_DB", "url_shortener_test")
    current_db = os.getenv("MONGO_DB", "url_shortener")
    print(f"Current DB: {current_db}, Test DB: {test_db}")
    if current_db != test_db:
        pytest.skip("Skipping tests because not running on test DB")


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    """Ensure test DB is cleaned after all tests."""
    yield

    client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
    db = client[os.getenv("MONGO_TEST_DB", "url_shortener_test")]
    db.urls.delete_many({})
    client.close()


@pytest.fixture(autouse=True)
def clear_redis_rate_limit():
    r = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
    yield
    for key in r.scan_iter("LIMITS*"):
        r.delete(key)
