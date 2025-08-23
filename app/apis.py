from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.repository import create_or_get_short_url, get_short_url
from app.schemas import URLRequest, URLResponse

router = APIRouter()


@router.post("/shorten", response_model=URLResponse)
async def shorten_url(request: URLRequest):
    """Create or return a shortened URL."""
    return await create_or_get_short_url(request)


@router.get("/{short}")
async def redirect_to_url(short: str):
    return RedirectResponse(await get_short_url(short))
