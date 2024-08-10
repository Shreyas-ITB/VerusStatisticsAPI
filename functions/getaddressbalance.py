from functions.send_request import send_request
from var.vars import RPCURL

def get_address_balance(address):
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getaddressbalance",
            "params": [{"addresses": [address]}],
            "id": 1
        }
    }
    response = send_request(**requestData)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve data"}