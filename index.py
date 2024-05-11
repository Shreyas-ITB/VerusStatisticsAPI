from flask import Flask, jsonify
import re
import requests, os
from dotenv import load_dotenv, find_dotenv
import json
import time
import threading

app = Flask(__name__)
load_dotenv(find_dotenv())
RPCURL = os.environ.get("RPCURL")
PORT = os.environ.get("APIPORT")

# Placeholder data
latestblock = []
reservecurrencies = []
mempool_res = []
rawtransaction = []
decodedrawtransaction = []
mempool_count = 0
res = []
arr_currencies = [
    {"currencyid": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV", "ticker": "VRSC"},
    {"currencyid": "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM", "ticker": "DAI.vETH"},
    {"currencyid": "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4", "ticker": "MKR.vETH"},
    {"currencyid": "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X", "ticker": "vETH"},
    {"currencyid": "iJczmut8fHgRvVxaNfEPm7SkgJLDFtPcrK", "ticker": "LINK.vETH"},
    {"currencyid": "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE", "ticker": "EURC.vETH"},
    {"currencyid": "iS3NjE3XRYWoHRoovpLhFnbDraCq7NFStf", "ticker": "WBTC.vETH"},
    {"currencyid": "i9oCSqKALwJtcv49xUKS2U2i79h1kX6NEY", "ticker": "USDT.vETH"},
    {"currencyid": "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU", "ticker": "Pure"},
    {"currencyid": "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd", "ticker": "USDC.vETH"},
    {"currencyid": "iEnQEjjozf1HZkqFT9U4NKnzz1iGZ7LbJ4", "ticker": "TRAC.vETH"},
    {"currencyid": "iNtUUdjsqV34snGZJerAvPLaojo6tV9sfd", "ticker": "MARS4.vETH"}
]

def send_request(method, url, headers, data):
    response = requests.request(method, url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

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

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve data"}
    
def get_imports_with_blocks(currency: str, fromblk: int, toblk: int):
    url = RPCURL

    json_data = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getimports",
        "params": [currency, fromblk, toblk]
    }

    response = requests.post(url, json=json_data)

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
        latestblock = response["result"]["blocks"]
        return jsonify(latestblock)
    except:
        return jsonify("Error!!, success: False")

def load_from_json():
    try:
        with open('temp_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Temporary JSON file not found.")
        return None

@app.route("/")
def main():    
    return jsonify(f"result: VerusCoin Multipurpose API running on port {PORT}, an API that knows everything about verus. Use it with responsibility and have fun building your project!!", "success: True")

@app.route('/price/<ticker>')
def price(ticker):
    resp = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids=verus-coin&vs_currencies={ticker}&include_24hr_change=true")
    return resp.json()

@app.route('/difficulty')
def difficulty():
    resp = requests.get("https://explorer.verus.io/api/getdifficulty")
    cleanresp = re.sub('"', '', resp.text)
    newresp = diff_format(float(cleanresp))
    return newresp

@app.route('/getcurrencystate/<currency>/<height>')
def routegetcurrencystate(currency, height):
    data = getcurrencystate(currency, height)
    return jsonify(data)

@app.route('/decoderawtransaction/<hex>', methods=['GET'])
def decode_rawtransaction_route(hex):
    data = decode_rawtransaction(hex)
    return jsonify(data)

@app.route('/getrawtransaction/<txid>', methods=['GET'])
def get_rawtransaction_route(txid):
    data = get_rawtransaction(txid)
    return jsonify(data)

@app.route('/blockcount', methods=['GET'])
def routelatest_block():
    data = latest_block()
    return data

@app.route('/getcurrencies/Bridge.vETH', methods=['GET'])
def getcurrenciesbridgeveth():
    reservecurrencies = get_bridge_currency_bridgeveth()
    return jsonify(reservecurrencies)

@app.route('/getcurrencies/RaceCondition', methods=['GET'])
def getcurrenciesracecondition():
    reservecurrencies = get_bridge_currency_racecondition()
    return jsonify(reservecurrencies)

@app.route('/getcurrencies/Switch', methods=['GET'])
def getcurrenciesswitch():
    reservecurrencies = get_bridge_currency_switch()
    return jsonify(reservecurrencies)

@app.route('/getcurrencies/Pure', methods=['GET'])
def getcurrenciespure():
    reservecurrencies = get_bridge_currency_pure()
    return jsonify(reservecurrencies)

@app.route('/dai_reserves', methods=['GET'])
def getdaireserves():
    daireserve = dai_reserves()
    return jsonify(daireserve)

@app.route('/vrsc_reserves', methods=['GET'])
def getvrscreserves():
    vrscreserve = vrsc_reserves()
    return jsonify(vrscreserve)

@app.route('/mkr_reserves', methods=['GET'])
def getmkrreserves():
    mkrreserve = mkr_reserves()
    return jsonify(mkrreserve)

@app.route('/eth_reserves', methods=['GET'])
def getethreserves():
    ethreserve = eth_reserves()
    return jsonify(ethreserve)

@app.route('/pure_reserves', methods=['GET'])
def getpurereserves():
    purereserve = pure_reserves()
    return jsonify(purereserve)

@app.route('/usdc_reserves', methods=['GET'])
def getusdcreserves():
    usdcreserve = usdc_reserves()
    return jsonify(usdcreserve)

@app.route('/eurc_reserves', methods=['GET'])
def geteurcreserves():
    eurcreserve = eurc_reserves()
    return jsonify(eurcreserve)

@app.route('/getticker/<currency_id>', methods=['GET'])
def get_ticker_route(currency_id):
    ticker = get_ticker_by_currency_id(currency_id)
    return jsonify({"ticker": ticker})

@app.route('/getcurrid/<ticker>', methods=['GET'])
def get_currid_route(ticker):
    currid = get_currencyid_by_ticker(ticker)
    return jsonify({"currencyid": currid})

@app.route('/getrawmempool', methods=['GET'])
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
        return jsonify({"error": str(error)})

    return jsonify({
        "mempool_res": mempool_res,
        "mempool_count": mempool_count,
    })

@app.route('/fetchblockhash/<longest_chain>', methods=['GET'])
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
        return jsonify({"error": str(error)})

    # In your actual implementation, you can replace the simulated response with the real block hash data.
    return jsonify({"block_hash": block_hash_data})

@app.route('/fetchtransactiondata/<transaction_id>', methods=['GET'])
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
        return jsonify({"error": str(error)})
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
        return jsonify({"error": str(error)})
    # In your actual implementation, you can replace the simulated responses with the real transaction data.
    return jsonify({"transaction_data": decoded_transaction_data})

@app.route('/getmoneysupply', methods=['GET'])
def getmoneysupply():
    resp = requests.get("https://explorer.verus.io/ext/getmoneysupply")
    return jsonify(resp.text, "success: True")

@app.route('/distribution', methods=['GET'])
def getdistribution():
    resp = requests.get("https://explorer.verus.io/ext/getdistribution")
    return resp.json()

@app.route('/getnethashpower', methods=['GET'])
def getnethashpower():
    resp = requests.get("https://insight.verus.io/api/getnetworkhashps")
    value = formatHashrate(int(resp.text))
    return jsonify(value, "success: True")

@app.route('/getweight_bridgeveth', methods=['GET'])
def getweightbridgeveth():
    resp = get_bridge_currency_bridgeveth()
    weights = [item['weight'] for item in resp]
    return jsonify({'weights': weights})

@app.route('/getweight_racecondition', methods=['GET'])
def getweightracecondition():
    resp = get_bridge_currency_racecondition()
    weights = [item['weight'] for item in resp]
    return jsonify({'weights': weights})

@app.route('/getweight_switch', methods=['GET'])
def getweightswitch():
    resp = get_bridge_currency_switch()
    weights = [item['weight'] for item in resp]
    return jsonify({'weights': weights})

@app.route('/getweight_pure', methods=['GET'])
def getweightpure():
    resp = get_bridge_currency_pure()
    weights = [item['weight'] for item in resp]
    return jsonify({'weights': weights})

@app.route('/getbridgedaiprice', methods=['GET'])
def getbridgedaireserveprice():
    reservecurrencies = get_bridge_currency_bridgeveth()
    dai = next((item for item in reservecurrencies if item["currencyid"] == "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM"), None)
    if dai:
        return jsonify(dai["priceinreserve"], "success: True")
    return None

@app.route('/getbridgevrscprice', methods=['GET'])
def getbridgevrscreserveprice():
    reservecurrencies = get_bridge_currency_bridgeveth()
    vrsc = next((item for item in reservecurrencies if item["currencyid"] == "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"), None)
    if vrsc:
        return jsonify(vrsc["priceinreserve"], "success: True")
    return None

@app.route('/getbridgemkrprice', methods=['GET'])
def getbridgemkrreserveprice():
    reservecurrencies = get_bridge_currency_bridgeveth()
    mkr = next((item for item in reservecurrencies if item["currencyid"] == "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4"), None)
    if mkr:
        return jsonify(mkr["priceinreserve"], "success: True")
    return None

@app.route('/getbridgeethprice', methods=['GET'])
def getbridgeethreserveprice():
    reservecurrencies = get_bridge_currency_bridgeveth()
    eth = next((item for item in reservecurrencies if item["currencyid"] == "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X"), None)
    if eth:
        return jsonify(eth["priceinreserve"], "success: True")
    return None

@app.route('/getbridgepureprice', methods=['GET'])
def getbridgepurereserveprice():
    reservecurrencies = get_bridge_currency_pure()
    dai = next((item for item in reservecurrencies if item["currencyid"] == "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU"), None)
    if dai:
        return jsonify(dai["priceinreserve"], "success: True")
    return None

@app.route('/getbridgeusdcprice', methods=['GET'])
def getbridgeusdcreserveprice():
    reservecurrencies = get_bridge_currency_switch()
    dai = next((item for item in reservecurrencies if item["currencyid"] == "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd"), None)
    if dai:
        return jsonify(dai["priceinreserve"], "success: True")
    return None

@app.route('/getbridgeeurcprice', methods=['GET'])
def getbridgeeurcreserveprice():
    reservecurrencies = get_bridge_currency_switch()
    dai = next((item for item in reservecurrencies if item["currencyid"] == "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE"), None)
    if dai:
        return jsonify(dai["priceinreserve"], "success: True")
    return None

@app.route('/getdaiveth_daireserveprice', methods=['GET'])
def getdaivethdaireserveprice():
    reserves = dai_reserves()
    resp = get_reserve_dai_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getvrsc_daireserveprice', methods=['GET'])
def getvrscdaireserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_dai_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getmkrveth_daireserveprice', methods=['GET'])
def getmkrvethdaireserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_dai_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getveth_daireserveprice', methods=['GET'])
def getvethdaireserveprice():
    reserves = eth_reserves()
    resp = get_reserve_dai_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getpure_daireserveprice', methods=['GET'])
def getpuredaireserveprice():
    reserves = pure_reserves()
    resp = get_reserve_dai_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getusdc_daireserveprice', methods=['GET'])
def getusdcdaireserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_dai_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/geteurc_daireserveprice', methods=['GET'])
def geteurcdaireserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_dai_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getdaiveth_vrscreserveprice', methods=['GET'])
def getdaivethvrscreserveprice():
    reserves = dai_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getvrsc_vrscreserveprice', methods=['GET'])
def getvrscvrscreserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getmkrveth_vrscreserveprice', methods=['GET'])
def getmkrvethvrscreserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getveth_vrscreserveprice', methods=['GET'])
def getvethvrscreserveprice():
    reserves = eth_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getpure_vrscreserveprice', methods=['GET'])
def getpurevrscreserveprice():
    reserves = pure_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getusdc_vrscreserveprice', methods=['GET'])
def getusdcvrscreserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/geteurc_vrscreserveprice', methods=['GET'])
def geteurcvrscreserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getdaiveth_mkrreserveprice', methods=['GET'])
def getdaivethmkrreserveprice():
    reserves = dai_reserves()
    resp = get_reserve_mkr_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getvrsc_mkrreserveprice', methods=['GET'])
def getvrscmkrreserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_mkr_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getmkrveth_mkrreserveprice', methods=['GET'])
def getmkrvethmkrreserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_mkr_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getveth_mkrreserveprice', methods=['GET'])
def getvethmkrreserveprice():
    reserves = eth_reserves()
    resp = get_reserve_mkr_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getpure_mkrreserveprice', methods=['GET'])
def getpuremkrreserveprice():
    reserves = pure_reserves()
    resp = get_reserve_mkr_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getusdc_mkrreserveprice', methods=['GET'])
def getusdcmkrreserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_mkr_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/geteurc_mkrreserveprice', methods=['GET'])
def geteurcmkrreserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_mkr_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getdaiveth_vethreserveprice', methods=['GET'])
def getdaivethvethreserveprice():
    reserves = dai_reserves()
    resp = get_reserve_eth_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getvrsc_vethreserveprice', methods=['GET'])
def getvrscvethreserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_eth_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getmkrveth_vethreserveprice', methods=['GET'])
def getmkrvethvethreserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_eth_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getveth_vethreserveprice', methods=['GET'])
def getvethvethreserveprice():
    reserves = eth_reserves()
    resp = get_reserve_eth_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getpure_vethreserveprice', methods=['GET'])
def getpurevethreserveprice():
    reserves = pure_reserves()
    resp = get_reserve_eth_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getusdc_vethreserveprice', methods=['GET'])
def getusdcvethreserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_eth_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/geteurc_vethreserveprice', methods=['GET'])
def geteurcvethreserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_eth_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getdaiveth_purereserveprice', methods=['GET'])
def getdaivethpurereserveprice():
    reserves = dai_reserves()
    resp = get_reserve_pure_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getvrsc_purereserveprice', methods=['GET'])
def getvrscpurereserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_pure_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getmkrveth_purereserveprice', methods=['GET'])
def getmkrvethpurereserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_pure_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getveth_purereserveprice', methods=['GET'])
def getvethpurereserveprice():
    reserves = eth_reserves()
    resp = get_reserve_pure_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getpure_purereserveprice', methods=['GET'])
def getpurepurereserveprice():
    reserves = pure_reserves()
    resp = get_reserve_pure_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getusdc_purereserveprice', methods=['GET'])
def getusdcpurereserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_pure_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/geteurc_purereserveprice', methods=['GET'])
def geteurcpurereserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_pure_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getdaiveth_usdcreserveprice', methods=['GET'])
def getdaivethusdcreserveprice():
    reserves = dai_reserves()
    resp = get_reserve_usdc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getvrsc_usdcreserveprice', methods=['GET'])
def getvrscusdcreserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_usdc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getmkrveth_usdcreserveprice', methods=['GET'])
def getmkrvethusdcreserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_usdc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getveth_usdcreserveprice', methods=['GET'])
def getvethusdcreserveprice():
    reserves = eth_reserves()
    resp = get_reserve_usdc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getpure_usdcreserveprice', methods=['GET'])
def getpureusdcreserveprice():
    reserves = pure_reserves()
    resp = get_reserve_usdc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getusdc_usdcreserveprice', methods=['GET'])
def getusdcusdcreserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_usdc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/geteurc_usdcreserveprice', methods=['GET'])
def geteurcusdcreserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_usdc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getdaiveth_eurcreserveprice', methods=['GET'])
def getdaivetheurcreserveprice():
    reserves = dai_reserves()
    resp = get_reserve_eurc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getvrsc_eurcreserveprice', methods=['GET'])
def getvrsceurcreserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_eurc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getmkrveth_eurcreserveprice', methods=['GET'])
def getmkrvetheurcreserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_eurc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getveth_eurcreserveprice', methods=['GET'])
def getvetheurcreserveprice():
    reserves = eth_reserves()
    resp = get_reserve_eurc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getpure_eurcreserveprice', methods=['GET'])
def getpureeurcreserveprice():
    reserves = pure_reserves()
    resp = get_reserve_eurc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getusdc_eurcreserveprice', methods=['GET'])
def getusdceurcreserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_eurc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/geteurc_eurcreserveprice', methods=['GET'])
def geteurceurcreserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_eurc_price(reserves)
    return jsonify(resp, "success: True")

@app.route('/getimports/<currency>/', methods=['GET'])
def routegetimports(currency: str):
    # newfromblk = int(fromblk)
    # newtoblk = int(toblk)
    newcurrency = str(currency)
    response = get_imports(newcurrency)
    return jsonify(response)

@app.route('/getimports_blk/<currency>/<fromblk>/<toblk>/', methods=['GET'])
def routegetimports_blk(currency: str, fromblk: int, toblk: int):
    newfromblk = int(fromblk)
    newtoblk = int(toblk)
    newcurrency = str(currency)
    response = get_imports_with_blocks(newcurrency, newfromblk, newtoblk)
    return jsonify(response)

@app.route('/getvolume/<currencyid>/<currency>/<fromblk>/<toblk>')
def routegetvolume(currencyid: str, currency: str, fromblk: int, toblk: int):
    newfromblk = int(fromblk)
    newtoblk = int(toblk)
    newcurrency = str(currency)
    newcurrencyid = str(currencyid)
    response = calculate_reserve_balance(newcurrencyid, newcurrency, newfromblk, newtoblk)
    return jsonify(response, "success: True")

@app.route('/gettotalvolume/<currency>/<fromblk>/<toblk>')
def routegettotalvolume(currency: str, fromblk: int, toblk: int):
    newfromblk = int(fromblk)
    newtoblk = int(toblk)
    newcurrency = str(currency)
    response = calculate_total_balances(newcurrency, newfromblk, newtoblk)
    return jsonify(response, "success: True")

@app.route('/gettransactions/<currency>/<fromblk>/<toblk>', methods=['GET'])
def routegettxns(currency: str, fromblk: int, toblk: int):
    newfromblk = int(fromblk)
    newtoblk = int(toblk)
    newcurrency = str(currency)
    response = extract_transfers(newcurrency, newfromblk, newtoblk)
    return jsonify(response)

@app.route('/market/allTickers/', methods=['GET'])
def routegetvrscdai():
    url = 'https://explorer.verus.io/api/getblockcount'
    height = requests.get(url).text
    reserves = dai_reserves()
    newreserves = vrsc_reserves()
    mkrreserves = mkr_reserves()
    ethreserves = eth_reserves()
    usdcreserves = usdc_reserves()
    eurcreserves = eurc_reserves()
    purereserves = pure_reserves()
    ethprice = get_reserve_eth_price(ethreserves)
    mkrprice = get_reserve_mkr_price(mkrreserves)
    vrscprice = get_reserve_vrsc_price(newreserves)
    daiprice = get_reserve_dai_price(reserves)
    usdcprice = get_reserve_usdc_price(usdcreserves)
    eurcprice = get_reserve_eurc_price(eurcreserves)
    pureprice = get_reserve_pure_price(purereserves)
    bridgevethreservecurrencies = get_bridge_currency_bridgeveth()
    raceconditionreservecurrencies = get_bridge_currency_racecondition()
    purebasketreservecurrencies = get_bridge_currency_pure()
    switchbasketreservecurrencies = get_bridge_currency_switch()
    vrsc = next((item for item in bridgevethreservecurrencies if item["currencyid"] == "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"), None)
    VRSCBridgeReservePrice = vrsc['priceinreserve']
    dai = next((item for item in bridgevethreservecurrencies if item["currencyid"] == "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM"), None)
    DAIBridgeReservePrice = dai['priceinreserve']
    mkr = next((item for item in bridgevethreservecurrencies if item["currencyid"] == "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4"), None)
    MKRBridgeReservePrice = mkr['priceinreserve']
    eth = next((item for item in bridgevethreservecurrencies if item["currencyid"] == "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X"), None)
    ETHBridgeReservePrice = eth['priceinreserve']
    pure = next((item for item in purebasketreservecurrencies if item["currencyid"] == "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU"), None)
    PUREBridgeReservePrice = pure['priceinreserve']
    usdc = next((item for item in switchbasketreservecurrencies if item["currencyid"] == "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd"), None)
    usdcBridgeReservePrice = usdc['priceinreserve']
    eurc = next((item for item in switchbasketreservecurrencies if item["currencyid"] == "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE"), None)
    EURCBridgeReservePrice = eurc['priceinreserve']
    
    ETHDAITotalBridgePrice = ETHBridgeReservePrice + DAIBridgeReservePrice
    ETHDAITotalPrice = ethprice + daiprice
    ETHMKRTotalBridgePrice = ETHBridgeReservePrice + MKRBridgeReservePrice
    ETHMKRTotalPrice = ethprice + mkrprice
    ETHVRSCTotalBridgePrice = ETHBridgeReservePrice + VRSCBridgeReservePrice
    ETHVRSCTotalPrice = ethprice + vrscprice
    ETHPURETotalBridgePrice = ETHBridgeReservePrice + PUREBridgeReservePrice
    ETHPURETotalPrice = ethprice + pureprice
    ETHTBTTCTotalBridgePrice = ETHBridgeReservePrice + usdcBridgeReservePrice
    ETHTBTTCTotalPrice = ethprice + usdcprice
    ETHEURCTotalBridgePrice = ETHBridgeReservePrice + EURCBridgeReservePrice
    ETHEURCTotalPrice = ethprice + eurcprice
    MKRDAITotalBridgePrice = MKRBridgeReservePrice + DAIBridgeReservePrice
    MKRDAITotalPrice = mkrprice + daiprice
    MKRVRSCTotalBridgePrice = MKRBridgeReservePrice + VRSCBridgeReservePrice
    MKRVRSCTotalPrice = mkrprice + vrscprice
    MKRETHTotalBridgePrice = MKRBridgeReservePrice + ETHBridgeReservePrice
    MKRETHTotalPrice = mkrprice + ethprice
    MKRPURETotalBridgePrice = MKRBridgeReservePrice + PUREBridgeReservePrice
    MKRPURETotalPrice = mkrprice + pureprice
    MKRTBTTCTotalBridgePrice = MKRBridgeReservePrice + usdcBridgeReservePrice
    MKRTBTTCTotalPrice = mkrprice + usdcprice
    MKREURCTotalBridgePrice = MKRBridgeReservePrice + EURCBridgeReservePrice
    MKREURCTotalPrice = mkrprice + eurcprice
    DAIVRSCTotalBridgePrice = DAIBridgeReservePrice + VRSCBridgeReservePrice
    DAIVRSCTotalPrice = daiprice + vrscprice
    DAIMKRTotalBridgePrice = DAIBridgeReservePrice + MKRBridgeReservePrice
    DAIMKRTotalPrice = daiprice + mkrprice
    DAIETHTotalBridgePrice = DAIBridgeReservePrice + ETHBridgeReservePrice
    DAIETHTotalPrice = daiprice + ethprice
    DAIPURETotalBridgePrice = DAIBridgeReservePrice + PUREBridgeReservePrice
    DAIPURETotalPrice = daiprice + pureprice
    DAITBTTCTotalBridgePrice = DAIBridgeReservePrice + usdcBridgeReservePrice
    DAITBTTCTotalPrice = daiprice + usdcprice
    DAIEURCTotalBridgePrice = DAIBridgeReservePrice + EURCBridgeReservePrice
    DAIEURCTotalPrice = daiprice + eurcprice
    VRSCDAITotalBridgePrice = VRSCBridgeReservePrice + DAIBridgeReservePrice
    VRSCDAITotalPrice = vrscprice + daiprice
    VRSCMKRTotalBridgePrice = VRSCBridgeReservePrice + MKRBridgeReservePrice
    VRSCMKRTotalPrice = vrscprice + mkrprice
    VRSCETHTotalBridgePrice = VRSCBridgeReservePrice + ETHBridgeReservePrice
    VRSCETHTotalPrice = vrscprice + ethprice
    VRSCPURETotalBridgePrice = VRSCBridgeReservePrice + PUREBridgeReservePrice
    VRSCPURETotalPrice = vrscprice + pureprice
    VRSCTBTTCTotalBridgePrice = VRSCBridgeReservePrice + usdcBridgeReservePrice
    VRSCTBTTCTotalPrice = vrscprice + usdcprice
    VRSCEURCTotalBridgePrice = VRSCBridgeReservePrice + EURCBridgeReservePrice
    VRSCEURCTotalPrice = vrscprice + eurcprice
    bridgevethbalances = calculate_total_balances("Bridge.vETH")
    raceconditionbalances = calculate_total_balances("RaceCondition")
    purebasketbalances = calculate_total_balances("Pure")
    switchbasketbalances = calculate_total_balances("Switch")
    bidgevolume = load_from_json()
    VRSC = bidgevolume["VRSC"]
    vETH = bidgevolume["vETH"]
    MKRvETH = bidgevolume["MKR.vETH"]
    DAIvETH = bidgevolume["DAI.vETH"]
    usdcvETH = bidgevolume["USDC.vETH"]
    EURCvETH = bidgevolume["EURC.vETH"]
    PUREvETH = bidgevolume["PURE.vETH"]
    response = [
        {
            "symbol": "VRSC-DAI",
            "symbolName": "VRSC-DAI",
            "DAIPrice": daiprice, 
            "VRSCPrice": vrscprice,
            "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * daiprice} DAI",
            "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * daiprice} DAI",
            "TotalBridgePrice": f"{VRSCDAITotalBridgePrice * daiprice} DAI",
            "TotalPrice": f"{VRSCDAITotalPrice * daiprice} DAI",
            "PairVolume": f"{VRSC + DAIvETH} DAI"
        },
        {
            "symbol": "VRSC-MKR",
            "symbolName": "VRSC-MKR",
            "MKRPrice": mkrprice,
            "VRSCPrice": vrscprice,
            "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * mkrprice} MKR",
            "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * mkrprice} MKR",
            "TotalBridgePrice": f"{VRSCMKRTotalBridgePrice * mkrprice} MKR",
            "TotalPrice": f"{VRSCMKRTotalPrice * mkrprice} MKR",
            "PairVolume": f"{VRSC + MKRvETH * mkrprice} MKR"

        },
        {
            "symbol": "VRSC-ETH",
            "symbolName": "VRSC-ETH",
            "ETHPrice": ethprice,
            "VRSCPrice": vrscprice,
            "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * ethprice} ETH",
            "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * ethprice} ETH",
            "TotalBridgePrice": f"{VRSCETHTotalBridgePrice * ethprice} ETH",
            "TotalPrice": f"{VRSCETHTotalPrice * ethprice} ETH",
            "PairVolume": f"{VRSC + vETH * ethprice} ETH"
        },
        {
            "symbol": "VRSC-PURE",
            "symbolName": "VRSC-PURE",
            "PUREPrice": pureprice,
            "VRSCPrice": vrscprice,
            "PUREBridgeReservePrice": f"{PUREBridgeReservePrice * pureprice} PURE",
            "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * pureprice} PURE",
            "TotalBridgePrice": f"{VRSCPURETotalBridgePrice * pureprice} PURE",
            "TotalPrice": f"{VRSCPURETotalPrice * pureprice} PURE",
            "PairVolume": f"{VRSC + PUREvETH * pureprice} PURE"
        },
        {
            "symbol": "VRSC-USDC",
            "symbolName": "VRSC-USDC",
            "usdcPrice": usdcprice,
            "VRSCPrice": vrscprice,
            "usdcBridgeReservePrice": f"{usdcBridgeReservePrice * usdcprice} USDC",
            "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * usdcprice} USDC",
            "TotalBridgePrice": f"{VRSCTBTTCTotalBridgePrice * usdcprice} USDC",
            "TotalPrice": f"{VRSCTBTTCTotalPrice * usdcprice} USDC",
            "PairVolume": f"{VRSC + usdcvETH * usdcprice} USDC"
        },
        {
            "symbol": "VRSC-EURC",
            "symbolName": "VRSC-EURC",
            "EURCPrice": eurcprice,
            "VRSCPrice": vrscprice,
            "EURCBridgeReservePrice": f"{EURCBridgeReservePrice * eurcprice} EURC",
            "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * eurcprice} EURC",
            "TotalBridgePrice": f"{VRSCEURCTotalBridgePrice * eurcprice} EURC",
            "TotalPrice": f"{VRSCEURCTotalPrice * eurcprice} EURC",
            "PairVolume": f"{VRSC + EURCvETH * eurcprice} EURC"
        },
        {
            "symbol": "ETH-DAI",
            "symbolName": "ETH-DAI",
            "DAIPrice": daiprice,
            "ETHPrice": ethprice,
            "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * daiprice} DAI",
            "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * daiprice} DAI",
            "TotalBridgePrice": f"{ETHDAITotalBridgePrice * daiprice} DAI",
            "TotalPrice": f"{ETHDAITotalPrice * daiprice} DAI",
            "PairVolume": f"{vETH + DAIvETH} DAI"
        },
        {
            "symbol": "ETH-MKR",
            "symbolName": "ETH-MKR",
            "MKRPrice": mkrprice,
            "ETHPrice": ethprice,
            "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * mkrprice} MKR",
            "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * mkrprice} MKR",
            "TotalBridgePrice": f"{ETHMKRTotalBridgePrice * mkrprice} MKR",
            "TotalPrice": f"{ETHMKRTotalPrice * mkrprice} MKR",
            "PairVolume": f"{vETH + MKRvETH * mkrprice} MKR"
        },
        {
            "symbol": "ETH-VRSC",
            "symbolName": "ETH-VRSC",
            "VRSCPrice": vrscprice,
            "ETHPrice": ethprice,
            "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * vrscprice} VRSC",
            "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * vrscprice} VRSC",
            "TotalBridgePrice": f"{ETHVRSCTotalBridgePrice * vrscprice} VRSC",
            "TotalPrice": f"{ETHVRSCTotalPrice * vrscprice} VRSC",
            "PairVolume": f"{vETH + VRSC * vrscprice} VRSC"
        },
        {
            "symbol": "ETH-PURE",
            "symbolName": "ETH-PURE",
            "PUREPrice": pureprice,
            "ETHPrice": ethprice,
            "PUREBridgeReservePrice": f"{PUREBridgeReservePrice * pureprice} PURE",
            "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * pureprice} PURE",
            "TotalBridgePrice": f"{ETHPURETotalBridgePrice * pureprice} PURE",
            "TotalPrice": f"{ETHPURETotalPrice * pureprice} PURE",
            "PairVolume": f"{vETH + PUREvETH * pureprice} PURE"
        },
        {
            "symbol": "ETH-USDC",
            "symbolName": "ETH-USDC",
            "usdcPrice": usdcprice,
            "ETHPrice": ethprice,
            "usdcBridgeReservePrice": f"{usdcBridgeReservePrice * usdcprice} USDC",
            "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * usdcprice} USDC",
            "TotalBridgePrice": f"{ETHTBTTCTotalBridgePrice * usdcprice} USDC",
            "TotalPrice": f"{ETHTBTTCTotalPrice * usdcprice} USDC",
            "PairVolume": f"{vETH + usdcvETH * usdcprice} USDC"
        },
        {
            "symbol": "ETH-EURC",
            "symbolName": "ETH-EURC",
            "EURCPrice": eurcprice,
            "ETHPrice": ethprice,
            "EURCBridgeReservePrice": f"{EURCBridgeReservePrice * eurcprice} EURC",
            "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * eurcprice} EURC",
            "TotalBridgePrice": f"{ETHEURCTotalBridgePrice * eurcprice} EURC",
            "TotalPrice": f"{ETHEURCTotalPrice * eurcprice} EURC",
            "PairVolume": f"{vETH + EURCvETH * eurcprice} EURC"
        },
        {
            "symbol": "DAI-MKR",
            "symbolName": "DAI-MKR",
            "DAIPrice": daiprice,
            "MKRPrice": mkrprice,
            "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * mkrprice} MKR",
            "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * mkrprice} MKR",
            "TotalBridgePrice": F"{DAIMKRTotalBridgePrice * mkrprice} MKR",
            "TotalPrice": F"{DAIMKRTotalPrice * mkrprice} MKR",
            "PairVolume": f"{DAIvETH + MKRvETH * mkrprice} MKR"
        },
        {
            "symbol": "DAI-ETH",
            "symbolName": "DAI-ETH",
            "DAIPrice": daiprice,
            "ETHPrice": ethprice,
            "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * ethprice} ETH",
            "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * ethprice} ETH",
            "TotalBridgePrice": f"{DAIETHTotalBridgePrice * ethprice} ETH",
            "TotalPrice": f"{DAIETHTotalPrice * ethprice} ETH",
            "PairVolume": f"{DAIvETH + vETH * ethprice} ETH"

        },
        {
            "symbol": "DAI-VRSC",
            "symbolName": "DAI-VRSC",
            "DAIPrice": daiprice,
            "VRSCPrice": vrscprice,
            "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * vrscprice} VRSC",
            "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * vrscprice} VRSC",
            "TotalBridgePrice": f"{DAIVRSCTotalBridgePrice * vrscprice} VRSC",
            "TotalPrice": f"{DAIVRSCTotalPrice * vrscprice} VRSC",
            "PairVolume": f"{DAIvETH + VRSC * vrscprice} VRSC"
        },
        {
            "symbol": "DAI-PURE",
            "symbolName": "DAI-PURE",
            "DAIPrice": daiprice,
            "PUREPrice": pureprice,
            "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * pureprice} PURE",
            "PUREBridgeReservePrice": f"{PUREBridgeReservePrice * pureprice} PURE",
            "TotalBridgePrice": f"{DAIPURETotalBridgePrice * pureprice} PURE",
            "TotalPrice": f"{DAIPURETotalPrice * pureprice} PURE",
            "PairVolume": f"{DAIvETH + PUREvETH * pureprice} PURE"
        },
        {
            "symbol": "DAI-USDC",
            "symbolName": "DAI-USDC",
            "DAIPrice": daiprice,
            "usdcPrice": usdcprice,
            "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * usdcprice} USDC",
            "usdcBridgeReservePrice": f"{usdcBridgeReservePrice * usdcprice} USDC",
            "TotalBridgePrice": f"{DAITBTTCTotalBridgePrice * usdcprice} USDC",
            "TotalPrice": f"{DAITBTTCTotalPrice * usdcprice} USDC",
            "PairVolume": f"{DAIvETH + usdcvETH * usdcprice} USDC"
        },
        {
            "symbol": "DAI-EURC",
            "symbolName": "DAI-EURC",
            "DAIPrice": daiprice,
            "EURCPrice": eurcprice,
            "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * eurcprice} EURC",
            "EURCBridgeReservePrice": f"{EURCBridgeReservePrice * eurcprice} EURC",
            "TotalBridgePrice": f"{DAIEURCTotalBridgePrice * eurcprice} EURC",
            "TotalPrice": f"{DAIEURCTotalPrice * eurcprice} EURC",
            "PairVolume": f"{DAIvETH + EURCvETH * eurcprice} EURC"
        },
        {
            "symbol": "MKR-ETH",
            "symbolName": "MKR-ETH",
            "MKRPrice": mkrprice,
            "ETHPrice": ethprice,
            "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * ethprice} ETH",
            "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * ethprice} ETH",
            "TotalBridgePrice": f"{MKRETHTotalBridgePrice * ethprice} ETH",
            "TotalPrice": f"{MKRETHTotalPrice * ethprice} ETH",
            "PairVolume": f"{MKRvETH + vETH * ethprice} ETH"
        },
        {
            "symbol": "MKR-VRSC",
            "symbolName": "MKR-VRSC",
            "MKRPrice": mkrprice,
            "VRSCPrice": vrscprice,
            "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * vrscprice} VRSC",
            "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * vrscprice} VRSC",
            "TotalBridgePrice": f"{MKRVRSCTotalBridgePrice * vrscprice} VRSC",
            "TotalPrice": f"{MKRVRSCTotalPrice * vrscprice} VRSC",
            "PairVolume": f"{MKRvETH + VRSC * vrscprice} VRSC"
        },
        {
            "symbol": "MKR-DAI",
            "symbolName": "MKR-DAI",
            "DAIPrice": daiprice,
            "MKRPrice": mkrprice,
            "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * mkrprice} MKR",
            "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * mkrprice} MKR",
            "TotalBridgePrice": f"{MKRDAITotalBridgePrice * mkrprice} MKR",
            "TotalPrice": f"{MKRDAITotalPrice * mkrprice} MKR",
            "PairVolume": f"{MKRvETH + DAIvETH * mkrprice} MKR"
        },
        {
            "symbol": "MKR-PURE",
            "symbolName": "MKR-PURE",
            "PUREPrice": pureprice,
            "MKRPrice": mkrprice,
            "PUREBridgeReservePrice": f"{PUREBridgeReservePrice * mkrprice} MKR",
            "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * mkrprice} MKR",
            "TotalBridgePrice": f"{MKRPURETotalBridgePrice * mkrprice} MKR",
            "TotalPrice": f"{MKRPURETotalPrice * mkrprice} MKR",
            "PairVolume": f"{MKRvETH + PUREvETH * mkrprice} MKR"
        },
        {
            "symbol": "MKR-USDC",
            "symbolName": "MKR-USDC",
            "usdcPrice": usdcprice,
            "MKRPrice": mkrprice,
            "usdcBridgeReservePrice": f"{usdcBridgeReservePrice * mkrprice} MKR",
            "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * mkrprice} MKR",
            "TotalBridgePrice": f"{MKRTBTTCTotalBridgePrice * mkrprice} MKR",
            "TotalPrice": f"{MKRTBTTCTotalPrice * mkrprice} MKR",
            "PairVolume": f"{MKRvETH + usdcvETH * mkrprice} MKR"
        },
        {
            "symbol": "MKR-EURC",
            "symbolName": "MKR-EURC",
            "EURCPrice": eurcprice,
            "MKRPrice": mkrprice,
            "EURCBridgeReservePrice": f"{EURCBridgeReservePrice * mkrprice} MKR",
            "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * mkrprice} MKR",
            "TotalBridgePrice": f"{MKREURCTotalBridgePrice * mkrprice} MKR",
            "TotalPrice": f"{MKREURCTotalPrice * mkrprice} MKR",
            "PairVolume": f"{MKRvETH + EURCvETH * mkrprice} MKR"
        },
    {"Total Bridge Balances": [
        {"Bridge.vETH": bridgevethbalances},
        {"PureBasket": purebasketbalances},
        {"SwitchBasket": switchbasketbalances}
    ]},
    {"24hr Currency Volume": bidgevolume},
    ]
    return jsonify(response, "success: True")

if __name__ == '__main__':
    app.run(debug=True)
