from datetime import date

from fastapi import APIRouter

from app.database.connection import SessionLocal
from app.models.currency_rate import CurrencyRate
from app.schemas.currency_rate import CurrencyRateResponse
from app.services.nbp_service import fetch_exchange_rates

router = APIRouter()


@router.get("/currencies", response_model=list[CurrencyRateResponse])
def get_currencies():

    db = SessionLocal()

    currencies = db.query(CurrencyRate).all()

    return currencies


@router.post("/currencies/fetch")
def fetch_currencies():

    db = SessionLocal()

    rates = fetch_exchange_rates()

    today = date.today()

    for rate in rates:
        currency_rate = CurrencyRate(
            currency=rate["currency"],
            code=rate["code"],
            rate=rate["mid"],
            date=today
        )

        db.add(currency_rate)

    db.commit()

    return {
        "message": f"{len(rates)} exchange rates saved"
    }