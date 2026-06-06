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

@router.get("/months/{year}")
def get_months(year: int):

    db = SessionLocal()

    months = (
        db.query(extract("month", CurrencyRate.date))
        .filter(extract("year", CurrencyRate.date) == year)
        .distinct()
        .all()
    )

    return sorted([int(month[0]) for month in months])

@router.get("/quarters/{year}")
def get_quarters(year: int):

    db = SessionLocal()

    months = (
        db.query(extract("month", CurrencyRate.date))
        .filter(extract("year", CurrencyRate.date) == year)
        .distinct()
        .all()
    )

    quarters = sorted(
        list(
            set(
                ((int(month[0]) - 1) // 3) + 1
                for month in months
            )
        )
    )

    return quarters

@router.get("/days/{year}/{month}")
def get_days(year: int, month: int):

    db = SessionLocal()

    days = (
        db.query(extract("day", CurrencyRate.date))
        .filter(extract("year", CurrencyRate.date) == year)
        .filter(extract("month", CurrencyRate.date) == month)
        .distinct()
        .all()
    )

    return sorted([int(day[0]) for day in days])

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