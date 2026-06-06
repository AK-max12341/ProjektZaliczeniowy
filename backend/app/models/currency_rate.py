from sqlalchemy import Column, Integer, String, Float, Date

from app.database.base import Base


class CurrencyRate(Base):
    __tablename__ = "currency_rates"

    id = Column(Integer, primary_key=True, index=True)
    currency = Column(String, nullable=False)
    code = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    date = Column(Date, nullable=False)