from app.core.config import settings
from fastapi import FastAPI

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.app_debug,
)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
