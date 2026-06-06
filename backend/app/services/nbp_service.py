import requests


def fetch_exchange_rates():
    url = "https://api.nbp.pl/api/exchangerates/tables/A?format=json"

    response = requests.get(url)

    response.raise_for_status()

    data = response.json()

    return data[0]["rates"]