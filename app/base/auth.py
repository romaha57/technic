from fastapi import Header, HTTPException

from app.config import settings


async def verify_api_key(api_key: str = Header(None, alias="X-API-Key")):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    return api_key
