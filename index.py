import re
import requests, os
from dotenv import load_dotenv, find_dotenv
import json
from fastapi import FastAPI, HTTPException
import uvicorn
import time
import numpy as np
from web3 import Web3
import yfinance as yf
from decimal import Decimal

app = FastAPI()
load_dotenv(find_dotenv())
RPCURL = os.environ.get("RPCURL")
PORT = os.environ.get("APIPORT")
ETHERSCANAPI = os.environ.get("ETHERSCANAPIKEY")
INFURAURL = os.environ.get("INFURAURL")
# RPCUSER=
# RPCPASS=

# Placeholder data
latestblock = []
reservecurrencies = []
mempool_res = []
rawtransaction = []
decodedrawtransaction = []
mempool_count = 0
res = []

# arr_currencies = [
#     {"currencyid": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV", "ticker": "VRSC"},
#     {"currencyid": "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM", "ticker": "DAI.vETH"},
#     {"currencyid": "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4", "ticker": "MKR.vETH"},
#     {"currencyid": "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X", "ticker": "vETH"},
#     {"currencyid": "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE", "ticker": "EURC.vETH"},
#     {"currencyid": "i9oCSqKALwJtcv49xUKS2U2i79h1kX6NEY", "ticker": "USDT.vETH"},
#     {"currencyid": "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd", "ticker": "USDC.vETH"},
#     {"currencyid": "iHax5qYQGbcMGqJKKrPorpzUBX2oFFXGnY", "ticker": "PURE.vETH"},
#     {"currencyid": "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU", "ticker": "tBTC.vETH"},
#     {"currencyid": "iExBJfZYK7KREDpuhj6PzZBzqMAKaFg7d2", "ticker": "vARRR" },
#     {"currencyid": "i3f7tSctFkiPpiedY8QR5Tep9p4qDVebDx", "ticker": "Bridge.vETH" },
#     {"currencyid": "i4Xr5TAMrDTD99H69EemhjDxJ4ktNskUtc", "ticker": "Switch" },
#     {"currencyid": "i9kVWKU2VwARALpbXn4RS9zvrhvNRaUibb", "ticker": "Kaiju"}
# ]

