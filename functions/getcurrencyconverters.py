from functions.send_request import send_request
from var.vars import RPCURL, VARRRRPCURL, VDEXRPCURL
from var.dict import COINGECKO_GETCURRENCYCONVERTERS_CURRENCY_FORMATS
from functions.latestblock import latest_block
from functions.getbasketsupply import get_basket_supply
from functions.getcurrencyreserves import get_reserve_dai_price
from functions.extractiaddress import extract_i_address
from functions.getallbaskets import getallbaskets
import time
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

def calculate_currency_prices(currencies, reserves, weights, known_currency, known_price):
    """
    Calculate the USD price of each currency in a weighted basket.
    
    Args:
        currencies (list): Names of all currencies in the basket
        reserves (list): Amount of each currency in the basket
        weights (list): Weight of each currency in the basket (should sum to 1)
        known_currency (str): Name of the currency with known USD price
        known_price (float): Known USD price of the reference currency
    
    Returns:
        dict: USD prices of each currency in the basket
    """
    # Find the index of the known currency
    known_index = currencies.index(known_currency)
    
    # Calculate the total USD value of the known currency
    known_value = reserves[known_index] * known_price
    
    # Calculate the total value of the basket based on the known currency's weight
    total_basket_value = known_value / weights[known_index]
    
    # Calculate the USD price of each currency
    prices = {}
    for i, currency in enumerate(currencies):
        # Currency's total value based on its weight in the basket
        currency_value = total_basket_value * weights[i]
        # Price = allocated value / reserve amount
        currency_price = currency_value / reserves[i]
        prices[currency] = currency_price
    
    return prices


def get_currencyconvertersdata():
    currency_one = ["DAI", "MKR"]
    currency_two = ["SUPERNET", "VRSC", "TBTC", "ETH", "ARRR", "DEX", "CHIPS", "scrvUSD"]
    weights = [0.25, 0.25]
    weights_ = [0.25, 0.25, 0.2, 0.1, 0.05, 0.05, 0.05, 0.05]
    baskets, i_addresses = getallbaskets()
    data = []
    for basket in baskets:
        basket_info = get_currencyconverters(basket)
        if basket_info:
            data.append(basket_info)

    # Initialize VRSC price in USD (to be calculated in Bridge.vETH basket)
    global VRSC_in_USD
    VRSC_in_USD = None
    total_VRSC_reserves = 0
    total_reserves = {}
    final_currency_prices = {}

    for bridge_entry in data:
        bridge_name = bridge_entry.get("bridge", "UnknownBridge")

        if bridge_name in COINGECKO_GETCURRENCYCONVERTERS_CURRENCY_FORMATS:
            currencies = COINGECKO_GETCURRENCYCONVERTERS_CURRENCY_FORMATS[bridge_name]
            reserves = {}

            for i, currency in enumerate(currencies):
                reserve_key = f"reserves_{i}"
                reserves[currency] = bridge_entry.get(reserve_key, None)

                if reserve_key in bridge_entry:
                    if currency not in total_reserves:
                        total_reserves[currency] = 0
                    total_reserves[currency] += bridge_entry[reserve_key]

            if bridge_name == "Bridge.vETH":
                if "DAI" in reserves and "VRSC" in reserves:
                    VRSC_in_USD = reserves["DAI"] / reserves["VRSC"]

            if "VRSC" in reserves and reserves["VRSC"] is not None:
                total_VRSC_reserves += reserves["VRSC"]

            if VRSC_in_USD is None:
                continue

            printed_data = []
            for currency, reserve_value in reserves.items():
                if reserve_value is not None:
                    if currency == "VRSC":
                        price_in_usd = reserve_value * VRSC_in_USD
                    else:
                        if bridge_name == "Bridge.vETH":
                            price_in_usd = reserves["DAI"] / reserve_value
                        else:
                            price_in_usd = reserves["VRSC"] / reserve_value

                    line = f"{bridge_name}_{currency}: Reserves = {reserve_value}, Price in USD = {price_in_usd}"
                    printed_data.append(line)

            all_extracted_reserves = []
            all_extracted_reserves_ = []
            for line in printed_data:
                if "Bridge.vETH_DAI" in line:
                    try:
                        parts = line.split(",")[0]
                        reserve_value = float(parts.split("Reserves = ")[1])
                        all_extracted_reserves.append(reserve_value)
                    except (IndexError, ValueError):
                        pass

                if "Bridge.vETH_MKR" in line:
                    try:
                        parts = line.split(",")[0]
                        reserve_value = float(parts.split("Reserves = ")[1])
                        all_extracted_reserves.append(reserve_value)
                    except (IndexError, ValueError):
                        pass

                if "SUPER🛒" in line:
                    try:
                        parts_ = line.split(",")[0]
                        reserve_value_ = float(parts_.split("Reserves = ")[1])
                        all_extracted_reserves_.append(reserve_value_)
                    except (IndexError, ValueError):
                        pass

            if all_extracted_reserves:
                prices = calculate_currency_prices(currency_one, all_extracted_reserves, weights, "DAI", float(1.0))
                for currency__, price__ in prices.items():
                    final_currency_prices[currency__] = round(price__, 3)

            if all_extracted_reserves_:
                prices_ = calculate_currency_prices(currency_two, all_extracted_reserves_, weights_, "VRSC", float(VRSC_in_USD))
                for currency___, price___ in prices_.items():
                    final_currency_prices[currency___] = round(price___, 3)

            if bridge_name == "NATI🦉":
                if "VRSC" in reserves and "tBTC" in reserves:
                    VRSC_reserves = reserves["VRSC"]
                    tBTC_reserves = reserves["tBTC"]
                    if tBTC_reserves != 0:
                        tBTC_price_in_usd = (VRSC_reserves / tBTC_reserves) * VRSC_in_USD
                        #final_currency_prices["TBTC"] = round(tBTC_price_in_usd, 6)

                if "VRSC" in reserves and "NATIvETH" in reserves:
                    VRSC_reserves = reserves["VRSC"]
                    NATI_vETH_reserves = reserves["NATIvETH"]
                    if NATI_vETH_reserves != 0:
                        NATI_vETH_price_in_usd = (VRSC_reserves / NATI_vETH_reserves) * VRSC_in_USD
                        final_currency_prices["NATI.vETH"] = round(NATI_vETH_price_in_usd, 6)

    if final_currency_prices:
        currency_price_data = {currency: price for currency, price in final_currency_prices.items()}
    else:
        currency_price_data = None

    return currency_price_data, total_reserves

