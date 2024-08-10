from fastapi import FastAPI, HTTPException
import requests, time
import re
import numpy as np
from var.vars import RPCURL
from var.dict import arr_token_contracts, arr_token_holders
from functions.send_request import send_request
from functions.formatdifficulty import diff_format
from functions.aggregatereserves import getcurrencystate
from functions.decoderawtransaction import decode_rawtransaction
from functions.getrawtransaction import get_rawtransaction
from functions.latestblock import latest_block
from functions.formathashrate import formatHashrate
from functions.tickerfunc import get_ticker_by_currency_id, get_currencyid_by_ticker
from functions.getimports import get_imports, get_imports_with_blocks
from functions.calcreservebalance import calculate_reserve_balance
from functions.calctotalbalances import calculate_total_balances
from functions.getaddressbalance import get_address_balance
from functions.extracttransfers import extract_transfers
from functions.getallbaskets import getallbaskets
from functions.getcurrencyconverters import get_currencyconverters
from functions.getvrscreservesfrmbaskets import getvrscreserves_frombaskets
from functions.gettokenbalance import *
from functions.gettokenprice import *
from functions.getvolinfo import *
from functions.getcurrencyprices import *
from functions.getdaivalue import get_dai_value
from functions.getdefichain import getdefichain
from functions.getethbalance import get_eth_balance

app = FastAPI()

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
        "url": RPCURL,
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
        "url": RPCURL,
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
        "url": RPCURL,
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
        "url": RPCURL,
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
                        volume = pair['volume']
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
                # if currency == "ETH" or convertto == "ETH":
                #     # Reverse currency and convertto in the pair
                #     if currency == "Bridge.vETH" or convertto == "Bridge.vETH":
                #         currency_pair = f"Bridge.vETH-ETH" if currency == "Bridge.vETH" else f"{convertto}-ETH"
                #     else:
                #         currency_pair = f"{convertto}-{currency}"

                #     # Calculate weights based on volume
                #     weights = pair['volume'] / np.sum(pair['volume'])

                #     # Invert values if VRSC is the quote currency (second position)
                #     if convertto == "ETH":
                #         volume = pair['volume'] * 2
                #         last = np.dot(weights, 1 / pair['close']) / np.sum(weights)
                #         high = np.dot(weights, 1 / pair['high']) / np.sum(weights)
                #         low = np.dot(weights, 1 / pair['low']) / np.sum(weights)
                #         openn = np.dot(weights, 1 / pair['open']) / np.sum(weights)
                #     else:
                #         volume = pair['volume']
                #         last = np.dot(weights, pair['close']) / np.sum(weights)
                #         high = np.dot(weights, pair['high']) / np.sum(weights)
                #         low = np.dot(weights, pair['low']) / np.sum(weights)
                #         openn = np.dot(weights, pair['open']) / np.sum(weights)

                #     ticker_info.append({
                #         'symbol': currency_pair,
                #         'symbolName': currency_pair,
                #         'volume': volume,
                #         'last': last,
                #         'high': high,
                #         'low': low,
                #         'open': openn
                #     })
                # if currency == "DAI" or convertto == "DAI":
                #     # Reverse currency and convertto in the pair
                #     if currency == "Bridge.vETH" or convertto == "Bridge.vETH":
                #         currency_pair = f"Bridge.vETH-DAI" if currency == "Bridge.vETH" else f"{convertto}-DAI"
                #     else:
                #         currency_pair = f"{convertto}-{currency}"

                #     # Calculate weights based on volume
                #     weights = pair['volume'] / np.sum(pair['volume'])

                #     # Invert values if VRSC is the quote currency (second position)
                #     if convertto == "DAI":
                #         volume = pair['volume'] * 2
                #         last = np.dot(weights, 1 / pair['close']) / np.sum(weights)
                #         high = np.dot(weights, 1 / pair['high']) / np.sum(weights)
                #         low = np.dot(weights, 1 / pair['low']) / np.sum(weights)
                #         openn = np.dot(weights, 1 / pair['open']) / np.sum(weights)
                #     else:
                #         volume = pair['volume']
                #         last = np.dot(weights, pair['close']) / np.sum(weights)
                #         high = np.dot(weights, pair['high']) / np.sum(weights)
                #         low = np.dot(weights, pair['low']) / np.sum(weights)
                #         openn = np.dot(weights, pair['open']) / np.sum(weights)

                #     ticker_info.append({
                #         'symbol': currency_pair,
                #         'symbolName': currency_pair,
                #         'volume': volume,
                #         'last': last,
                #         'high': high,
                #         'low': low,
                #         'open': openn
                #     })

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
        if ticker['symbol'] == "VRSC-USDT":
            ticker['symbol'] = "USDT-VRSC"
            ticker['symbolName'] = "USDT-VRSC"
        if ticker['symbol'] == "VRSC-EURC":
            ticker['symbol'] = "EURC-VRSC"
            ticker['symbolName'] = "EURC-VRSC"
        if ticker['symbol'] == "VRSC-USDC":
            ticker['symbol'] = "USDC-VRSC"
            ticker['symbolName'] = "USDC-VRSC"
        if ticker['symbol'] == "VRSC-Kaiju":
            ticker['symbol'] = "Kaiju-VRSC"
            ticker['symbolName'] = "Kaiju-VRSC"
        if ticker['symbol'] == "VRSC-Switch":
            ticker['symbol'] = "Switch-VRSC"
            ticker['symbolName'] = "Switch-VRSC"
        if ticker['symbol'] == "tBTC-VRSC":
            ticker['symbol'] = "TBTC-VRSC"
            ticker['symbolName'] = "TBTC-VRSC"
        if ticker['symbol'] == "VRSC-whales":
            ticker['symbol'] = "whales-VRSC"
            ticker['symbolName'] = "whales-VRSC"
        # if ticker['symbol'] == "DAI-EURC":
        #     ticker['symbol'] = "EURC-DAI"
        #     ticker['symbolName'] = "EURC-DAI"
        # if ticker['symbol'] == "DAI-USDC":
        #     ticker['symbol'] = "USDC-DAI"
        #     ticker['symbolName'] = "USDC-DAI"

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
        pie_value = get_dai_value()
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