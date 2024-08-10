from functions.send_request import send_request
from var.vars import RPCURL

def latest_block():
    requestData = {
        "method": "post",
        "url": RPCURL,
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