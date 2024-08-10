from functions.getbridgecurrencybaskets import *

def dai_reserves():
    reservecurrencies = get_bridge_currency_bridgeveth()
    dai = next((item for item in reservecurrencies if item["currencyid"] == "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM"), None)
    if dai:
        return dai["reserves"]
    return None

def vrsc_reserves():
    reservecurrencies = get_bridge_currency_bridgeveth()
    vrsc = next((item for item in reservecurrencies if item["currencyid"] == "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"), None)
    if vrsc:
        return vrsc["reserves"]
    return None

def mkr_reserves():
    reservecurrencies = get_bridge_currency_bridgeveth()
    mkr = next((item for item in reservecurrencies if item["currencyid"] == "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4"), None)
    if mkr:
        return mkr["reserves"]
    return None

def eth_reserves():
    reservecurrencies = get_bridge_currency_bridgeveth()
    eth = next((item for item in reservecurrencies if item["currencyid"] == "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X"), None)
    if eth:
        return eth["reserves"]
    return None

def pure_reserves():
    reservecurrencies = get_bridge_currency_pure()
    pure = next((item for item in reservecurrencies if item["currencyid"] == "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU"), None)
    if pure:
        return pure["reserves"]
    return None

def tbtc_reserves():
    reservecurrencies = get_bridge_currency_kaiju()
    tbtc = next((item for item in reservecurrencies if item["currencyid"] == "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU"), None)
    if tbtc:
        return tbtc["reserves"]
    return None

def usdc_reserves():
    reservecurrencies = get_bridge_currency_switch()
    usdc = next((item for item in reservecurrencies if item["currencyid"] == "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd"), None)
    if usdc:
        return usdc["reserves"]
    return None

def eurc_reserves():
    reservecurrencies = get_bridge_currency_switch()
    eth = next((item for item in reservecurrencies if item["currencyid"] == "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE"), None)
    if eth:
        return eth["reserves"]
    return None