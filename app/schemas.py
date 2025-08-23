from pydantic import BaseModel, Field, HttpUrl


class URLRequest(BaseModel):
    url: HttpUrl


class URLResponse(BaseModel):
    short_url: str = Field(..., min_length=5, max_length=5)
