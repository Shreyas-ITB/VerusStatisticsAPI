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
from functions.markettickers import getmarkettickers
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
    ticker_infovrsc = []
    ticker_infoeth = []
    ticker_infodai = []
    excluded_pairs = ["DAI-VRSC", "VRSC-DAI", "DAI-ETH", "ETH-DAI", "VRSC-ETH", "ETH-VRSC"]
    final_ticker_infovrsc, final_ticker_infodai, final_ticker_infoeth = getmarkettickers(baskets, volblock, latestblock, ticker_infovrsc, ticker_infodai, ticker_infoeth, excluded_pairs)
    for ticker in final_ticker_infovrsc:
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

    for ticker in final_ticker_infodai:
        if ticker['symbol'] == "DAI-MKR":
            ticker['symbol'] = "MKR-DAI"
            ticker['symbolName'] = "MKR-DAI"
        if ticker['symbol'] == "DAI-USDT":
            ticker['symbol'] = "USDT-DAI"
            ticker['symbolName'] = "USDT-DAI"
        if ticker['symbol'] == "DAI-EURC":
            ticker['symbol'] = "EURC-DAI"
            ticker['symbolName'] = "EURC-DAI"
        if ticker['symbol'] == "DAI-ETH":
            ticker['symbol'] = "ETH-DAI"
            ticker['symbolName'] = "ETH-DAI"
        if ticker['symbol'] == "DAI-USDC":
            ticker['symbol'] = "USDC-DAI"
            ticker['symbolName'] = "USDC-DAI"
        if ticker['symbol'] == "DAI-Kaiju":
            ticker['symbol'] = "Kaiju-DAI"
            ticker['symbolName'] = "Kaiju-DAI"
        if ticker['symbol'] == "DAI-Switch":
            ticker['symbol'] = "Switch-DAI"
            ticker['symbolName'] = "Switch-DAI"
        if ticker['symbol'] == "tBTC-DAI":
            ticker['symbol'] = "TBTC-DAI"
            ticker['symbolName'] = "TBTC-DAI"
        if ticker['symbol'] == "DAI-whales":
            ticker['symbol'] = "whales-DAI"
            ticker['symbolName'] = "whales-DAI"

    for ticker in final_ticker_infoeth:
        if ticker['symbol'] == "ETH-MKR":
            ticker['symbol'] = "MKR-ETH"
            ticker['symbolName'] = "MKR-ETH"
        if ticker['symbol'] == "ETH-USDT":
            ticker['symbol'] = "USDT-ETH"
            ticker['symbolName'] = "USDT-ETH"
        if ticker['symbol'] == "ETH-EURC":
            ticker['symbol'] = "EURC-ETH"
            ticker['symbolName'] = "EURC-ETH"
        if ticker['symbol'] == "ETH-USDC":
            ticker['symbol'] = "USDC-ETH"
            ticker['symbolName'] = "USDC-ETH"
        if ticker['symbol'] == "ETH-Kaiju":
            ticker['symbol'] = "Kaiju-ETH"
            ticker['symbolName'] = "Kaiju-ETH"
        if ticker['symbol'] == "ETH-Switch":
            ticker['symbol'] = "Switch-ETH"
            ticker['symbolName'] = "Switch-ETH"
        if ticker['symbol'] == "tBTC-ETH":
            ticker['symbol'] = "TBTC-ETH"
            ticker['symbolName'] = "TBTC-ETH"
        if ticker['symbol'] == "ETH-whales":
            ticker['symbol'] = "whales-ETH"
            ticker['symbolName'] = "whales-ETH"
    
    final_ticker_info = final_ticker_infovrsc + final_ticker_infodai + final_ticker_infoeth
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
