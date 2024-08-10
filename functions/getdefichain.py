from functions.send_request import send_request
from var.vars import RPCURL
from functions.tickerfunc import get_ticker_by_currency_id
from functions.getcurrencyreserves import get_reserve_dai_price
from functions.latestblock import latest_block
from functions.reserves import dai_reserves
from functions.getvolinfo import getdefivolume

def getdefichain(basket):
    reserves = dai_reserves()
    resp = get_reserve_dai_price(reserves)
    latest = latest_block()
    volblock = int(latest) - 1440
    
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencyconverters",
            "params": [basket],
            "id": 1
        }
    }
    
    response = send_request(**requestData)
    data = response.get('result')
    if not data:
        return None

    result = []
    volume_info = {}

    # Get volume information for each basket
    for item in data:
        fully_qualified_name = item.get('fullyqualifiedname')
        i_address = next((key for key in item.keys() if key.startswith('i') and len(key) > 1), None)
        
        reserves = []
        priceinreserve = []
        currencyids = []
        total_fees = 0.0
        
        if i_address:
            currency_data = item[i_address]
            last_notarization = item.get('lastnotarization')
            if last_notarization:
                currencystate = last_notarization.get('currencystate', {})
                reservecurrencies = currencystate.get('reservecurrencies', [])
                currencies = currencystate.get('currencies', {})
                for rc in reservecurrencies:
                    reserves_value = rc.get('reserves', 0) * resp
                    priceinreserve_value = rc.get('priceinreserve', 0) * resp
                    reserves.append(reserves_value)
                    priceinreserve.append(priceinreserve_value)
                    currencyids.append(rc.get('currencyid'))

                # Aggregate and multiply all 'fees' from the 'currencystate.currencies'
                for currency_id, currency_info in currencies.items():
                    total_fees += currency_info.get('fees', 0)
                
                total_fees *= resp  # Multiply the aggregated fees by resp
        
        tickers = [get_ticker_by_currency_id(currency_id) for currency_id in currencyids]
        
        # Get volume for the current basket
        volume = getdefivolume(basket, volblock, latest, 1440, "VRSC")
        if volume is not None:
            if isinstance(volume, list):
                for vol in volume:
                    volume_info[vol['basket_name']] = vol['volume']
            else:
                volume_info[basket] = volume  # Handle the case where volume is a single float value
        else:
            volume_info[basket] = None
        
        formatted_priceinreserve = [format(value, '.10f') for value in priceinreserve]
        
        result.append({
            "fullyqualifiedname": fully_qualified_name,
            "i_address": i_address,
            "reserves": reserves,
            "priceinreserve": formatted_priceinreserve,
            "currencyids": currencyids,
            "tickers": tickers,
            #"fees": total_fees,  # Add aggregated fees (multiplied by resp) to the result
        })
    
    formatted_baskets = []
    for basket in result:
        formatted_basket = {
            "liquiditypool": basket['fullyqualifiedname'],
            "lp_address": basket['i_address'],
            #"fees": basket['fees'],  # Add fees to the formatted_basket
            "lp_volume": volume_info.get(basket['fullyqualifiedname'], None),  # Include volume in the formatted basket
            "tokens": []
        }
        for i, ticker in enumerate(basket['tickers']):
            formatted_basket["tokens"].append({
                "ticker": ticker,
                "reserves": basket['reserves'][i],
                "priceinreserve": float(basket['priceinreserve'][i]),
                "i_address": basket['currencyids'][i]
            })
        formatted_baskets.append(formatted_basket)

    return formatted_baskets