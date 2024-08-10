from functions.send_request import send_request
from var.vars import RPCURL
from functions.tickerfunc import get_ticker_by_currency_id

def getcurrencystate(currency, height):
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencystate",
            "params": [currency, height],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response

def aggregate_reserve_data(currencyid, height):
    currencies_data = {
        "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV": {"total_reserve": 0},
        "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X": {"total_reserve": 0},
        "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4": {"total_reserve": 0},
        "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM": {"total_reserve": 0}
    }
    
    for _ in range(1440):
        response = getcurrencystate(currencyid, height)
        for currency_id, data in currencies_data.items():
            currency_info = response['result'][0]['currencystate']['currencies'][currency_id]
            data['total_reserve'] += currency_info['reservein'] + currency_info['reserveout']
        height = str(int(height) - 1)
    
    # Fetch currency names and structure the result
    result = {}
    for currency_id, data in currencies_data.items():
        currency_name = get_ticker_by_currency_id(currency_id)
        result[currency_name] = data['total_reserve']
    
    return result