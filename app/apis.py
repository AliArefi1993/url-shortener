from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.rate_limit import limiter
from app.repository import create_or_get_short_url, get_short_url
from app.schemas import URLRequest, URLResponse

router = APIRouter()


@router.post("/shorten", response_model=URLResponse)
@limiter.limit("5/minute")
async def shorten_url(url_request: URLRequest, request: Request):
    """Create or return a shortened URL."""
    return await create_or_get_short_url(url_request)


@router.get("/{short}")
@limiter.limit("20/minute")
async def redirect_to_url(short: str, request: Request):
    return RedirectResponse(await get_short_url(short))