arr_currencies = [
    {"currencyid": "iQ3NQaPQRtJ4KamYkWEJfuiggkCbnmFW1z", "ticker": "VerusNFT"},
    {"currencyid": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV", "ticker": "VRSC"},
    {"currencyid": "i3f7tSctFkiPpiedY8QR5Tep9p4qDVebDx", "ticker": "Bridge.vETH"},
    {"currencyid": "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X", "ticker": "vETH"},
    {"currencyid": "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM", "ticker": "DAI.vETH"},
    {"currencyid": "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4", "ticker": "MKR.vETH"},
    {"currencyid": "iEnQEjjozf1HZkqFT9U4NKnzz1iGZ7LbJ4", "ticker": "TRAC.vETH"},
    {"currencyid": "iJczmut8fHgRvVxaNfEPm7SkgJLDFtPcrK", "ticker": "vLINK.vETH"},
    {"currencyid": "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd", "ticker": "vUSDC.vETH"},
    {"currencyid": "i9oCSqKALwJtcv49xUKS2U2i79h1kX6NEY", "ticker": "vUSDT.vETH"},
    {"currencyid": "iNtUUdjsqV34snGZJerAvPLaojo6tV9sfd", "ticker": "vMars4"},
    {"currencyid": "iS3NjE3XRYWoHRoovpLhFnbDraCq7NFStf", "ticker": "vwBTC.vETH"},
    {"currencyid": "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU", "ticker": "tBTC.vETH"},
    {"currencyid": "i4YYnZvzhaQPJvQsVMsDPjPouLSEpZS6vP", "ticker": "OIL.vETH"},
    {"currencyid": "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE", "ticker": "vEURC.vETH"},
    {"currencyid": "iSUD6kGQKDaFUfK6EMYRtR4SNU4wjhEpMi", "ticker": "vOVERRIDE.vETH"},
    {"currencyid": "i9A4wBXUastzupqZwkich4zhCtziZS1JoF", "ticker": "BAT.vETH"},
    {"currencyid": "iExBJfZYK7KREDpuhj6PzZBzqMAKaFg7d2", "ticker": "vARRR"},
    {"currencyid": "iSYJ5L91bURKemiuALK1uBUXad3ZKCpDX7", "ticker": "paxg.vETH"},
    {"currencyid": "i7eFvyL44S2iWz9EZjd6HTaBioFqhALcdi", "ticker": "xaut.vETH"},
    {"currencyid": "iL62spNN42Vqdxh8H5nrfNe8d6Amsnfkdx", "ticker": "NATI.vETH"},
    {"currencyid": "i4Xr5TAMrDTD99H69EemhjDxJ4ktNskUtc", "ticker": "Switch" },
    {"currencyid": "i9kVWKU2VwARALpbXn4RS9zvrhvNRaUibb", "ticker": "Kaiju"},
    {"currencyid": "iHax5qYQGbcMGqJKKrPorpzUBX2oFFXGnY", "ticker": "PURE.vETH"},
]

arr_token_contracts = {
    "0x18084fbA666a33d37592fA2633fD49a74DD93a88": 18,  # tBTC
    "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2": 18,  # MKR
    "0xdAC17F958D2ee523a2206206994597C13D831ec7": 6,   # USDT
    "0x1aBaEA1f7C830bD89Acc67eC4af516284b1bC33c": 6,   # EURC
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48": 6    # USDC
}

arr_token_holders = [
    "0x71518580f36FeCEFfE0721F06bA4703218cD7F63",
    "0x197E90f9FAD81970bA7976f33CbD77088E5D7cf7"
]

def send_request(method, url, headers, data):
    response = requests.request(method, url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# def send_request(method, url, headers, data):
#     response = requests.request(method, url, headers=headers, json=data, auth=(RPCUSER, RPCPASS))
#     return response.json()

def getallbaskets():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencyconverters",
            "params": ["VRSC"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    if isinstance(response, dict) and 'result' in response and isinstance(response['result'], list):
        fully_qualified_names = []
        i_strings = []
        for item in response['result']:
            fully_qualified_name = item.get("fullyqualifiedname")
            i_string = next((key for key in item if key.startswith('i') and len(key) == 34), None)
            if fully_qualified_name and i_string:
                fully_qualified_names.append(fully_qualified_name)
                i_strings.append(i_string)
        return fully_qualified_names, i_strings
    else:
        print("Unexpected response format")
        return [], []

def get_pie_value():
    web3 = Web3(Web3.HTTPProvider(INFURAURL))
    function_signature = web3.keccak(text='pie(address)').hex()[:10]
    encoded_query_address = web3.to_hex(web3.to_bytes(hexstr=arr_token_holders[0]))[2:].zfill(64)
    data = function_signature + encoded_query_address
    url = f'https://api.etherscan.io/api?module=proxy&action=eth_call&to={arr_token_holders[1]}&data={data}&apikey={ETHERSCANAPI}'
    response = requests.get(url).json()
    wei_value = int(response['result'], 16)
    ether_value = web3.from_wei(wei_value, 'ether')
    return ether_value

def get_eth_balance(address):
    url = f'https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCANAPI}'
    response = requests.get(url).json()
    return Decimal(response['result']) / (10 ** 18)  # Convert wei to ether

def get_token_balance(token_contract, decimals):
    url = f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={token_contract}&address={arr_token_holders[0]}&tag=latest&apikey={ETHERSCANAPI}'
    response = requests.get(url).json()
    balance = Decimal(response['result']) / (10 ** decimals)
    return balance

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

def get_dai_price():
    dai = yf.Ticker("DAI-USD")
    data = dai.history(period="1d")
    return Decimal(data['Close'].iloc[-1])

def get_eth_price():
    eth = yf.Ticker("ETH-USD")
    data = eth.history(period="1d")
    return Decimal(data['Close'].iloc[-1])

def get_bridge_currency_bridgeveth():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["Bridge.vETH"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["bestcurrencystate"]["reservecurrencies"]

def get_bridge_currency_racecondition():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["RaceCondition"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["bestcurrencystate"]["reservecurrencies"]

def get_bridge_currency_kaiju():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["Kaiju"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["bestcurrencystate"]["reservecurrencies"]

def get_bridge_currency_pure():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["Pure"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["bestcurrencystate"]["reservecurrencies"]

def get_bridge_currency_switch():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["Switch"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["bestcurrencystate"]["reservecurrencies"]

def get_bridge_currency_kaiju():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["Kaiju"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["bestcurrencystate"]["reservecurrencies"]

def dai_reserves():
    reservecurrencies = get_bridge_currency_bridgeveth()
    dai = next((item for item in reservecurrencies if item["currencyid"] == "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM"), None)
    if dai:
        return dai["reserves"]
    return None

def vrsc_reserves():
    reservecurrencies = get_bridge_currency_bridgeveth()
    vrsc = next((item for item in reservecurrencies if item["currencyid"] == "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"), None)
    if vrsc:
        return vrsc["reserves"]
    return None

def mkr_reserves():
    reservecurrencies = get_bridge_currency_bridgeveth()
    mkr = next((item for item in reservecurrencies if item["currencyid"] == "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4"), None)
    if mkr:
        return mkr["reserves"]
    return None

def eth_reserves():
    reservecurrencies = get_bridge_currency_bridgeveth()
    eth = next((item for item in reservecurrencies if item["currencyid"] == "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X"), None)
    if eth:
        return eth["reserves"]
    return None

def pure_reserves():
    reservecurrencies = get_bridge_currency_pure()
    pure = next((item for item in reservecurrencies if item["currencyid"] == "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU"), None)
    if pure:
        return pure["reserves"]
    return None

def tbtc_reserves():
    reservecurrencies = get_bridge_currency_kaiju()
    tbtc = next((item for item in reservecurrencies if item["currencyid"] == "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU"), None)
    if tbtc:
        return tbtc["reserves"]
    return None

def usdc_reserves():
    reservecurrencies = get_bridge_currency_switch()
    usdc = next((item for item in reservecurrencies if item["currencyid"] == "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd"), None)
    if usdc:
        return usdc["reserves"]
    return None

def eurc_reserves():
    reservecurrencies = get_bridge_currency_switch()
    eth = next((item for item in reservecurrencies if item["currencyid"] == "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE"), None)
    if eth:
        return eth["reserves"]
    return None

def get_ticker_by_currency_id(currency_id):
    currency = next((item for item in arr_currencies if item["currencyid"] == currency_id), None)
    if currency:
        return currency["ticker"]
    return "Currency not found"

def get_currencyid_by_ticker(ticker):
    currency = next((item for item in arr_currencies if item["ticker"] == ticker), None)
    if currency:
        return currency["currencyid"]
    return "Currency not found"

def get_imports(currency: str):
    url = RPCURL

    json_data = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getimports",
        "params": [currency]
    }

    response = requests.post(url, json=json_data)
    return response.json()

def getvarrrblocks():
    req = requests.get("https://varrrexplorer.piratechain.com/api/getblockcount")
    return req.text

def get_imports_with_blocks(currency: str, fromblk: int, toblk: int):
    url = RPCURL

    json_data = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getimports",
        "params": [currency, fromblk, toblk]
    }

    response = requests.post(url, json=json_data)
    return response.json()

def get_address_balance(address):
    json_data = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getaddressbalance",
        "params": [{"addresses": [address]}]
    }

    response = requests.post(RPCURL, json=json_data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve data"}

def get_rawtransaction(txid):
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getrawtransaction",
            "params": [txid],
            "id": 2
        }
    }
    try:
        response = send_request(**requestData)
        raw_transaction_data = response["result"]["transaction_data"]
    except Exception as error:
        return {"error": str(error)}

    return {"raw_transaction": raw_transaction_data}

def calculate_reserve_balance(currencyid: str, currency: str):
    total_reservein = 0.0
    total_reserveout = 0.0
    json_data = get_imports(currency)

    try:
        results = json_data["result"]
        for result in results:
            importnotarization = result["importnotarization"]
            currencystate = importnotarization["currencystate"]
            currencies = currencystate["currencies"]

            for currency_id, currency_data in currencies.items():
                if currency_id == str(currencyid):
                    if "reservein" in currency_data:
                        total_reservein += currency_data["reservein"]
                    if "reserveout" in currency_data:
                        total_reserveout += currency_data["reserveout"]
        ticker = get_ticker_by_currency_id(str(currencyid))
        return {
            "currencyid": ticker,
            "currency": currency,
            "reservein": total_reservein,
            "reserveout": total_reserveout
        }
    except KeyError as e:
        return {"error": f"KeyError: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

def decode_rawtransaction(hex):
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "decoderawtransaction",
            "params": [hex],
            "id": 2
        }
    }
    try:
        response = send_request(**requestData)
        decoded_transaction_data = response["result"]["decoded_data"]
    except Exception as error:
        return {"error": str(error)}
    return {"decoded_transaction": decoded_transaction_data}

def processTransactionCoinbase(vin, vout):
    is_coinbase = len(vin) == 1 and vin[0].get("coinbase")

    if is_coinbase:
        coinbase_reward_address = ""
        if vout[0]["scriptPubKey"]["addresses"][0] == "RCG8KwJNDVwpUBcdoa6AoHqHVJsA1uMYMR":
            coinbase_reward_address = vout[0]["scriptPubKey"]["addresses"][1]
        else:
            coinbase_reward_address = vout[0]["scriptPubKey"]["addresses"][0]

        return {"address": coinbase_reward_address}

    return None

def processTransactionStaking(vin, vout, coinbase_reward_address):
    try:
        matching_vin = next((v for v in vin if v.get("address") == coinbase_reward_address), None)
        matching_vout = next((v for v in vout if coinbase_reward_address in v["scriptPubKey"]["addresses"]), None)

        if matching_vin and matching_vout:
            staking_amount = matching_vout["value"]
            return {"amount": staking_amount, "address": coinbase_reward_address}
    except Exception as error:
        for vin_entry in vin:
            for vout_entry in vout:
                if (
                    vin_entry.get("valueSat") == vout_entry.get("valueSat")
                    and vin_entry.get("addresses")
                    and vout_entry["scriptPubKey"].get("addresses")
                    and len(vin_entry["addresses"]) == 1
                    and len(vout_entry["scriptPubKey"]["addresses"]) == 1
                    and vin_entry["addresses"][0] == vout_entry["scriptPubKey"]["addresses"][0]
                ):
                    return {"amount": vin_entry["value"], "address": vout_entry["scriptPubKey"]["addresses"][0]}

    return None

def processStakeBlock(transactions, block):
    coinbaseRewardAddress = None
    stakingAmount = None
    block_reward = block.get("reward", {})
    block_height = block.get("height", "")
    block_hash = block.get("hash", "")
    validation_type = block.get("validationtype", "")
    
    new_blocks = []

    for transactionId in transactions:
        try:
            transaction = get_rawtransaction(transactionId)

            if not coinbaseRewardAddress:
                coinbaseReward = processTransactionCoinbase(transaction)
                if coinbaseReward:
                    coinbaseRewardAddress = coinbaseReward["address"]
            if coinbaseRewardAddress:
                staking_reward = processTransactionStaking(transaction, coinbaseRewardAddress)
                if staking_reward:
                    stakingAmount = staking_reward["amount"]
                    new_block = {
                        "blockHeight": block_height,
                        "blockHash": block_hash,
                        "validationType": validation_type,
                        "coinbaseRewardAddress": coinbaseRewardAddress,
                        "stakingAmount": stakingAmount,
                        "stakingAddress": staking_reward["address"],
                        "blockRewards": block_reward
                    }
                    new_blocks.append(new_block)
                    print(new_block)

        except Exception as error:
            print('Error fetching transaction data:', error)

    return new_blocks

def fetchBlocksAndProcess(num_blocks, block_hash):
    current_block_hash = block_hash
    blocks_processed = 0
    request_config_get_block = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getblock",
            "params": [],
            "id": 1
        }
    }

    def process_next_block():
        nonlocal blocks_processed, current_block_hash

        if blocks_processed >= num_blocks:
            return {"result": "Process completed"}
        request_config_get_block["data"]["params"] = [current_block_hash, True]

        try:
            # Simulate sending the request
            response = send_request(request_config_get_block)
            block = response["result"]
            validation_type = block["validationtype"]

            if validation_type == "stake":
                # Replace this with your actual implementation
                processStakeBlock(block)
                blocks_processed += 1

            current_block_hash = block["previousblockhash"]
        except Exception as error:
            return {"error": str(error)}

        return process_next_block()

    # Start the process with the initial call
    return process_next_block()

def diff_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', ' Thousand', ' Million', ' Billion', ' Trillion'][magnitude])

def getcurrencyvolumeinfo(currency, fromblock, endblock, interval, volumecurrency):
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencystate",
            "params": [currency, f"{fromblock}, {endblock}, {interval}", volumecurrency],
            "id": 1
        }
    }
    response = send_request(**requestData)
    
    try:
        nresponse = response['result'][1]['conversiondata']
        if all(key in nresponse for key in ["volumecurrency", "volumepairs", "volumethisinterval"]):
            new_response = nresponse['volumepairs']
            new_volume_response = nresponse['volumethisinterval']
        else:
            new_response = None
            new_volume_response = None
    except (KeyError, IndexError):
        new_response = None
        new_volume_response = None
    return new_response, new_volume_response

