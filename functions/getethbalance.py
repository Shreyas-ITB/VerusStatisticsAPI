import requests
from decimal import Decimal
from var.vars import ETHERSCANAPI

def get_eth_balance(address):
    url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCANAPI}'
    response = requests.get(url).json()
    return Decimal(response['result']) / (10 ** 18)