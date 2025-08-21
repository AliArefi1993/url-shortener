import os

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient

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
    # At this point, event loop is closed, so use synchronous pymongo

    client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
    db = client[os.getenv("MONGO_TEST_DB", "url_shortener_test")]
    db.urls.delete_many({})  # synchronous cleanup
    client.close()