def getdefivolume(currency, fromblock, endblock, interval, volumecurrency):
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencystate",
            "params": [currency, f"{fromblock}, {endblock}, {interval}", volumecurrency],
            "id": 1
        }
    }
    response = send_request(**requestData)
    
    try:
        nresponse = response['result'][1]['conversiondata']
        if all(key in nresponse for key in ["volumecurrency", "volumepairs", "volumethisinterval"]):
            new_volume_response = nresponse['volumethisinterval']
        else:
            new_volume_response = None
    except (KeyError, IndexError):
        new_volume_response = None
    return new_volume_response

def calculatevolumeinfo():
    currblock = latest_block()
    blockint = int(currblock) - 1440
    baskets, i_addresses = getallbaskets()
    
    data = {}
    for basket in baskets:
        volume_info = getcurrencyvolumeinfo(basket, blockint, currblock, 1440, "VRSC")
        data[basket] = volume_info

    return data
    
def getvrscreserves_frombaskets(basket):
    requestData = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com/",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencyconverters",
            "params": [f"{basket}"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    data = response.get('result')
    total_initialsupply = 0
    total_startblock = 0
    total_reservein = 0
    total_reserveout = 0
    reserves = []
    priceinreserve = []
    for item in data:
        currency_info = item.get('i3f7tSctFkiPpiedY8QR5Tep9p4qDVebDx')
        last_notarization = item.get('lastnotarization')
        if currency_info:
            total_initialsupply += currency_info.get('initialsupply', 0)
            total_startblock += currency_info.get('startblock', 0)
        if last_notarization:
            currencystate = last_notarization.get('currencystate', {})
            currencies = currencystate.get('currencies', {})
            for key, value in currencies.items():
                total_reservein += value.get('reservein', 0)
                total_reserveout += value.get('reserveout', 0)
            reservecurrencies = currencystate.get('reservecurrencies', [])
            for rc in reservecurrencies:
                reserves.append(rc.get('reserves', 0))
                priceinreserve.append(rc.get('priceinreserve', 0))
    volume = total_reservein + total_reserveout
    return reserves[0]

def formatHashrate(hashrate):
    if hashrate < 1000:
        return f"{round(hashrate, 2)}H/s"
    elif hashrate < 1000000:
        return f"{round(hashrate/1000, 2)}kH/s"
    elif hashrate < 1000000000:
        return f"{round(hashrate/1000000, 2)}MH/s"
    elif hashrate < 1000000000000:
        return f"{round(hashrate/1000000000, 2)}GH/s"

def get_reserve_dai_price(reserves):
    return round(dai_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_vrsc_price(reserves):
    return round(vrsc_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_mkr_price(reserves):
    return round(mkr_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_eth_price(reserves):
    return round(eth_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_pure_price(reserves):
    return round(pure_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_tbtc_price(reserves):
    return round(tbtc_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_usdc_price(reserves):
    return round(usdc_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_eurc_price(reserves):
    return round(eurc_reserves() / reserves, 6) if reserves != 0 else 0.0

def calculate_total_balances(currency: str):
    total_reservein = 0.0
    total_reserveout = 0.0
    total_conversion_fees = 0.0
    total_primary_currency_in = 0.0
    total_primary_currency_out = 0.0
    json_data = get_imports(currency)

    try:
        results = json_data["result"]
        for result in results:
            importnotarization = result["importnotarization"]
            currencystate = importnotarization["currencystate"]
            currencies = currencystate["currencies"]

            for currency_data in currencies.values():
                total_reservein += currency_data.get("reservein", 0.0)
                total_reserveout += currency_data.get("reserveout", 0.0)
                total_conversion_fees += currency_data.get("conversionfees", 0.0)
                total_primary_currency_in += currency_data.get("primarycurrencyin", 0.0)
                total_primary_currency_out += currency_data.get("primarycurrencyout", 0.0)
        reserves = dai_reserves()
        resp = get_reserve_dai_price(reserves)

        return {
            "DAI price in DAI reserves": resp,
            "total_reservein": f"{int(resp) * total_reservein} DAI",
            "total_reserveout": f"{int(resp) * total_reserveout} DAI",
            "total_conversion_fees": f"{int(resp) * total_conversion_fees} DAI",
            "total_primary_currency_in": f"{int(resp) * total_primary_currency_in} DAI",
            "total_primary_currency_out": f"{int(resp) * total_primary_currency_out} DAI",
        }
    except KeyError as e:
        return {"error": f"KeyError: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

def extract_transfers(currency: str):
    transfers_list = []
    json_data = get_imports(currency)
    try:
        results = json_data.get("result", [])
        for result in results:
            exporttxid = result.get("import", [])
            exporttxid = exporttxid['exporttxid']
            importtxid = result.get("importtxid", [])
            transfers = result.get("transfers", [])
            resp = (transfers, exporttxid, importtxid)
            transfers_list.extend(resp)

        return transfers_list
    except Exception as e:
        return {"error": str(e)}

def getcurrencystate(currency, height):
    url = 'https://rpc.vrsc.komodefi.com/'
    payload = {
        'id': 1,
        'jsonrpc': '2.0',
        'method': 'getcurrencystate',
        "params": [currency, height]
    }
    response = requests.post(url, json=payload).json()
    return response

def aggregate_reserve_data(currencyid, height):
    currencies_data = {
        "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV": {"total_reserve": 0},
        "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X": {"total_reserve": 0},
        "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4": {"total_reserve": 0},
        "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM": {"total_reserve": 0}
    }
    
    for _ in range(1440):
        response = getcurrencystate(currencyid, height)
        for currency_id, data in currencies_data.items():
            currency_info = response['result'][0]['currencystate']['currencies'][currency_id]
            data['total_reserve'] += currency_info['reservein'] + currency_info['reserveout']
        height = str(int(height) - 1)
    
    # Fetch currency names and structure the result
    result = {}
    for currency_id, data in currencies_data.items():
        currency_name = get_ticker_by_currency_id(currency_id)
        result[currency_name] = data['total_reserve']
    
    return result
       
def latest_block():
    requestData = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getinfo",
            "params": [],
            "id": 3
        }
    }
    try:
        response = send_request(**requestData)
        latestblock = response['result']['blocks']
        return latestblock
    except:
        return "Error!!, success: False"

def load_from_json():
    try:
        with open('temp_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Temporary JSON file not found.")
        return None
    
def get_basket_supply(basket_name):
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": [basket_name],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["lastconfirmedcurrencystate"]["supply"]

def extract_i_address(data):
    for item in data:
        for key in item.keys():
            if key.startswith('i'):
                return key
    return None

def get_verus_coin_price():
    # Get Verus Coin price from Yahoo Finance
    verus = yf.Ticker("VRSC-USD")  # Replace with correct symbol if needed
    return Decimal(verus.history(period="1d")["Close"].iloc[-1])

def get_currencyconverters(basket_name):
    networkblocks = latest_block()
    reserves = dai_reserves()
    resp = get_reserve_dai_price(reserves)
    supply = get_basket_supply(basket_name)

    requestData = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com/",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencyconverters",
            "params": [basket_name],
            "id": 1
        }
    }
    response = send_request(**requestData)

    data = response.get('result')
    if not data:
        return None

    i_address = extract_i_address(data)
    if not i_address:
        return None

    total_initialsupply = 0
    total_startblock = 0
    total_reservein = 0
    total_reserveout = 0
    reserves = []
    priceinreserve = []

    for item in data:
        last_notarization = item.get('lastnotarization')
        if last_notarization:
            currencystate = last_notarization.get('currencystate', {})
            reservecurrencies = currencystate.get('reservecurrencies', [])
            for rc in reservecurrencies:
                reserves.append(rc.get('reserves', 0))
                priceinreserve.append(rc.get('priceinreserve', 0))

    volume = total_reservein + total_reserveout

    # Creating the output dictionary
    output = {
        "bridge": basket_name,
        "i_address": i_address,
        "initialsupply": total_initialsupply,
        "supply": supply,
        "startblock": total_startblock,
        "block": networkblocks,
        "blk_volume": volume,
    }

    # Adding reserve and price information to the output, with filtering for specific basket
    for i in range(len(reserves)):
        if basket_name == "Bridge.vETH" and i >= 4:
            continue
        output[f"reserves_{i}"] = reserves[i] * resp
        output[f"price_in_reserves_{i}"] = priceinreserve[i] * resp

    return output

def get_currencyconverters(basket_name):
    networkblocks = latest_block()
    reserves = dai_reserves()
    resp = get_reserve_dai_price(reserves)
    supply = get_basket_supply(basket_name)

    requestData = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com/",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencyconverters",
            "params": [basket_name],
            "id": 1
        }
    }
    response = send_request(**requestData)

    data = response.get('result')
    if not data:
        return None

    i_address = extract_i_address(data)
    if not i_address:
        return None

    total_initialsupply = 0
    total_startblock = 0
    total_reservein = 0
    total_reserveout = 0
    reserves = []
    priceinreserve = []

    for item in data:
        currency_info = item.get(i_address)
        last_notarization = item.get('lastnotarization')

        if currency_info:
            total_initialsupply += currency_info.get('initialsupply', 0)
            total_startblock += currency_info.get('startblock', 0)

        if last_notarization:
            currencystate = last_notarization.get('currencystate', {})
            currencies = currencystate.get('currencies', {})

            for key, value in currencies.items():
                total_reservein += value.get('reservein', 0)
                total_reserveout += value.get('reserveout', 0)

            reservecurrencies = currencystate.get('reservecurrencies', [])
            for rc in reservecurrencies:
                reserves.append(rc.get('reserves', 0))
                priceinreserve.append(rc.get('priceinreserve', 0))

    volume = total_reservein + total_reserveout

    # Creating the output dictionary
    output = {
        "bridge": basket_name,
        "initialsupply": total_initialsupply,
        "supply": supply,
        "startblock": total_startblock,
        "block": networkblocks,
        "blk_volume": volume,
    }

    # Adding reserve and price information to the output, with filtering for specific basket
    for i in range(len(reserves)):
        if basket_name == "Bridge.vETH" and i >= 4:
            continue
        output[f"reserves_{i}"] = reserves[i] * resp
        output[f"price_in_reserves_{i}"] = priceinreserve[i] * resp

    return output

def getdefichain(basket):
    reserves = dai_reserves()
    resp = get_reserve_dai_price(reserves)
    latest = latest_block()
    volblock = int(latest) - 1440
    
    requestData = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com/",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencyconverters",
            "params": [basket],
            "id": 1
        }
    }
    
    response = send_request(**requestData)
    data = response.get('result')
    if not data:
        return None

    result = []
    volume_info = {}

    # Get volume information for each basket
    for item in data:
        fully_qualified_name = item.get('fullyqualifiedname')
        i_address = next((key for key in item.keys() if key.startswith('i') and len(key) > 1), None)
        
        reserves = []
        priceinreserve = []
        currencyids = []
        total_fees = 0.0
        
        if i_address:
            currency_data = item[i_address]
            last_notarization = item.get('lastnotarization')
            if last_notarization:
                currencystate = last_notarization.get('currencystate', {})
                reservecurrencies = currencystate.get('reservecurrencies', [])
                currencies = currencystate.get('currencies', {})
                for rc in reservecurrencies:
                    reserves_value = rc.get('reserves', 0) * resp
                    priceinreserve_value = rc.get('priceinreserve', 0) * resp
                    reserves.append(reserves_value)
                    priceinreserve.append(priceinreserve_value)
                    currencyids.append(rc.get('currencyid'))

                # Aggregate and multiply all 'fees' from the 'currencystate.currencies'
                for currency_id, currency_info in currencies.items():
                    total_fees += currency_info.get('fees', 0)
                
                total_fees *= resp  # Multiply the aggregated fees by resp
        
        tickers = [get_ticker_by_currency_id(currency_id) for currency_id in currencyids]
        
        # Get volume for the current basket
        volume = getdefivolume(basket, volblock, latest, 1440, "VRSC")
        if volume is not None:
            if isinstance(volume, list):
                for vol in volume:
                    volume_info[vol['basket_name']] = vol['volume']
            else:
                volume_info[basket] = volume  # Handle the case where volume is a single float value
        else:
            volume_info[basket] = None
        
        formatted_priceinreserve = [format(value, '.10f') for value in priceinreserve]
        
        result.append({
            "fullyqualifiedname": fully_qualified_name,
            "i_address": i_address,
            "reserves": reserves,
            "priceinreserve": formatted_priceinreserve,
            "currencyids": currencyids,
            "tickers": tickers,
            "fees": total_fees,  # Add aggregated fees (multiplied by resp) to the result
        })
    
    formatted_baskets = []
    for basket in result:
        formatted_basket = {
            "liquiditypool": basket['fullyqualifiedname'],
            "lp_address": basket['i_address'],
            "fees": basket['fees'],  # Add fees to the formatted_basket
            "lp_volume": volume_info.get(basket['fullyqualifiedname'], None),  # Include volume in the formatted basket
            "tokens": []
        }
        for i, ticker in enumerate(basket['tickers']):
            formatted_basket["tokens"].append({
                "ticker": ticker,
                "reserves": basket['reserves'][i],
                "priceinreserve": float(basket['priceinreserve'][i]),
                "i_address": basket['currencyids'][i]
            })
        formatted_baskets.append(formatted_basket)

    return formatted_baskets

@app.get("/")
def main():    
    return "result: VerusCoin Multipurpose API running on port {PORT}, an API that knows everything about verus. Use it with responsibility and have fun building your project!!", "success: True"

@app.get('/price/{ticker}')
def price(ticker):
    try:
        resp = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids=verus-coin&vs_currencies={ticker}&include_24hr_change=true")
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/difficulty')
def difficulty():
    try:
        resp = requests.get("https://explorer.verus.io/api/getdifficulty")
        cleanresp = re.sub('"', '', resp.text)
        newresp = diff_format(float(cleanresp))
        return newresp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getcurrencystate/{currency}/{height}')
def routegetcurrencystate(currency, height):
    try:
        data = getcurrencystate(currency, height)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/decoderawtransaction/{hex}')
def decode_rawtransaction_route(hex):
    try:
        data = decode_rawtransaction(hex)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getrawtransaction/{txid}')
def get_rawtransaction_route(txid):
    try:
        data = get_rawtransaction(txid)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/blockcount')
def routelatest_block():
    try:
        data = latest_block()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getcurrencies/Bridge.vETH')
def getcurrenciesbridgeveth():
    try:
        reservecurrencies = get_bridge_currency_bridgeveth()
        return reservecurrencies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getcurrencies/RaceCondition')
def getcurrenciesracecondition():
    try:
        reservecurrencies = get_bridge_currency_racecondition()
        return reservecurrencies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/getcurrencies/Kaiju')
def getcurrencieskaiju():
    try:
        reservecurrencies = get_bridge_currency_kaiju()
        return reservecurrencies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getcurrencies/Switch')
def getcurrenciesswitch():
    try:
        reservecurrencies = get_bridge_currency_switch()
        return reservecurrencies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/getcurrencies/Kaiju')
def getcurrencieskaiju():
    try:
        reservecurrencies = get_bridge_currency_kaiju()
        return reservecurrencies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getcurrencies/Pure')
def getcurrenciespure():
    try:
        reservecurrencies = get_bridge_currency_pure()
        return reservecurrencies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/dai_reserves')
def getdaireserves():
    try:
        daireserve = dai_reserves()
        return daireserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/vrsc_reserves')
def getvrscreserves():
    try:
        vrscreserve = vrsc_reserves()
        return vrscreserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/mkr_reserves')
def getmkrreserves():
    try:
        mkrreserve = mkr_reserves()
        return mkrreserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/eth_reserves')
def getethreserves():
    try:
        ethreserve = eth_reserves()
        return ethreserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/pure_reserves')
def getpurereserves():
    try:
        purereserve = pure_reserves()
        return purereserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/tbtc_reserves')
def gettbtcreserves():
    try:
        tbtcreserve = tbtc_reserves()
        return tbtcreserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/usdc_reserves')
def getusdcreserves():
    try:
        usdcreserve = usdc_reserves()
        return usdcreserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/eurc_reserves')
def geteurcreserves():
    try:
        eurcreserve = eurc_reserves()
        return eurcreserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getticker/{currency_id}')
def get_ticker_route(currency_id):
    try:
        ticker = get_ticker_by_currency_id(currency_id)
        return {"ticker": ticker}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getcurrid/{ticker}')
def get_currid_route(ticker):
    try:
        currid = get_currencyid_by_ticker(ticker)
        return {"currencyid": currid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getrawmempool')
def get_rawmempool_route():
    requestData = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getrawmempool",
            "params": [],
            "id": 2
        }
    }
    try:
        response = send_request(**requestData)
        mempool_res = response["result"]
        mempool_count = len(mempool_res)
        print(mempool_res[0])

    except Exception as error:
        return {"error": str(error)}

    return {
        "mempool_res": mempool_res,
        "mempool_count": mempool_count,
    }

@app.get('/fetchblockhash/{longest_chain}')
def fetch_block_hash_route(longest_chain):
    request_data = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getblockhash",
            "params": [longest_chain],
            "id": 1
        }
    }
    try:
        # Simulate sending the request
        response = send_request(**request_data)
        block_hash_data = response["result"]
    except Exception as error:
        return {"error": str(error)}

    # In your actual implementation, you can replace the simulated response with the real block hash data.
    return {"block_hash": block_hash_data}

