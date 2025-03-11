from functions.send_request import send_request
from var.vars import RPCURL
from functions.getallbaskets import getallbaskets
from functions.latestblock import latest_block

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

def getcurrencyvolumeinfo_new(currency, fromblock, endblock, interval, volumecurrency, target_currency_id):
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
    if not isinstance(response, dict) or 'result' not in response or not isinstance(response['result'], list) or not response['result']:
        return None

    result_list = response['result']
    if not isinstance(result_list[0], dict) or 'currencystate' not in result_list[0] or not isinstance(result_list[0]['currencystate'], dict):
        return None

    currencystate = result_list[0]['currencystate']
    if 'reservecurrencies' not in currencystate or not isinstance(currencystate['reservecurrencies'], list):
        return None

    reserve_currencies = currencystate['reservecurrencies']

    for currency_info in reserve_currencies:
        if isinstance(currency_info, dict) and currency_info.get('currencyid') == target_currency_id:
            return currency_info.get('reserves')

    return None
