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
    {"currencyid": "iJczmut8fHgRvVxaNfEPm7SkgJLDFtPcrK", "ticker": "LINK.vETH"},
    {"currencyid": "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE", "ticker": "EURC.vETH"},
    {"currencyid": "iS3NjE3XRYWoHRoovpLhFnbDraCq7NFStf", "ticker": "WBTC.vETH"},
    {"currencyid": "i9oCSqKALwJtcv49xUKS2U2i79h1kX6NEY", "ticker": "USDT.vETH"},
    {"currencyid": "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd", "ticker": "USDC.vETH"},
    {"currencyid": "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU", "ticker": "PURE.vETH"},
    {"currencyid": "iEnQEjjozf1HZkqFT9U4NKnzz1iGZ7LbJ4", "ticker": "TRAC.vETH"},
    {"currencyid": "iNtUUdjsqV34snGZJerAvPLaojo6tV9sfd", "ticker": "MARS4.vETH"}
]

def get_ticker_by_currency_id(currency_id):
    currency = next((item for item in arr_currencies if item["currencyid"] == currency_id), None)
    if currency:
        return currency["ticker"]
    return "Currency not found"


# Previous code which doesn't check for the previous block values and adds all the values blindly
# def aggregate_reserve_data(height):
#     currencies_data = {
#         "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV": {"total_reserve": 0},
#         "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X": {"total_reserve": 0},
#         "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4": {"total_reserve": 0},
#         "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM": {"total_reserve": 0}
#     }
    
#     for _ in range(1440):
#         response = getcurrencystate("Bridge.vETH", height)
#         for currency_id, data in currencies_data.items():
#             currency_info = response['result'][0]['currencystate']['currencies'][currency_id]
#             data['total_reserve'] += currency_info['reservein'] + currency_info['reserveout']
#         height = str(int(height) - 1)
#         print(f"Fetching stats for block {height}")
    
#     # Fetch currency names and structure the result
#     result = {}
#     for currency_id, data in currencies_data.items():
#         currency_name = get_ticker_by_currency_id(currency_id)
#         result[currency_name] = data['total_reserve']
#     return result


# New code which checks if the next block contains the values of the previous block, if yes then it doesnt add that block values since its already added.
# Eliminates unnecessary additions to the volume values.
def aggregate_reserve_data_bridgeveth(height, rangevalue):
    bridgeveth_currencies_data = {
        "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV": {"total_reserve": 0},
        "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X": {"total_reserve": 0},
        "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4": {"total_reserve": 0},
        "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM": {"total_reserve": 0}
    }

    prev_reserve_in = None
    prev_reserve_out = None
    print("Getting info for Bridge.vETH")
    for _ in range(rangevalue):
        response = getcurrencystate("Bridge.vETH", height)
        for currency_id, data in bridgeveth_currencies_data.items():
            currency_info = response['result'][0]['currencystate']['currencies'][currency_id]
            reserve_in = currency_info['reservein']
            reserve_out = currency_info['reserveout']
            
            if reserve_in != prev_reserve_in or reserve_out != prev_reserve_out:
                data['total_reserve'] += reserve_in + reserve_out
                prev_reserve_in = reserve_in
                prev_reserve_out = reserve_out

        height = str(int(height) - 1)
        print(f"Fetching stats for block {height}")
        time.sleep(0.2)
    
    # Fetch currency names and structure the result
    result = {}
    for currency_id, data in bridgeveth_currencies_data.items():
        currency_name = get_ticker_by_currency_id(currency_id)
        result[currency_name] = data['total_reserve']

    return result

def aggregate_reserve_data_switch(height, rangevalue):
    switchbasket_currencies_data = {
        "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd": {"total_reserve": 0},
        "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE": {"total_reserve": 0},
    }

    prev_reserve_in = None
    prev_reserve_out = None
    print("Getting info for Switch")
    for _ in range(rangevalue):
        response = getcurrencystate("Switch", height)
        for currency_id, data in switchbasket_currencies_data.items():
            currency_info = response['result'][0]['currencystate']['currencies'][currency_id]
            reserve_in = currency_info['reservein']
            reserve_out = currency_info['reserveout']
            
            if reserve_in != prev_reserve_in or reserve_out != prev_reserve_out:
                data['total_reserve'] += reserve_in + reserve_out
                prev_reserve_in = reserve_in
                prev_reserve_out = reserve_out
            
        height = str(int(height) - 1)
        print(f"Fetching stats for block {height}")
        time.sleep(0.2)
    
    # Fetch currency names and structure the result
    result = {}
    for currency_id, data in switchbasket_currencies_data.items():
        currency_name = get_ticker_by_currency_id(currency_id)
        result[currency_name] = data['total_reserve']

    return result

def aggregate_reserve_data_pure(height, rangevalue):
    purebasket_currencies_data = {
        "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU": {"total_reserve": 0},
    }

    prev_reserve_in = None
    prev_reserve_out = None
    print("Getting info for Pure")
    for _ in range(rangevalue):
        response = getcurrencystate("Pure", height)
        for currency_id, data in purebasket_currencies_data.items():
            currency_info = response['result'][0]['currencystate']['currencies'][currency_id]
            reserve_in = currency_info['reservein']
            reserve_out = currency_info['reserveout']
            
            if reserve_in != prev_reserve_in or reserve_out != prev_reserve_out:
                data['total_reserve'] += reserve_in + reserve_out
                prev_reserve_in = reserve_in
                prev_reserve_out = reserve_out
            
        height = str(int(height) - 1)
        print(f"Fetching stats for block {height}")
        time.sleep(0.2)
    
    # Fetch currency names and structure the result
    result = {}
    for currency_id, data in purebasket_currencies_data.items():
        currency_name = get_ticker_by_currency_id(currency_id)
        result[currency_name] = data['total_reserve']
    
    return result

def save_to_json(data):
    with open('temp_data.json', 'w') as file:
        json.dump(data, file)

def add_to_json(new_data):
    with open('temp_data.json', 'r') as file:
        existing_data = json.load(file)
    merged_data = {key: existing_data.get(key, 0) + new_data.get(key, 0) for key in set(existing_data) | set(new_data)}
    with open('temp_data.json', 'w') as file:
        json.dump(merged_data, file)

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
    if height is not None:
        reservevolume1 = aggregate_reserve_data_bridgeveth(str(value[0]), 1440)
        print("Sleeping for 60 secs.... Trying to not rate-limit the API")
        time.sleep(60)
        print("")
        reservevolume2 = aggregate_reserve_data_switch(str(value[0]), 1440)
        print("Sleeping for 60 secs.... Trying to not rate-limit the API")
        time.sleep(60)
        print("")
        reservevolume3 = aggregate_reserve_data_pure(str(value[0]), 1440)
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
        print(f"Latest block height is: {height}")
        print(f"Block height saved to memory {value[0]}")
        print("")
        print(f"During the period of 30 mins, {numblocks} blocks have been found.")
        print(f"Fetching stats for {numblocks} blocks")
        newreservevolume1 = aggregate_reserve_data_bridgeveth(str(height), numblocks)
        print("Sleeping for 60 secs.... Trying to not rate-limit the API")
        time.sleep(60)
        print("")
        newreservevolume2 = aggregate_reserve_data_switch(str(height), numblocks)
        print("Sleeping for 60 secs.... Trying to not rate-limit the API")
        time.sleep(60)
        print("")
        newreservevolume3 = aggregate_reserve_data_pure(str(height), numblocks)
        newbridgereserves = merge_json_data(newreservevolume1, newreservevolume2, newreservevolume3)
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
