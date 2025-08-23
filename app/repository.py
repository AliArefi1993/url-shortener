import logging
import secrets
import string

from fastapi import HTTPException
from pydantic import HttpUrl

from app.models import URL
from app.schemas import SHORT_URL_LEN, URLRequest, URLResponse

ALPHABET = string.ascii_letters + string.digits


async def generate_short() -> str:
    """Generate unique short code."""
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(SHORT_URL_LEN))
        if not await URL.find_one(URL.short == code):
            return code


async def create_or_get_short_url(request: URLRequest) -> URLResponse:
    """Create or return a shortened URL."""
    existing = await URL.find_one(URL.url == request.url)
    if existing:
        return URLResponse(short_url=existing.short)

    short = await generate_short()
    entry = URL(short=short, url=request.url)
    await entry.insert()
    return URLResponse(short_url=short)


async def get_short_url(short: str) -> HttpUrl:
    """
    Retrieve the original URL for a given short code.
    Raises HTTPException(404) if not found.
    """
    if len(short) != SHORT_URL_LEN:
        raise HTTPException(
            status_code=400,
            detail=f"Short URL must be exactly {SHORT_URL_LEN} characters.",
        )
    url_doc = await URL.find_one(URL.short == short)
    if not url_doc:
        logging.error(f"Short URL not found: {short}")
        raise HTTPException(status_code=404, detail="Short URL not found.")
    return url_doc.url
