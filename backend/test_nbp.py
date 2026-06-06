from app.services.nbp_service import fetch_exchange_rates

rates = fetch_exchange_rates()

print(rates[:5])