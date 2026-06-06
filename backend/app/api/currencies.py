from datetime import date

from fastapi import APIRouter
from sqlalchemy import extract

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


@router.get(
    "/currencies/{selected_date}",
    response_model=list[CurrencyRateResponse]
)
def get_currencies_by_date(selected_date: date):

    db = SessionLocal()

    currencies = (
        db.query(CurrencyRate)
        .filter(CurrencyRate.date == selected_date)
        .all()
    )

    return currencies


@router.get("/years")
def get_years():

    db = SessionLocal()

    years = (
        db.query(extract("year", CurrencyRate.date))
        .distinct()
        .all()
    )

    return [int(year[0]) for year in years]


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


@router.post("/currencies/fetch/{selected_date}")
def fetch_currencies_by_date(selected_date: date):

    db = SessionLocal()

    rates = fetch_exchange_rates(str(selected_date))

    for rate in rates:
        currency_rate = CurrencyRate(
            currency=rate["currency"],
            code=rate["code"],
            rate=rate["mid"],
            date=selected_date
        )

        db.add(currency_rate)

    db.commit()

    return {
        "message": f"{len(rates)} exchange rates saved for {selected_date}"
    }