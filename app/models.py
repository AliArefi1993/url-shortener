from beanie import Document
from pydantic import HttpUrl
from pymongo import IndexModel


class URL(Document):
    short: str
    url: HttpUrl

    class Settings:
        name = "urls"
        indexes = [
            IndexModel([("short", 1)], unique=True),
            IndexModel([("url", 1)], unique=True),
        ]
