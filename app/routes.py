from fastapi import APIRouter, Depends, HTTPException,Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime,timezone
from app.database import get_db
from app.models import URL
from app.schemas import URLCreate,URLrepsonse
from app.utils import generate_short_code
from app.redis import redis_client
from app.rate_limiter import check_rate_limit
import logging

router = APIRouter()

logger = logging.getLogger(__name__)



@router.post("/shorten", tags=["URL"],response_model=URLrepsonse)
async def shorten_url(data: URLCreate, db: Session = Depends(get_db)):
    logger.info("Creating short URL for %s", data.mainurl)
    while True:
        short_code = generate_short_code()
        existing_url=(db.query(URL).filter(URL.short_code==short_code).first())
        if not existing_url:
            break
    new_url = URL(
        original_url=str(data.mainurl),
        short_code=short_code,
        expires_at=data.expires_at
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    logger.info("Created short URL with code %s", new_url.short_code)
    return new_url

@router.get("/rate-test", tags=["Rate Limit"])
async def rate_test():
    return {"message": "Request allowed"}

@router.get("/redis-test", tags=["Redis"])
async def redis_test():

    redis_client.set("test", "hello")

    value = redis_client.get("test")

    return {"value": value}

@router.get("/{short_code}", tags=["URL"],dependencies=[Depends(check_rate_limit)])
async def redirect_url(short_code: str, db: Session = Depends(get_db)):

    original_url = redis_client.get(short_code)
    if original_url:
        logger.info("Redis cache hit for %s", short_code)
        return RedirectResponse(url=original_url)
    logger.info("Redis cache miss for %s", short_code)

    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        logger.warning("Short code %s not found", short_code)
        raise HTTPException(status_code=404, detail="URL not found")
    
    if url.expires_at:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        if now>=url.expires_at:
            logger.info("Short code %s has expired", short_code)
            raise HTTPException(status_code=410,detail="Url has Expired")
        
    if url.expires_at:
        ttl = int((url.expires_at - datetime.now(timezone.utc).replace(tzinfo=None)).total_seconds())
        if ttl>0:
            redis_client.set(short_code,url.original_url,ex=ttl)
        else:
            redis_client.set(short_code,url.original_url,ex=3600)

    return RedirectResponse(url=url.original_url)   


