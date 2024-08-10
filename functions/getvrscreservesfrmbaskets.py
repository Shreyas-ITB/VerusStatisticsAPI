from functions.send_request import send_request
from var.vars import RPCURL

def getvrscreserves_frombaskets(basket):
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencyconverters",
            "params": [f"{basket}"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    data = response.get('result')
    total_initialsupply = 0
    total_startblock = 0
    total_reservein = 0
    total_reserveout = 0
    reserves = []
    priceinreserve = []
    for item in data:
        currency_info = item.get('i3f7tSctFkiPpiedY8QR5Tep9p4qDVebDx')
        last_notarization = item.get('lastnotarization')
        if currency_info:
            total_initialsupply += currency_info.get('initialsupply', 0)
            total_startblock += currency_info.get('startblock', 0)
        if last_notarization:
            currencystate = last_notarization.get('currencystate', {})
            currencies = currencystate.get('currencies', {})
            for key, value in currencies.items():
                total_reservein += value.get('reservein', 0)
                total_reserveout += value.get('reserveout', 0)
            reservecurrencies = currencystate.get('reservecurrencies', [])
            for rc in reservecurrencies:
                reserves.append(rc.get('reserves', 0))
                priceinreserve.append(rc.get('priceinreserve', 0))
    volume = total_reservein + total_reserveout
    return reserves[0]