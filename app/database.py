from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = "postgresql://postgres:prasad@localhost:5432/url_shortener"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False,
                            autoflush= False,
                            bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()