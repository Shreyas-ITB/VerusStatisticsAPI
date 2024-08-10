import requests
from web3 import Web3
from var.dict import arr_token_holders
from var.vars import INFURAURL, ETHERSCANAPI

def get_dai_value():
    web3 = Web3(Web3.HTTPProvider(INFURAURL))
    function_signature = web3.keccak(text='pie(address)').hex()[:10]
    encoded_query_address = web3.to_hex(web3.to_bytes(hexstr=arr_token_holders[0]))[2:].zfill(64)
    data = function_signature + encoded_query_address
    url = f'https://api.etherscan.io/api?module=proxy&action=eth_call&to={arr_token_holders[1]}&data={data}&apikey={ETHERSCANAPI}'
    response = requests.get(url).json()
    wei_value = int(response['result'], 16)
    ether_value = web3.from_wei(wei_value, 'ether')
    return ether_value