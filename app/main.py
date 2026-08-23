from fastapi import FastAPI
from app.routes import router
from app.database import engine, Base
from app.models import URL

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)


@app.get("/")
def read_root():
    return {"database": "connected"}

