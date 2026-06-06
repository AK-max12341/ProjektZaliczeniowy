from fastapi import APIRouter

router = APIRouter()

@router.get("/currencies")
def get_currencies():
    return [
        "USD",
        "EUR",
        "GBP"
    ]