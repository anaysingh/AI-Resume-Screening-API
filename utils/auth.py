# utils/auth.py

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

# -------------------- API KEY VALUE --------------------
API_KEY = "supersecretkey123"   # change it if you want

# -------------------- SECURITY HEADER --------------------
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

# -------------------- VALIDATION FUNCTION --------------------
async def validate_api_key(api_key: str = Security(api_key_header)):
    """
    Validates the x-api-key header using FastAPI's Security system.
    This works with Swagger's Authorize button.
    """
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: Invalid or missing API Key."
        )