@app.get('/fetchtransactiondata/{transaction_id}')
def fetch_transaction_data_route(transaction_id):
    request_config_get_raw_transaction = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getrawtransaction",
            "params": [transaction_id],
            "id": 1
        }
    }
    try:
        response = send_request(**request_config_get_raw_transaction)
        raw_transaction_data = response["result"]
    except Exception as error:
        return {"error": str(error)}
    request_config_decode_raw_transaction = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "decoderawtransaction",
            "params": [raw_transaction_data],
            "id": 1
        }
    }
    try:
        # Simulate sending the request
        response = send_request(**request_config_decode_raw_transaction)
        decoded_transaction_data = response["result"]
    except Exception as error:
        return {"error": str(error)}
    # In your actual implementation, you can replace the simulated responses with the real transaction data.
    return {"transaction_data": decoded_transaction_data}

@app.get('/getmoneysupply')
def getmoneysupply():
    resp = requests.get("https://explorer.verus.io/ext/getmoneysupply")
    return resp.text, "success: True"

@app.get('/distribution')
def getdistribution():
    resp = requests.get("https://explorer.verus.io/ext/getdistribution")
    return resp.json()

@app.get('/getnethashpower')
def getnethashpower():
    resp = requests.get("https://insight.verus.io/api/getnetworkhashps")
    value = formatHashrate(int(resp.text))
    return value, "success: True"

