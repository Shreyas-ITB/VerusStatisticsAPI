from functions.send_request import send_request
from var.vars import RPCURL, VARRRRPCURL, VDEXRPCURL
from functions.latestblock import latest_block
from functions.getbasketsupply import get_basket_supply
from functions.getcurrencyreserves import get_reserve_dai_price
from functions.extractiaddress import extract_i_address
from functions.reserves import dai_reserves


def get_currencyconverters(basket_name):
    networkblocks = latest_block()
    reserves = dai_reserves()
    resp = get_reserve_dai_price(reserves)
    supply = get_basket_supply(basket_name)
    if basket_name == "Bridge.vARRR":
        requestData = {
        "method": "post",
        "url": VARRRRPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencyconverters",
            "params": [basket_name],
            "id": 1
            }
        }
    elif basket_name == "Bridge.vDEX":
        requestData = {
        "method": "post",
        "url": VDEXRPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencyconverters",
            "params": [basket_name],
            "id": 1
            }
        }
    else:
        requestData = {
            "method": "post",
            "url": RPCURL,
            "headers": {"Content-Type": "application/json"},
            "data": {
                "method": "getcurrencyconverters",
                "params": [basket_name],
                "id": 1
            }
        }
    response = send_request(**requestData)

    data = response.get('result')
    if not data:
        return None

    i_address = extract_i_address(data)
    if not i_address:
        return None

    total_initialsupply = 0
    total_startblock = 0
    total_reservein = 0
    total_reserveout = 0
    reserves = []
    priceinreserve = []

    for item in data:
        currency_info = item.get(i_address)
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

    # Creating the output dictionary
    output = {
        "bridge": basket_name,
        "initialsupply": total_initialsupply,
        "supply": supply,
        "startblock": total_startblock,
        "block": networkblocks,
        "blk_volume": volume,
    }

    # Adding reserve and price information to the output, with filtering for specific basket
    for i in range(len(reserves)):
        if basket_name == "Bridge.vETH" and i >= 4:
            continue
        output[f"reserves_{i}"] = reserves[i] * resp
        output[f"price_in_reserves_{i}"] = priceinreserve[i] * resp

    return output