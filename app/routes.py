from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime,timezone
from app.database import get_db
from app.models import URL
from app.schemas import URLCreate,URLrepsonse
from app.utils import generate_short_code

router = APIRouter()

url_store = {}


@router.post("/shorten", tags=["URL"],response_model=URLrepsonse)
async def shorten_url(data: URLCreate, db: Session = Depends(get_db)):
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

    return new_url


@router.get("/{short_code}", tags=["URL"])
async def redirect_url(short_code: str, db: Session = Depends(get_db)):

    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    if url.expires_at:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        if now>=url.expires_at:
            raise HTTPException(status_code=410,detail="Url has Expired")

    return RedirectResponse(url=url.original_url)   