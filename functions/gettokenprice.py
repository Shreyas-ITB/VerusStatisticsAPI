import requests
from decimal import Decimal
import time

def get_token_price(token_contract, retries=5, delay=1):
    url = f'https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses={token_contract}&vs_currencies=usd'
    for attempt in range(retries):
        try:
            response = requests.get(url).json()
            return Decimal(response[token_contract.lower()]['usd'])
        except KeyError:
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print(f"Request failed: {e}")
                raise