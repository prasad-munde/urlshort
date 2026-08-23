from pydantic import BaseModel, HttpUrl
from datetime import datetime

class URLCreate(BaseModel):
    mainurl: HttpUrl
    expires_at: datetime | None = None
class URLrepsonse(BaseModel):
    original_url: HttpUrl
    short_code:str
    expires_at:datetime | None=None