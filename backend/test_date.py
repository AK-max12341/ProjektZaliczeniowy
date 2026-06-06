from app.services.nbp_service import fetch_exchange_rates

rates = fetch_exchange_rates("2025-01-02")

print(rates[:5])