from functions.reserves import *

def get_reserve_dai_price(reserves):
    return round(dai_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_vrsc_price(reserves):
    return round(vrsc_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_mkr_price(reserves):
    return round(mkr_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_eth_price(reserves):
    return round(eth_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_pure_price(reserves):
    return round(pure_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_tbtc_price(reserves):
    return round(tbtc_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_usdc_price(reserves):
    return round(usdc_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_eurc_price(reserves):
    return round(eurc_reserves() / reserves, 6) if reserves != 0 else 0.0