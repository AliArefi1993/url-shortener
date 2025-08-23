from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from app.rate_limit import limiter
from app.repository import create_or_get_short_url, get_short_url
from app.schemas import URLRequest, URLResponse

router = APIRouter()


@router.post("/shorten", response_model=URLResponse)
@limiter.limit("5/minute")
async def shorten_url(url_request: URLRequest, request: Request):
    """
    Shortens a given URL and returns a short code.
    If the URL was previously shortened, returns the existing short code.
    Validates the input URL and enforces a maximum length for the short code.
    Rate limited to 5 requests per minute per IP.
    """
    return await create_or_get_short_url(url_request)


@router.get("/{short}")
@limiter.limit("20/minute")
async def redirect_to_url(short: str, request: Request):
    """
    Redirects to the original URL for a given short code.
    Returns 404 if the short code is not found, or 400 if the code is invalid.
    Enforces exact length and character validation for the short code.
    Rate limited to 20 requests per minute per IP.
    """
    return RedirectResponse(await get_short_url(short))
