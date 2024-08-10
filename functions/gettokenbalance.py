import requests
from decimal import Decimal
from var.vars import ETHERSCANAPI
from var.dict import arr_token_holders

def get_token_balance(token_contract, decimals):
    url = f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={token_contract}&address={arr_token_holders[0]}&tag=latest&apikey={ETHERSCANAPI}'
    response = requests.get(url).json()
    balance = Decimal(response['result']) / (10 ** decimals)
    return balance