from sqlalchemy import Column, Integer, String,DateTime,func
from app.database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, nullable=False, index=True)
    expires_at = Column(DateTime,nullable=True)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)