_cached_prices = None
_cached_reserves = None
_cached_time = None

def calculate_liquidity(base_currency, target_currency):
    global _cached_prices, _cached_reserves, _cached_time
    CACHE_TIMEOUT = 10 * 60  # 5 minutes
    current_time = time.time()
    currency_exclusions = ["Bridge.vETH", "Bridge.CHIPS", "Bridge.vARRR", "Bridge.vDEX"]
    stablecoins = ["USDT", "USDC"]
    if base_currency in currency_exclusions or target_currency in currency_exclusions:
        return 0.0

    # Replace tBTC with TBTC in currency names
    base_currency = base_currency.replace("tBTC", "TBTC")
    target_currency = target_currency.replace("tBTC", "TBTC")
    if _cached_prices is not None and _cached_reserves is not None and _cached_time is not None and (current_time - _cached_time < CACHE_TIMEOUT):
        prices = _cached_prices
        reserves = _cached_reserves
        base_currency_price = 1.0 if base_currency in stablecoins else prices.get(base_currency, 0.0)
        target_currency_price = 1.0 if target_currency in stablecoins else prices.get(target_currency, 0.0)
        base_currency_reserve = reserves.get(base_currency, 0.0)
        target_currency_reserve = reserves.get(target_currency, 0.0)
        #print(base_currency_price, target_currency_price)

        # Calculate the values
        base_currency_value =  base_currency_reserve * base_currency_price
        target_currency_value = target_currency_reserve * target_currency_price

        # print(f"Base currency value: {base_currency_value}")
        # print(f"Target currency value: {target_currency_value}")

        # Find the smaller value and multiply it by 2
        smallest_value = min(base_currency_value, target_currency_value)
        result = smallest_value * 2

        #print(f"Smallest value multiplied by 2: {result}")
        return result, base_currency_price, target_currency_price
    else:
        print("Fetching new data...")
        currency_price_data, reserves_new = get_currencyconvertersdata()
        _cached_prices = currency_price_data
        _cached_reserves = reserves_new
        _cached_time = current_time
