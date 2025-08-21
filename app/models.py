from beanie import Document
from pydantic import HttpUrl


class URL(Document):
    short: str
    url: HttpUrl

    class Settings:
        name = "urls"
        indexes = [[("short", 1), ("url", 1)]]
