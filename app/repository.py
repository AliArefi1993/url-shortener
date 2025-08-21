import secrets
import string

from app.models import URL

ALPHABET = string.ascii_letters + string.digits
MAX_LENGTH = 5


async def generate_short() -> str:
    """Generate unique short code."""
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(MAX_LENGTH))
        if not await URL.find_one(URL.short == code):
            return code
