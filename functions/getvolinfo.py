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