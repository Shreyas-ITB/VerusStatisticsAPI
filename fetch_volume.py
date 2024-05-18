import threading
import requests
import json
import time
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
RPCURL = os.environ.get("RPCURL")

def get_block_count():
    url = 'https://explorer.verus.io/api/getblockcount'
    response = requests.get(url)
    if response.status_code == 200:
        return int(response.text)
    else:
        print(f"Failed to retrieve block count. Status code: {response.status_code}")
        return None

def getcurrencystate(currency, height):
    payload = {
    'id': 1,
    'jsonrpc': '2.0',
    'method': 'getcurrencystate',
    'params': [currency, height]
    }
    response = requests.post(RPCURL, json=payload, timeout=10000).json()
    return response

arr_currencies = [
    {"currencyid": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV", "ticker": "VRSC"},
    {"currencyid": "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM", "ticker": "DAI.vETH"},
    {"currencyid": "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4", "ticker": "MKR.vETH"},
    {"currencyid": "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X", "ticker": "vETH"},
    {"currencyid": "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE", "ticker": "EURC.vETH"},
    {"currencyid": "i9oCSqKALwJtcv49xUKS2U2i79h1kX6NEY", "ticker": "USDT.vETH"},
    {"currencyid": "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd", "ticker": "USDC.vETH"},
    {"currencyid": "iHax5qYQGbcMGqJKKrPorpzUBX2oFFXGnY", "ticker": "PURE.vETH"},
    {"currencyid": "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU", "ticker": "tBTC.vETH"},
    {"currencyid": "iExBJfZYK7KREDpuhj6PzZBzqMAKaFg7d2", "ticker": "vARRR" },
    {"currencyid": "i3f7tSctFkiPpiedY8QR5Tep9p4qDVebDx", "ticker": "Bridge.vETH" },
    {"currencyid": "i4Xr5TAMrDTD99H69EemhjDxJ4ktNskUtc", "ticker": "Switch" }
]

def get_ticker_by_currency_id(currency_id):
    currency = next((item for item in arr_currencies if item["currencyid"] == currency_id), None)
    if currency:
        return currency["ticker"]
    return "Currency not found"

def aggregate_reserve_data(height, rangevalue, currency_name, currencies_data):
    prev_reserve_in = None
    prev_reserve_out = None
    print(f"Getting info for {currency_name}")
    
    # Track reserve data per block
    reserve_data_per_block = []

    for _ in range(rangevalue):
        response = getcurrencystate(currency_name, height)
        block_data = {}
        
        for currency_id, data in currencies_data.items():
            currency_info = response['result'][0]['currencystate']['currencies'][currency_id]
            reserve_in = currency_info['reservein']
            reserve_out = currency_info['reserveout']
            if reserve_in != prev_reserve_in or reserve_out != prev_reserve_out:
                data['total_reserve'] += reserve_in + reserve_out
                prev_reserve_in = reserve_in
                prev_reserve_out = reserve_out
            
            block_data[currency_id] = reserve_in + reserve_out

        reserve_data_per_block.append(block_data)
        height = str(int(height) - 1)
        print(f"Fetching stats for block {height}")
        time.sleep(0.2)
    
    return reserve_data_per_block

def update_reserve_data(height, numblocks, currency_name, currencies_data, reserve_data_per_block):
    prev_reserve_in = None
    prev_reserve_out = None
    print(f"Updating info for {currency_name}")

    new_reserve_data_per_block = []

    for _ in range(numblocks):
        response = getcurrencystate(currency_name, height)
        block_data = {}

        for currency_id, data in currencies_data.items():
            currency_info = response['result'][0]['currencystate']['currencies'][currency_id]
            reserve_in = currency_info['reservein']
            reserve_out = currency_info['reserveout']
            if reserve_in != prev_reserve_in or reserve_out != prev_reserve_out:
                data['total_reserve'] += reserve_in + reserve_out
                prev_reserve_in = reserve_in
                prev_reserve_out = reserve_out
            
            block_data[currency_id] = reserve_in + reserve_out

        new_reserve_data_per_block.append(block_data)
        height = str(int(height) - 1)
        print(f"Fetching stats for block {height}")
        time.sleep(0.2)

    # Remove the oldest blocks from the total reserve
    for old_block_data in reserve_data_per_block[:numblocks]:
        for currency_id, reserve in old_block_data.items():
            currencies_data[currency_id]['total_reserve'] -= reserve

    # Add the new blocks to the total reserve
    for new_block_data in new_reserve_data_per_block:
        for currency_id, reserve in new_block_data.items():
            currencies_data[currency_id]['total_reserve'] += reserve

    # Update the reserve data list
    reserve_data_per_block = reserve_data_per_block[numblocks:] + new_reserve_data_per_block

    return reserve_data_per_block

def save_to_json(data):
    with open('temp_data.json', 'w') as file:
        json.dump(data, file)

def add_to_json(new_data):
    with open('temp_data.json', 'r') as file:
        existing_data = json.load(file)
    
    for key, value in new_data.items():
        if key in existing_data:
            existing_data[key] += value
        else:
            existing_data[key] = value
    
    with open('temp_data.json', 'w') as file:
        json.dump(existing_data, file)

def merge_json_data(data1, data2, data3):
    merged_data = {}
    for key, value in data1.items():
        merged_data[key] = value
    for key, value in data2.items():
        merged_data[key] = value
    for key, value in data3.items():
        merged_data[key] = value
    return merged_data

def fetch_and_save_data():
    value = []
    height = get_block_count()
    value.append(height)
    print(f"Latest block height is: {height}")
    print(f"Block height saved to memory {value[0]}")
    print("")

    bridgeveth_currencies_data = {
        "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV": {"total_reserve": 0},
        "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X": {"total_reserve": 0},
        "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4": {"total_reserve": 0},
        "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM": {"total_reserve": 0}
    }

    switchbasket_currencies_data = {
        "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd": {"total_reserve": 0},
        "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE": {"total_reserve": 0},
    }

    purebasket_currencies_data = {
        "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU": {"total_reserve": 0},
    }

    if height is not None:
        reserve_data_per_block_bridgeveth = aggregate_reserve_data(str(value[0]), 1440, "Bridge.vETH", bridgeveth_currencies_data)
        reserve_data_per_block_switch = aggregate_reserve_data(str(value[0]), 1440, "Switch", switchbasket_currencies_data)
        reserve_data_per_block_pure = aggregate_reserve_data(str(value[0]), 1440, "Pure", purebasket_currencies_data)
        
        reservevolume1 = {get_ticker_by_currency_id(k): v['total_reserve'] for k, v in bridgeveth_currencies_data.items()}
        reservevolume2 = {get_ticker_by_currency_id(k): v['total_reserve'] for k, v in switchbasket_currencies_data.items()}
        reservevolume3 = {get_ticker_by_currency_id(k): v['total_reserve'] for k, v in purebasket_currencies_data.items()}

        bridgereserves = merge_json_data(reservevolume1, reservevolume2, reservevolume3)
        save_to_json(bridgereserves)
        print("Data saved to JSON file.")
    
    while True:
        print(f"Sleeping for 15 mins...")
        time.sleep(900)  # Sleep for 15 mins
        print("")
        currentheight = get_block_count()
        numblocks = int(currentheight) - int(value[0])
        value.append(currentheight)
        print(f"Latest block height is: {currentheight}")
        print(f"Block height saved to memory {value[-1]}")
        print("")
        print(f"During the period of 15 mins, {numblocks} blocks have been found.")
        print(f"Fetching stats for {numblocks} blocks")

        reserve_data_per_block_bridgeveth = update_reserve_data(str(currentheight), numblocks, "Bridge.vETH", bridgeveth_currencies_data, reserve_data_per_block_bridgeveth)
        reserve_data_per_block_switch = update_reserve_data(str(currentheight), numblocks, "Switch", switchbasket_currencies_data, reserve_data_per_block_switch)
        reserve_data_per_block_pure = update_reserve_data(str(currentheight), numblocks, "Pure", purebasket_currencies_data, reserve_data_per_block_pure)
        
        reservevolume1 = {get_ticker_by_currency_id(k): v['total_reserve'] for k, v in bridgeveth_currencies_data.items()}
        reservevolume2 = {get_ticker_by_currency_id(k): v['total_reserve'] for k, v in switchbasket_currencies_data.items()}
        reservevolume3 = {get_ticker_by_currency_id(k): v['total_reserve'] for k, v in purebasket_currencies_data.items()}
        
        newbridgereserves = merge_json_data(reservevolume1, reservevolume2, reservevolume3)
        add_to_json(newbridgereserves)
        print("Data saved to JSON file.")

def run():
    try:
        # Start a separate thread to periodically fetch and save data
        fetch_thread = threading.Thread(target=fetch_and_save_data)
        fetch_thread.start()
    except Exception as e:
        print(f"An Error occurred: {e}, trying after 60 seconds...")
        time.sleep(60)
        run()

run()
