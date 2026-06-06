import requests


def fetch_exchange_rates(selected_date=None):

    if selected_date:
        url = (
            f"https://api.nbp.pl/api/exchangerates/tables/A/"
            f"{selected_date}?format=json"
        )
    else:
        url = "https://api.nbp.pl/api/exchangerates/tables/A?format=json"

    response = requests.get(url)

    response.raise_for_status()

    data = response.json()

    return data[0]["rates"]