@app.get('/getweight_bridgeveth')
def getweightbridgeveth():
    resp = get_bridge_currency_bridgeveth()
    weights = [item['weight'] for item in resp]
    return {'weights': weights}

@app.get('/getweight_racecondition')
def getweightracecondition():
    resp = get_bridge_currency_racecondition()
    weights = [item['weight'] for item in resp]
    return {'weights': weights}

@app.get('/getweight_kaiju')
def getweightkaiju():
    resp = get_bridge_currency_kaiju()
    weights = [item['weight'] for item in resp]
    return {'weights': weights}

@app.get('/getweight_switch')
def getweightswitch():
    resp = get_bridge_currency_switch()
    weights = [item['weight'] for item in resp]
    return {'weights': weights}

@app.get('/getweight_pure')
def getweightpure():
    resp = get_bridge_currency_pure()
    weights = [item['weight'] for item in resp]
    return {'weights': weights}

@app.get('/getbridgedaiprice')
def getbridgedaireserveprice():
    reservecurrencies = get_bridge_currency_bridgeveth()
    dai = next((item for item in reservecurrencies if item["currencyid"] == "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM"), None)
    if dai:
        return dai["priceinreserve"], "success: True"
    return None

@app.get('/getbridgevrscprice')
def getbridgevrscreserveprice():
    reservecurrencies = get_bridge_currency_bridgeveth()
    vrsc = next((item for item in reservecurrencies if item["currencyid"] == "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"), None)
    if vrsc:
        return vrsc["priceinreserve"], "success: True"
    return None

