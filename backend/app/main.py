from fastapi import FastAPI
from app.api.currencies import router as currencies_router

app = FastAPI()

app.include_router(currencies_router)

@app.get("/")
def root():
    return {
        "message": "Hello Currency API"
    }