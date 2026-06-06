from app.database.base import Base
from app.database.connection import engine

from app.models.currency_rate import CurrencyRate

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")