@app.get('/getbridgemkrprice')
def getbridgemkrreserveprice():
    reservecurrencies = get_bridge_currency_bridgeveth()
    mkr = next((item for item in reservecurrencies if item["currencyid"] == "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4"), None)
    if mkr:
        return mkr["priceinreserve"], "success: True"
    return None

@app.get('/getbridgeethprice')
def getbridgeethreserveprice():
    reservecurrencies = get_bridge_currency_bridgeveth()
    eth = next((item for item in reservecurrencies if item["currencyid"] == "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X"), None)
    if eth:
        return eth["priceinreserve"], "success: True"
    return None

@app.get('/getbridgepureprice')
def getbridgepurereserveprice():
    reservecurrencies = get_bridge_currency_pure()
    pure = next((item for item in reservecurrencies if item["currencyid"] == "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU"), None)
    if pure:
        return pure["priceinreserve"], "success: True"
    return None

@app.get('/getbridgetbtcprice')
def getbridgetbtcreserveprice():
    reservecurrencies = get_bridge_currency_kaiju()
    tbtc = next((item for item in reservecurrencies if item["currencyid"] == "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU"), None)
    if tbtc:
        return tbtc["priceinreserve"], "success: True"
    return None

@app.get('/getbridgeusdcprice')
def getbridgeusdcreserveprice():
    reservecurrencies = get_bridge_currency_switch()
    usdc = next((item for item in reservecurrencies if item["currencyid"] == "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd"), None)
    if usdc:
        return usdc["priceinreserve"], "success: True"
    return None

@app.get('/getbridgeeurcprice')
def getbridgeeurcreserveprice():
    reservecurrencies = get_bridge_currency_switch()
    eurc = next((item for item in reservecurrencies if item["currencyid"] == "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE"), None)
    if eurc:
        return eurc["priceinreserve"], "success: True"
    return None

@app.get('/getdaiveth_daireserveprice')
def getdaivethdaireserveprice():
    reserves = dai_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/getvrsc_daireserveprice')
def getvrscdaireserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/getmkrveth_daireserveprice')
def getmkrvethdaireserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/getveth_daireserveprice')
def getvethdaireserveprice():
    reserves = eth_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/getpure_daireserveprice')
def getpuredaireserveprice():
    reserves = pure_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_daireserveprice')
def gettbtcdaireserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_daireserveprice')
def getusdcdaireserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_daireserveprice')
def geteurcdaireserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/getdaiveth_vrscreserveprice')
def getdaivethvrscreserveprice():
    reserves = dai_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/getvrsc_vrscreserveprice')
def getvrscvrscreserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/getmkrveth_vrscreserveprice')
def getmkrvethvrscreserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/getveth_vrscreserveprice')
def getvethvrscreserveprice():
    reserves = eth_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/getpure_vrscreserveprice')
def getpurevrscreserveprice():
    reserves = pure_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_vrscreserveprice')
def gettbtcvrscreserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_vrscreserveprice')
def getusdcvrscreserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_vrscreserveprice')
def geteurcvrscreserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/getdaiveth_mkrreserveprice')
def getdaivethmkrreserveprice():
    reserves = dai_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/getvrsc_mkrreserveprice')
def getvrscmkrreserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/getmkrveth_mkrreserveprice')
def getmkrvethmkrreserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/getveth_mkrreserveprice')
def getvethmkrreserveprice():
    reserves = eth_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/getpure_mkrreserveprice')
def getpuremkrreserveprice():
    reserves = pure_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_mkrreserveprice')
def gettbtcmkrreserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_mkrreserveprice')
def getusdcmkrreserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_mkrreserveprice')
def geteurcmkrreserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/getdaiveth_vethreserveprice')
def getdaivethvethreserveprice():
    reserves = dai_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/getvrsc_vethreserveprice')
def getvrscvethreserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/getmkrveth_vethreserveprice')
def getmkrvethvethreserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/getveth_vethreserveprice')
def getvethvethreserveprice():
    reserves = eth_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/getpure_vethreserveprice')
def getpurevethreserveprice():
    reserves = pure_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_vethreserveprice')
def gettbtcvethreserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_vethreserveprice')
def getusdcvethreserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_vethreserveprice')
def geteurcvethreserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/getdaiveth_purereserveprice')
def getdaivethpurereserveprice():
    reserves = dai_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/getvrsc_purereserveprice')
def getvrscpurereserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/getmkrveth_purereserveprice')
def getmkrvethpurereserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/getveth_purereserveprice')
def getvethpurereserveprice():
    reserves = eth_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_purereserveprice')
def gettbtcpurereserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/getpure_purereserveprice')
def getpurepurereserveprice():
    reserves = pure_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_tbtcreserveprice')
def gettbctbtcrereserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_tbtc_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_purereserveprice')
def getusdcpurereserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_tbtcreserveprice')
def getusdctbtcrereserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_tbtc_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_tbtcreserveprice')
def geteurctbtcrereserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_tbtc_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_purereserveprice')
def geteurcpurereserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/getdaiveth_usdcreserveprice')
def getdaivethusdcreserveprice():
    reserves = dai_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/getvrsc_usdcreserveprice')
def getvrscusdcreserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/getmkrveth_usdcreserveprice')
def getmkrvethusdcreserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/getveth_usdcreserveprice')
def getvethusdcreserveprice():
    reserves = eth_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/getpure_usdcreserveprice')
def getpureusdcreserveprice():
    reserves = pure_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_usdcreserveprice')
def gettbtcusdcreserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_usdcreserveprice')
def getusdcusdcreserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_usdcreserveprice')
def geteurcusdcreserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/getdaiveth_eurcreserveprice')
def getdaivetheurcreserveprice():
    reserves = dai_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/getvrsc_eurcreserveprice')
def getvrsceurcreserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/getmkrveth_eurcreserveprice')
def getmkrvetheurcreserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/getveth_eurcreserveprice')
def getvetheurcreserveprice():
    reserves = eth_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/getpure_eurcreserveprice')
def getpureeurcreserveprice():
    reserves = pure_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_eurcreserveprice')
def gettbctheurcreserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_eurcreserveprice')
def getusdceurcreserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_eurcreserveprice')
def geteurceurcreserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/getimports/{currency}')
def routegetimports(currency: str):
    # newfromblk = int(fromblk)
    # newtoblk = int(toblk)
    try:
        newcurrency = str(currency)
        response = get_imports(newcurrency)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getimports_blk/{currency}/{fromblk}/{toblk}/')
def routegetimports_blk(currency: str, fromblk: int, toblk: int):
    newfromblk = int(fromblk)
    newtoblk = int(toblk)
    newcurrency = str(currency)
    response = get_imports_with_blocks(newcurrency, newfromblk, newtoblk)
    return response

@app.get('/getvolume/{currencyid}/{currency}/{fromblk}/{toblk}')
def routegetvolume(currencyid: str, currency: str, fromblk: int, toblk: int):
    newfromblk = int(fromblk)
    newtoblk = int(toblk)
    newcurrency = str(currency)
    newcurrencyid = str(currencyid)
    response = calculate_reserve_balance(newcurrencyid, newcurrency, newfromblk, newtoblk)
    return response, "success: True"

@app.get('/gettotalvolume/{currency}/{fromblk}/{toblk}')
def routegettotalvolume(currency: str, fromblk: int, toblk: int):
    newfromblk = int(fromblk)
    newtoblk = int(toblk)
    newcurrency = str(currency)
    response = calculate_total_balances(newcurrency, newfromblk, newtoblk)
    return response, "success: True"

@app.get('/gettransactions/{currency}/{fromblk}/{toblk}')
def routegettxns(currency: str, fromblk: int, toblk: int):
    newfromblk = int(fromblk)
    newtoblk = int(toblk)
    newcurrency = str(currency)
    response = extract_transfers(newcurrency, newfromblk, newtoblk)
    return response

@app.get('/getaddressbalance/{address}')
def routegetaddressbalance(address: str):
    newaddress = str(address)
    response = get_address_balance(newaddress)
    return response

@app.get('/getbasketinfo/')
def routegetbasketsupply():
    try:
        baskets, i_addresses = getallbaskets()
        data = []
        for basket in baskets:
            basket_info = get_currencyconverters(basket)
            if basket_info:
                data.append(basket_info)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getcurrencyvolumes')
def routegetcurrencyvolumes():
    jsond = calculatevolumeinfo()
    return jsond

########################################################################################################################################################################################
# MARKET ROUTES
########################################################################################################################################################################################

