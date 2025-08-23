from pydantic import BaseModel, Field, HttpUrl

SHORT_URL_LEN = 5


class URLRequest(BaseModel):
    url: HttpUrl


class URLResponse(BaseModel):
    short_url: str = Field(..., min_length=SHORT_URL_LEN, max_length=SHORT_URL_LEN)
