import requests
from decimal import Decimal
from var.vars import ETHERSCANAPI
from var.dict import arr_token_holders

def get_token_balance(token_contract, decimals):
    url = f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={token_contract}&address={arr_token_holders[0]}&tag=latest&apikey={ETHERSCANAPI}'
    response = requests.get(url).json()
    balance = Decimal(response['result']) / (10 ** decimals)
    return balance

def getnatisupply():
    url = "https://api.etherscan.io/api"
    params = {
        "module": "stats",
        "action": "tokensupply",
        "contractaddress": "0x4f14e88b5037f0ca24348fa707e4a7ee5318d9d5",
        "apikey": ETHERSCANAPI
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "1":
            return Decimal(int(data["result"]) / (10 ** 18))
        else:
            raise ValueError(f"Error: {data['message']}")
    else:
        raise Exception(f"HTTP Error: {response.status_code}")
