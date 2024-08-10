from functions.send_request import send_request
from var.vars import RPCURL

def get_basket_supply(basket_name):
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": [basket_name],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["lastconfirmedcurrencystate"]["supply"]