from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.schemas import URLRequest, URLResponse
from app.models import URL
from app.repository import generate_short

router = APIRouter()


@router.post("/shorten", response_model=URLResponse)
async def shorten_url(request: URLRequest):
    """Create or return a shortened URL."""
    existing = await URL.find_one(URL.url == request.url)
    if existing:
        return {"short_url": existing.short}

    short = await generate_short()
    entry = URL(short=short, url=request.url)
    await entry.insert()
    return {"short_url": short}


@router.get("/{short}")
async def redirect_to_url(short: str, request: Request):
    url_doc = await URL.find_one(URL.short == short)
    if not url_doc:
        raise HTTPException(status_code=404, detail="Short URL not found.")
    return RedirectResponse(str(url_doc.url))
