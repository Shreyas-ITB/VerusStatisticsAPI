from functions.send_request import send_request
from var.vars import RPCURL

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