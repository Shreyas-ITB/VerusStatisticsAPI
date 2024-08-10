from functions.send_request import send_request
from var.vars import RPCURL

def get_imports(currency: str):
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getimports",
            "params": [currency],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response.json()

def get_imports_with_blocks(currency: str, fromblk: int, toblk: int):
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": [currency, fromblk, toblk],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response.json()