@app.get('/market/allTickers')
def routegetalltickers():
    baskets, i_addresses = getallbaskets()
    latestblock = latest_block()
    volblock = int(latestblock) - 1440
    timestamp = int(time.time() * 1000)
    ticker_info = []

    for basket in baskets:
        volume_info, currencyvolume = getcurrencyvolumeinfo(basket, volblock, latestblock, 1440, "VRSC")
        getvrscweightsfrombaskets = getvrscreserves_frombaskets(basket)
        weightedreserves = np.array(getvrscweightsfrombaskets)

        if volume_info is not None:
            for pair in volume_info:
                # Remove .vETH suffix and 'v' prefix from currency names
                if pair['currency'] == "Bridge.vETH" or pair['convertto'] == "Bridge.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                else:
                    currency = pair['currency'].replace(".vETH", "").lstrip('v')
                    convertto = pair['convertto'].replace(".vETH", "").lstrip('v')

                if currency == "VRSC" or convertto == "VRSC":
                    # Reverse currency and convertto in the pair
                    if currency == "Bridge.vETH" or convertto == "Bridge.vETH":
                        currency_pair = f"Bridge.vETH-VRSC" if currency == "Bridge.vETH" else f"{convertto}-VRSC"
                    else:
                        currency_pair = f"{convertto}-{currency}"

                    # Calculate weights based on volume
                    weights = pair['volume'] / np.sum(pair['volume'])

                    # Invert values if VRSC is the quote currency (second position)
                    if convertto == "VRSC":
                        volume = pair['volume'] * 2
                        last = np.dot(weights, 1 / pair['close']) / np.sum(weights)
                        high = np.dot(weights, 1 / pair['high']) / np.sum(weights)
                        low = np.dot(weights, 1 / pair['low']) / np.sum(weights)
                        openn = np.dot(weights, 1 / pair['open']) / np.sum(weights)
                    else:
                        volume = pair['volume']
                        last = np.dot(weights, pair['close']) / np.sum(weights)
                        high = np.dot(weights, pair['high']) / np.sum(weights)
                        low = np.dot(weights, pair['low']) / np.sum(weights)
                        openn = np.dot(weights, pair['open']) / np.sum(weights)

                    ticker_info.append({
                        'symbol': currency_pair,
                        'symbolName': currency_pair,
                        'volume': volume,
                        'last': last,
                        'high': high,
                        'low': low,
                        'open': openn
                    })

    # Combine reverse pairs
    combined_ticker_info = {}
    for ticker in ticker_info:
        symbol = ticker['symbol']
        reverse_symbol = "-".join(symbol.split("-")[::-1])

        if symbol in combined_ticker_info:
            combined_volume = combined_ticker_info[symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_info[symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_info[symbol]['volume'] = combined_volume
            combined_ticker_info[symbol]['last'] = np.dot(
                [combined_ticker_info[symbol]['last'], ticker['last']], combined_weights)
            combined_ticker_info[symbol]['high'] = np.dot(
                [combined_ticker_info[symbol]['high'], ticker['high']], combined_weights)
            combined_ticker_info[symbol]['low'] = np.dot(
                [combined_ticker_info[symbol]['low'], ticker['low']], combined_weights)
            combined_ticker_info[symbol]['open'] = np.dot(
                [combined_ticker_info[symbol]['open'], ticker['open']], combined_weights)
        elif reverse_symbol in combined_ticker_info:
            combined_volume = combined_ticker_info[reverse_symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_info[reverse_symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_info[reverse_symbol]['volume'] = combined_volume
            combined_ticker_info[reverse_symbol]['last'] = np.dot(
                [combined_ticker_info[reverse_symbol]['last'], ticker['last']], combined_weights)
            combined_ticker_info[reverse_symbol]['high'] = np.dot(
                [combined_ticker_info[reverse_symbol]['high'], ticker['low']], combined_weights)
            combined_ticker_info[reverse_symbol]['low'] = np.dot(
                [combined_ticker_info[reverse_symbol]['low'], ticker['high']], combined_weights)
            combined_ticker_info[reverse_symbol]['open'] = np.dot(
                [combined_ticker_info[reverse_symbol]['open'], ticker['open']], combined_weights)
        else:
            combined_ticker_info[symbol] = ticker

    # Convert combined ticker info to list
    final_ticker_info = list(combined_ticker_info.values())

    # Flip VRSC-MKR to MKR-VRSC
    for ticker in final_ticker_info:
        if ticker['symbol'] == "VRSC-MKR":
            ticker['symbol'] = "MKR-VRSC"
            ticker['symbolName'] = "MKR-VRSC"

    return {
        "code": "200000",
        "data": {
            "time": timestamp,
            "ticker": final_ticker_info
        }
    }

@app.get('/gettvl')
def gettvl():
    try:
        baskets, i_addresses = getallbaskets()
        data = []
        for basket in baskets:
            basket_info = get_currencyconverters(basket)
            if basket_info:
                data.append(basket_info)
        
        # Get prices and balances
        dai_price = get_dai_price()
        pie_value = get_pie_value()
        dai_usd_value = pie_value * dai_price

        eth_price = get_eth_price()
        eth_balance = get_eth_balance(arr_token_holders[0])

        # Get Verus Coin price
        verus_price = get_verus_coin_price()  # Assumed to be returning Decimal

        token_balances = {}
        network_tvl = dai_usd_value + (eth_balance * eth_price)

        # Calculate token balances and their USD values
        for token_contract, decimals in arr_token_contracts.items():
            balance = get_token_balance(token_contract, decimals)
            price = get_token_price(token_contract)
            usd_value = balance * price
            token_balances[token_contract] = {
                'balance': '{:.10f}'.format(balance),
                'usd_value': '{:.8f}'.format(usd_value)
            }
            network_tvl += usd_value

        # Extract reserves_0 values and calculate
        reserves_0_total = Decimal('0')
        for basket in data:
            basket_name = basket["bridge"]
            reserves_0 = Decimal(basket.get("reserves_0", 0))  # Default to 0 if key is not present
            reserves_0_usd_value = reserves_0 * verus_price
            reserves_0_total += reserves_0_usd_value
            token_balances[basket_name] = {
                'VRSC_reserves': '{:.10f}'.format(reserves_0),
                'usd_value': '{:.8f}'.format(reserves_0_usd_value)
            }

        network_tvl += reserves_0_total

        # Add ETH and DAI details
        token_balances['DAI_Price'] = '{:.8f}'.format(dai_price)
        token_balances['DAI_Balance'] = '{:.8f}'.format(pie_value)
        token_balances['ETH_Price'] = '{:.8f}'.format(eth_price)
        token_balances['ETH_Balance'] = '{:.8f}'.format(eth_balance)
        token_balances['Network_TVL'] = '{:.8f}'.format(network_tvl)

        return {
            "code": "200000",
            "data": {
                "result": token_balances
            }
        }
    except HTTPException as e:
        return {
            "code": "500000",
            "message": e.detail
        }
    except Exception as e:
        return {
            "code": "500000",
            "message": f"An unexpected error occurred: {str(e)}"
        }

@app.get('/getdefichaininfo')
def getdefichaininfo():
    timestamp = int(time.time() * 1000)
    try:
        baskets, i = getallbaskets()
        output = []
        for basket in baskets:
            out = getdefichain(basket)
            for item in out:
                output.append(item)
        return {
            "code": "200000",
            "data": {
                "time": timestamp,
                "results": output
            }
        }
    except HTTPException as e:
        return {
            "code": "500000",
            "message": e.detail
        }
    except Exception as e:
        return {
            "code": "500000",
            "message": f"An unexpected error occurred: {str(e)}"
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(PORT))
