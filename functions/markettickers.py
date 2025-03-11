import numpy as np
from functions.getvolinfo import getcurrencyvolumeinfo

def getmarkettickers(baskets, volblock, latestblock, ticker_infovrsc, ticker_infodai, ticker_infoeth, ticker_infomkr, ticker_infotbtc):
    for basket in baskets:
        volume_info, currencyvolume = getcurrencyvolumeinfo(basket, volblock, latestblock, 1440, "VRSC")
        if volume_info is not None:
            for pair in volume_info:
                # Remove .vETH suffix and 'v' prefix from currency names
                if pair['currency'] == "Bridge.vETH" or pair['convertto'] == "Bridge.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                elif pair['currency'] == "NATI.vETH" or pair['convertto'] == "NATI.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                else:
                    currency = pair['currency'].replace(".vETH", "").lstrip('v')
                    convertto = pair['convertto'].replace(".vETH", "").lstrip('v')
                if currency == "VRSC" or convertto == "VRSC":
                    # Reverse currency and convertto in the pair
                    if currency == "Bridge.vETH" or convertto == "Bridge.vETH":
                        currency_pair = f"Bridge.vETH-VRSC" if currency == "Bridge.vETH" else f"{convertto}-VRSC"
                    else:
                        currency_pair = f"{convertto}-{currency}"
                    # Calculate weights based on volume
                    weights = pair['volume'] / np.sum(pair['volume'])
                    # Invert values if VRSC is the quote currency (second position)
                    if convertto == "VRSC":
                        volume = pair['volume']
                        last = np.dot(weights, 1 / pair['close']) / np.sum(weights)
                        high = np.dot(weights, 1 / pair['high']) / np.sum(weights)
                        low = np.dot(weights, 1 / pair['low']) / np.sum(weights)
                        openn = np.dot(weights, 1 / pair['open']) / np.sum(weights)
                    else:
                        volume = pair['volume']
                        last = np.dot(weights, pair['close']) / np.sum(weights)
                        high = np.dot(weights, pair['high']) / np.sum(weights)
                        low = np.dot(weights, pair['low']) / np.sum(weights)
                        openn = np.dot(weights, pair['open']) / np.sum(weights)
                    ticker_infovrsc.append({
                        'symbol': currency_pair,
                        'symbolName': currency_pair,
                        'volume': volume,
                        'last': last,
                        'high': high,
                        'low': low,
                        'open': openn
                    })
        
    # Combine reverse pairs
    combined_ticker_infovrsc = {}
    for ticker in ticker_infovrsc:
        symbol = ticker['symbol']
        reverse_symbol = "-".join(symbol.split("-")[::-1])
        if symbol in combined_ticker_infovrsc:
            combined_volume = combined_ticker_infovrsc[symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infovrsc[symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infovrsc[symbol]['volume'] = combined_volume
            combined_ticker_infovrsc[symbol]['last'] = np.dot(
                [combined_ticker_infovrsc[symbol]['last'], ticker['last']], combined_weights)
            combined_ticker_infovrsc[symbol]['high'] = np.dot(
                [combined_ticker_infovrsc[symbol]['high'], ticker['high']], combined_weights)
            combined_ticker_infovrsc[symbol]['low'] = np.dot(
                [combined_ticker_infovrsc[symbol]['low'], ticker['low']], combined_weights)
            combined_ticker_infovrsc[symbol]['open'] = np.dot(
                [combined_ticker_infovrsc[symbol]['open'], ticker['open']], combined_weights)
        elif reverse_symbol in combined_ticker_infovrsc:
            combined_volume = combined_ticker_infovrsc[reverse_symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infovrsc[reverse_symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infovrsc[reverse_symbol]['volume'] = combined_volume
            combined_ticker_infovrsc[reverse_symbol]['last'] = np.dot(
                [combined_ticker_infovrsc[reverse_symbol]['last'], ticker['last']], combined_weights)
            combined_ticker_infovrsc[reverse_symbol]['high'] = np.dot(
                [combined_ticker_infovrsc[reverse_symbol]['high'], ticker['low']], combined_weights)
            combined_ticker_infovrsc[reverse_symbol]['low'] = np.dot(
                [combined_ticker_infovrsc[reverse_symbol]['low'], ticker['high']], combined_weights)
            combined_ticker_infovrsc[reverse_symbol]['open'] = np.dot(
                [combined_ticker_infovrsc[reverse_symbol]['open'], ticker['open']], combined_weights)
        else:
            combined_ticker_infovrsc[symbol] = ticker


    for basket in baskets:
        daivolume_info, daicurrencyvolume = getcurrencyvolumeinfo(basket, volblock, latestblock, 1440, "DAI.vETH")
        if daivolume_info is not None:
            for pair in daivolume_info:
                # Remove .vETH suffix and 'v' prefix from currency names
                if pair['currency'] == "Bridge.vETH" or pair['convertto'] == "Bridge.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                elif pair['currency'] == "NATI.vETH" or pair['convertto'] == "NATI.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                else:
                    currency = pair['currency'].replace(".vETH", "").lstrip('v')
                    convertto = pair['convertto'].replace(".vETH", "").lstrip('v')
                if currency == "DAI" or convertto == "DAI":
                    # Reverse currency and convertto in the pair
                    if currency == "Bridge.vETH" or convertto == "Bridge.vETH":
                        currency_pair = f"Bridge.vETH-DAI" if currency == "Bridge.vETH" else f"{convertto}-DAI"
                    else:
                        currency_pair = f"{convertto}-{currency}"
                    weights = pair['volume'] / np.sum(pair['volume'])
                    # Invert values if VRSC is the quote currency (second position)
                    if convertto == "DAI":
                        volume = pair['volume']
                        last = np.dot(weights, 1 / pair['close']) / np.sum(weights)
                        high = np.dot(weights, 1 / pair['high']) / np.sum(weights)
                        low = np.dot(weights, 1 / pair['low']) / np.sum(weights)
                        openn = np.dot(weights, 1 / pair['open']) / np.sum(weights)
                    else:
                        volume = pair['volume']
                        last = np.dot(weights, pair['close']) / np.sum(weights)
                        high = np.dot(weights, pair['high']) / np.sum(weights)
                        low = np.dot(weights, pair['low']) / np.sum(weights)
                        openn = np.dot(weights, pair['open']) / np.sum(weights)
                    ticker_infodai.append({
                        'symbol': currency_pair,
                        'symbolName': currency_pair,
                        'volume': volume,
                        'last': last,
                        'high': high,
                        'low': low,
                        'open': openn
                    })
        
    # Combine reverse pairs
    combined_ticker_infodai = {}
    for ticker in ticker_infodai:
        symbol = ticker['symbol']
        reverse_symbol = "-".join(symbol.split("-")[::-1])
        if symbol in combined_ticker_infodai:
            combined_volume = combined_ticker_infodai[symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infodai[symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infodai[symbol]['volume'] = combined_volume
            combined_ticker_infodai[symbol]['last'] = np.dot(
                [combined_ticker_infodai[symbol]['last'], ticker['last']], combined_weights)
            combined_ticker_infodai[symbol]['high'] = np.dot(
                [combined_ticker_infodai[symbol]['high'], ticker['high']], combined_weights)
            combined_ticker_infodai[symbol]['low'] = np.dot(
                [combined_ticker_infodai[symbol]['low'], ticker['low']], combined_weights)
            combined_ticker_infodai[symbol]['open'] = np.dot(
                [combined_ticker_infodai[symbol]['open'], ticker['open']], combined_weights)
        elif reverse_symbol in combined_ticker_infodai:
            combined_volume = combined_ticker_infodai[reverse_symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infodai[reverse_symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infodai[reverse_symbol]['volume'] = combined_volume
            combined_ticker_infodai[reverse_symbol]['last'] = np.dot(
                [combined_ticker_infodai[reverse_symbol]['last'], ticker['last']], combined_weights)
            combined_ticker_infodai[reverse_symbol]['high'] = np.dot(
                [combined_ticker_infodai[reverse_symbol]['high'], ticker['low']], combined_weights)
            combined_ticker_infodai[reverse_symbol]['low'] = np.dot(
                [combined_ticker_infodai[reverse_symbol]['low'], ticker['high']], combined_weights)
            combined_ticker_infodai[reverse_symbol]['open'] = np.dot(
                [combined_ticker_infodai[reverse_symbol]['open'], ticker['open']], combined_weights)
        else:
            combined_ticker_infodai[symbol] = ticker
    
    for basket in baskets:
        ethvolume_info, ethcurrencyvolume = getcurrencyvolumeinfo(basket, volblock, latestblock, 1440, "vETH")
        if ethvolume_info is not None:
            for pair in ethvolume_info:
                # Remove .vETH suffix and 'v' prefix from currency names
                if pair['currency'] == "Bridge.vETH" or pair['convertto'] == "Bridge.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                elif pair['currency'] == "NATI.vETH" or pair['convertto'] == "NATI.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                else:
                    currency = pair['currency'].replace(".vETH", "").lstrip('v')
                    convertto = pair['convertto'].replace(".vETH", "").lstrip('v')
                if currency == "ETH" or convertto == "ETH":
                    # Reverse currency and convertto in the pair
                    if currency == "Bridge.vETH" or convertto == "Bridge.vETH":
                        currency_pair = f"Bridge.vETH-ETH" if currency == "Bridge.vETH" else f"{convertto}-ETH"
                    else:
                        currency_pair = f"{convertto}-{currency}"
                    weights = pair['volume'] / np.sum(pair['volume'])
                    # Invert values if VRSC is the quote currency (second position)
                    if convertto == "ETH":
                        volume = pair['volume']
                        last = np.dot(weights, 1 / pair['close']) / np.sum(weights)
                        high = np.dot(weights, 1 / pair['high']) / np.sum(weights)
                        low = np.dot(weights, 1 / pair['low']) / np.sum(weights)
                        openn = np.dot(weights, 1 / pair['open']) / np.sum(weights)
                    else:
                        volume = pair['volume']
                        last = np.dot(weights, pair['close']) / np.sum(weights)
                        high = np.dot(weights, pair['high']) / np.sum(weights)
                        low = np.dot(weights, pair['low']) / np.sum(weights)
                        openn = np.dot(weights, pair['open']) / np.sum(weights)
                    ticker_infoeth.append({
                        'symbol': currency_pair,
                        'symbolName': currency_pair,
                        'volume': volume,
                        'last': last,
                        'high': high,
                        'low': low,
                        'open': openn
                    })
        
    # Combine reverse pairs
    combined_ticker_infoeth = {}
    for ticker in ticker_infoeth:
        symbol = ticker['symbol']
        reverse_symbol = "-".join(symbol.split("-")[::-1])
        if symbol in combined_ticker_infoeth:
            combined_volume = combined_ticker_infoeth[symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infoeth[symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infoeth[symbol]['volume'] = combined_volume
            combined_ticker_infoeth[symbol]['last'] = np.dot(
                [combined_ticker_infoeth[symbol]['last'], ticker['last']], combined_weights)
            combined_ticker_infoeth[symbol]['high'] = np.dot(
                [combined_ticker_infoeth[symbol]['high'], ticker['high']], combined_weights)
            combined_ticker_infoeth[symbol]['low'] = np.dot(
                [combined_ticker_infoeth[symbol]['low'], ticker['low']], combined_weights)
            combined_ticker_infoeth[symbol]['open'] = np.dot(
                [combined_ticker_infoeth[symbol]['open'], ticker['open']], combined_weights)
        elif reverse_symbol in combined_ticker_infoeth:
            combined_volume = combined_ticker_infoeth[reverse_symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infoeth[reverse_symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infoeth[reverse_symbol]['volume'] = combined_volume
            combined_ticker_infoeth[reverse_symbol]['last'] = np.dot(
                [combined_ticker_infoeth[reverse_symbol]['last'], ticker['last']], combined_weights)
            combined_ticker_infoeth[reverse_symbol]['high'] = np.dot(
                [combined_ticker_infoeth[reverse_symbol]['high'], ticker['low']], combined_weights)
            combined_ticker_infoeth[reverse_symbol]['low'] = np.dot(
                [combined_ticker_infoeth[reverse_symbol]['low'], ticker['high']], combined_weights)
            combined_ticker_infoeth[reverse_symbol]['open'] = np.dot(
                [combined_ticker_infoeth[reverse_symbol]['open'], ticker['open']], combined_weights)
        else:
            combined_ticker_infoeth[symbol] = ticker


    for basket in baskets:
        mkrvolume_info, mkrcurrencyvolume = getcurrencyvolumeinfo(basket, volblock, latestblock, 1440, "MKR.vETH")
        if mkrvolume_info is not None:
            for pair in mkrvolume_info:
                # Remove .vETH suffix and 'v' prefix from currency names
                if pair['currency'] == "Bridge.vETH" or pair['convertto'] == "Bridge.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                elif pair['currency'] == "NATI.vETH" or pair['convertto'] == "NATI.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                else:
                    currency = pair['currency'].replace(".vETH", "").lstrip('v')
                    convertto = pair['convertto'].replace(".vETH", "").lstrip('v')
                if currency == "MKR" or convertto == "MKR":
                    # Reverse currency and convertto in the pair
                    if currency == "Bridge.vETH" or convertto == "Bridge.vETH":
                        currency_pair = f"Bridge.vETH-MKR" if currency == "Bridge.vETH" else f"{convertto}-MKR"
                    else:
                        currency_pair = f"{convertto}-{currency}"
                    weights = pair['volume'] / np.sum(pair['volume'])
                    # Invert values if VRSC is the quote currency (second position)
                    if convertto == "MKR":
                        volume = pair['volume']
                        last = np.dot(weights, 1 / pair['close']) / np.sum(weights)
                        high = np.dot(weights, 1 / pair['high']) / np.sum(weights)
                        low = np.dot(weights, 1 / pair['low']) / np.sum(weights)
                        openn = np.dot(weights, 1 / pair['open']) / np.sum(weights)
                    else:
                        volume = pair['volume']
                        last = np.dot(weights, pair['close']) / np.sum(weights)
                        high = np.dot(weights, pair['high']) / np.sum(weights)
                        low = np.dot(weights, pair['low']) / np.sum(weights)
                        openn = np.dot(weights, pair['open']) / np.sum(weights)
                    ticker_infomkr.append({
                        'symbol': currency_pair,
                        'symbolName': currency_pair,
                        'volume': volume,
                        'last': last,
                        'high': high,
                        'low': low,
                        'open': openn
                    })
        
    # Combine reverse pairs
    combined_ticker_infomkr = {}
    for ticker in ticker_infomkr:
        symbol = ticker['symbol']
        reverse_symbol = "-".join(symbol.split("-")[::-1])
        if symbol in combined_ticker_infomkr:
            combined_volume = combined_ticker_infomkr[symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infomkr[symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infomkr[symbol]['volume'] = combined_volume
            combined_ticker_infomkr[symbol]['last'] = np.dot(
                [combined_ticker_infomkr[symbol]['last'], ticker['last']], combined_weights)
            combined_ticker_infomkr[symbol]['high'] = np.dot(
                [combined_ticker_infomkr[symbol]['high'], ticker['high']], combined_weights)
            combined_ticker_infomkr[symbol]['low'] = np.dot(
                [combined_ticker_infomkr[symbol]['low'], ticker['low']], combined_weights)
            combined_ticker_infomkr[symbol]['open'] = np.dot(
                [combined_ticker_infomkr[symbol]['open'], ticker['open']], combined_weights)
        elif reverse_symbol in combined_ticker_infomkr:
            combined_volume = combined_ticker_infomkr[reverse_symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infomkr[reverse_symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infomkr[reverse_symbol]['volume'] = combined_volume
            combined_ticker_infomkr[reverse_symbol]['last'] = np.dot(
                [combined_ticker_infomkr[reverse_symbol]['last'], ticker['last']], combined_weights)
            combined_ticker_infomkr[reverse_symbol]['high'] = np.dot(
                [combined_ticker_infomkr[reverse_symbol]['high'], ticker['low']], combined_weights)
            combined_ticker_infomkr[reverse_symbol]['low'] = np.dot(
                [combined_ticker_infomkr[reverse_symbol]['low'], ticker['high']], combined_weights)
            combined_ticker_infomkr[reverse_symbol]['open'] = np.dot(
                [combined_ticker_infomkr[reverse_symbol]['open'], ticker['open']], combined_weights)
        else:
            combined_ticker_infomkr[symbol] = ticker

    for basket in baskets:
        tbtcvolume_info, tbtccurrencyvolume = getcurrencyvolumeinfo(basket, volblock, latestblock, 1440, "tBTC.vETH")
        if tbtcvolume_info is not None:
            for pair in tbtcvolume_info:
                # Remove .vETH suffix and 'v' prefix from currency names
                if pair['currency'] == "Bridge.vETH" or pair['convertto'] == "Bridge.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                elif pair['currency'] == "NATI.vETH" or pair['convertto'] == "NATI.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                else:
                    currency = pair['currency'].replace(".vETH", "").lstrip('v')
                    convertto = pair['convertto'].replace(".vETH", "").lstrip('v')

                    if currency.lower() == "tbtc":
                        currency = "TBTC"
                    if convertto.lower() == "tbtc":
                        convertto = "TBTC"

                if currency == "TBTC" or convertto == "TBTC":
                    # Reverse currency and convertto in the pair
                    if currency == "Bridge.vETH" or convertto == "Bridge.vETH":
                        currency_pair = f"Bridge.vETH-TBTC" if currency == "Bridge.vETH" else f"{convertto}-TBTC"
                    else:
                        currency_pair = f"{convertto}-{currency}"
                    weights = pair['volume'] / np.sum(pair['volume'])
                    # Invert values if VRSC is the quote currency (second position)
                    if convertto == "TBTC":
                        volume = pair['volume']
                        last = np.dot(weights, 1 / pair['close']) / np.sum(weights)
                        high = np.dot(weights, 1 / pair['high']) / np.sum(weights)
                        low = np.dot(weights, 1 / pair['low']) / np.sum(weights)
                        openn = np.dot(weights, 1 / pair['open']) / np.sum(weights)
                    else:
                        volume = pair['volume']
                        last = np.dot(weights, pair['close']) / np.sum(weights)
                        high = np.dot(weights, pair['high']) / np.sum(weights)
                        low = np.dot(weights, pair['low']) / np.sum(weights)
                        openn = np.dot(weights, pair['open']) / np.sum(weights)
                    ticker_infotbtc.append({
                        'symbol': currency_pair,
                        'symbolName': currency_pair,
                        'volume': volume,
                        'last': last,
                        'high': high,
                        'low': low,
                        'open': openn
                    })
        
    # Combine reverse pairs
    combined_ticker_infotbtc = {}
    for ticker in ticker_infotbtc:
        symbol = ticker['symbol']
        reverse_symbol = "-".join(symbol.split("-")[::-1])
        if symbol in combined_ticker_infotbtc:
            combined_volume = combined_ticker_infotbtc[symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infotbtc[symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infotbtc[symbol]['volume'] = combined_volume
            combined_ticker_infotbtc[symbol]['last'] = np.dot(
                [combined_ticker_infotbtc[symbol]['last'], ticker['last']], combined_weights)
            combined_ticker_infotbtc[symbol]['high'] = np.dot(
                [combined_ticker_infotbtc[symbol]['high'], ticker['high']], combined_weights)
            combined_ticker_infotbtc[symbol]['low'] = np.dot(
                [combined_ticker_infotbtc[symbol]['low'], ticker['low']], combined_weights)
            combined_ticker_infotbtc[symbol]['open'] = np.dot(
                [combined_ticker_infotbtc[symbol]['open'], ticker['open']], combined_weights)
        elif reverse_symbol in combined_ticker_infotbtc:
            combined_volume = combined_ticker_infotbtc[reverse_symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infotbtc[reverse_symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infotbtc[reverse_symbol]['volume'] = combined_volume
            combined_ticker_infotbtc[reverse_symbol]['last'] = np.dot(
                [combined_ticker_infotbtc[reverse_symbol]['last'], ticker['last']], combined_weights)
            combined_ticker_infotbtc[reverse_symbol]['high'] = np.dot(
                [combined_ticker_infotbtc[reverse_symbol]['high'], ticker['low']], combined_weights)
            combined_ticker_infotbtc[reverse_symbol]['low'] = np.dot(
                [combined_ticker_infotbtc[reverse_symbol]['low'], ticker['high']], combined_weights)
            combined_ticker_infotbtc[reverse_symbol]['open'] = np.dot(
                [combined_ticker_infotbtc[reverse_symbol]['open'], ticker['open']], combined_weights)
        else:
            combined_ticker_infotbtc[symbol] = ticker


    final_ticker_infovrsc = list(combined_ticker_infovrsc.values())
    final_ticker_infodai = list(combined_ticker_infodai.values())
    final_ticker_infoeth = list(combined_ticker_infoeth.values())
    final_ticker_infomkr = list(combined_ticker_infomkr.values())
    final_ticker_infotbtc = list(combined_ticker_infotbtc.values())
    return final_ticker_infovrsc, final_ticker_infodai, final_ticker_infoeth, final_ticker_infomkr, final_ticker_infotbtc

def getmarkettickersnew(baskets, volblock, latestblock, ticker_infovrsc, ticker_infodai, ticker_infoeth, ticker_infomkr, ticker_infotbtc):
    price_vrsc_usd = getcurrencyvolumeinfo("Bridge.vETH", volblock, latestblock, 1440, "VRSC")
    price_vrsc_usd = price_vrsc_usd[0]
    # Iterating through the list to find the correct entry
    for pair in price_vrsc_usd:
        if pair['convertto'] == 'DAI.vETH' and pair['currency'] == 'VRSC':
            global result
            result = 1 / pair['close']
    for basket in baskets:
        volume_info, currencyvolume = getcurrencyvolumeinfo(basket, volblock, latestblock, 1440, "VRSC")
        liquidity_volume = getcurrencyvolumeinfo_new("Bridge.vETH", latestblock, latestblock, 1, "VRSC", "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV")
        print(liquidity_volume)
        #print(volume_info)
        basket_addr_vrsc = get_currencyid_by_ticker(basket)
        #print(basket + " basket i address - " + basket_addr_vrsc)
        if volume_info is not None:
            for pair in volume_info:
                # Remove .vETH suffix and 'v' prefix from currency names
                if pair['currency'] == "Bridge.vETH" or pair['convertto'] == "Bridge.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                elif pair['currency'] == "NATI.vETH" or pair['convertto'] == "NATI.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                else:
                    currency = pair['currency'].replace(".vETH", "").lstrip('v')
                    convertto = pair['convertto'].replace(".vETH", "").lstrip('v')
                if currency == "VRSC" or convertto == "VRSC":
                    # Reverse currency and convertto in the pair
                    if currency == "Bridge.vETH" or convertto == "Bridge.vETH":
                        currency_pair = f"Bridge.vETH_VRSC" if currency == "Bridge.vETH" else f"{convertto}_VRSC"
                    else:
                        currency_pair = f"{convertto}_{currency}"
                    # Calculate weights based on volume
                    weights = pair['volume'] / np.sum(pair['volume'])
                    # Invert values if VRSC is the quote currency (second position)
                    if convertto == "VRSC":
                        volume = pair['volume']
                        last = np.dot(weights, 1 / pair['close']) / np.sum(weights)
                        high = np.dot(weights, 1 / pair['high']) / np.sum(weights)
                        low = np.dot(weights, 1 / pair['low']) / np.sum(weights)
                        openn = np.dot(weights, 1 / pair['open']) / np.sum(weights)
                    else:
                        volume = pair['volume']
                        last = np.dot(weights, pair['close']) / np.sum(weights)
                        high = np.dot(weights, pair['high']) / np.sum(weights)
                        low = np.dot(weights, pair['low']) / np.sum(weights)
                        openn = np.dot(weights, pair['open']) / np.sum(weights)
                    base_currency, target_currency = currency_pair.split("_")
                    ticker_infovrsc.append({
                        'ticker_id': currency_pair,
                        'base_currency': base_currency,
                        'target_currency': target_currency,                   
                        'pool_id': basket_addr_vrsc,
                        'volume': volume,
                        'liquidity_in_usd': result * volume,
                        'last_price': last,
                        'high': high,
                        'low': low,
                        'open': openn
                    })
        
    # Combine reverse pairs
    combined_ticker_infovrsc = {}
    for ticker in ticker_infovrsc:
        symbol = ticker['ticker_id']
        reverse_symbol = "-".join(symbol.split("-")[::-1])
        if symbol in combined_ticker_infovrsc:
            combined_volume = combined_ticker_infovrsc[symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infovrsc[symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infovrsc[symbol]['volume'] = combined_volume
            combined_ticker_infovrsc[symbol]['last_price'] = np.dot(
                [combined_ticker_infovrsc[symbol]['last_price'], ticker['last_price']], combined_weights)
            combined_ticker_infovrsc[symbol]['high'] = np.dot(
                [combined_ticker_infovrsc[symbol]['high'], ticker['high']], combined_weights)
            combined_ticker_infovrsc[symbol]['low'] = np.dot(
                [combined_ticker_infovrsc[symbol]['low'], ticker['low']], combined_weights)
            combined_ticker_infovrsc[symbol]['open'] = np.dot(
                [combined_ticker_infovrsc[symbol]['open'], ticker['open']], combined_weights)
        elif reverse_symbol in combined_ticker_infovrsc:
            combined_volume = combined_ticker_infovrsc[reverse_symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infovrsc[reverse_symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infovrsc[reverse_symbol]['volume'] = combined_volume
            combined_ticker_infovrsc[reverse_symbol]['last_price'] = np.dot(
                [combined_ticker_infovrsc[reverse_symbol]['last_price'], ticker['last_price']], combined_weights)
            combined_ticker_infovrsc[reverse_symbol]['high'] = np.dot(
                [combined_ticker_infovrsc[reverse_symbol]['high'], ticker['low']], combined_weights)
            combined_ticker_infovrsc[reverse_symbol]['low'] = np.dot(
                [combined_ticker_infovrsc[reverse_symbol]['low'], ticker['high']], combined_weights)
            combined_ticker_infovrsc[reverse_symbol]['open'] = np.dot(
                [combined_ticker_infovrsc[reverse_symbol]['open'], ticker['open']], combined_weights)
        else:
            combined_ticker_infovrsc[symbol] = ticker


    for basket in baskets:
        daivolume_info, daicurrencyvolume = getcurrencyvolumeinfo(basket, volblock, latestblock, 1440, "DAI.vETH")
        basket_addr_dai = get_currencyid_by_ticker(basket)
        if daivolume_info is not None:
            for pair in daivolume_info:
                # Remove .vETH suffix and 'v' prefix from currency names
                if pair['currency'] == "Bridge.vETH" or pair['convertto'] == "Bridge.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                elif pair['currency'] == "NATI.vETH" or pair['convertto'] == "NATI.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                else:
                    currency = pair['currency'].replace(".vETH", "").lstrip('v')
                    convertto = pair['convertto'].replace(".vETH", "").lstrip('v')
                if currency == "DAI" or convertto == "DAI":
                    # Reverse currency and convertto in the pair
                    if currency == "Bridge.vETH" or convertto == "Bridge.vETH":
                        currency_pair = f"Bridge.vETH_DAI" if currency == "Bridge.vETH" else f"{convertto}_DAI"
                    else:
                        currency_pair = f"{convertto}_{currency}"
                    weights = pair['volume'] / np.sum(pair['volume'])
                    # Invert values if VRSC is the quote currency (second position)
                    if convertto == "DAI":
                        volume = pair['volume']
                        last = np.dot(weights, 1 / pair['close']) / np.sum(weights)
                        high = np.dot(weights, 1 / pair['high']) / np.sum(weights)
                        low = np.dot(weights, 1 / pair['low']) / np.sum(weights)
                        openn = np.dot(weights, 1 / pair['open']) / np.sum(weights)
                    else:
                        volume = pair['volume']
                        last = np.dot(weights, pair['close']) / np.sum(weights)
                        high = np.dot(weights, pair['high']) / np.sum(weights)
                        low = np.dot(weights, pair['low']) / np.sum(weights)
                        openn = np.dot(weights, pair['open']) / np.sum(weights)
                    base_currency, target_currency = currency_pair.split("_")
                    ticker_infodai.append({
                        'ticker_id': currency_pair,
                        'base_currency': base_currency,
                        'target_currency': target_currency,
                        'pool_id': basket_addr_dai,
                        'volume': volume,
                        'liquidity_in_usd': result * volume,
                        'last_price': last,
                        'high': high,
                        'low': low,
                        'open': openn
                    })
        
    # Combine reverse pairs
    combined_ticker_infodai = {}
    for ticker in ticker_infodai:
        symbol = ticker['ticker_id']
        reverse_symbol = "-".join(symbol.split("-")[::-1])
        if symbol in combined_ticker_infodai:
            combined_volume = combined_ticker_infodai[symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infodai[symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infodai[symbol]['volume'] = combined_volume
            combined_ticker_infodai[symbol]['last_price'] = np.dot(
                [combined_ticker_infodai[symbol]['last_price'], ticker['last_price']], combined_weights)
            combined_ticker_infodai[symbol]['high'] = np.dot(
                [combined_ticker_infodai[symbol]['high'], ticker['high']], combined_weights)
            combined_ticker_infodai[symbol]['low'] = np.dot(
                [combined_ticker_infodai[symbol]['low'], ticker['low']], combined_weights)
            combined_ticker_infodai[symbol]['open'] = np.dot(
                [combined_ticker_infodai[symbol]['open'], ticker['open']], combined_weights)
        elif reverse_symbol in combined_ticker_infodai:
            combined_volume = combined_ticker_infodai[reverse_symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infodai[reverse_symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infodai[reverse_symbol]['volume'] = combined_volume
            combined_ticker_infodai[reverse_symbol]['last_price'] = np.dot(
                [combined_ticker_infodai[reverse_symbol]['last_price'], ticker['last_price']], combined_weights)
            combined_ticker_infodai[reverse_symbol]['high'] = np.dot(
                [combined_ticker_infodai[reverse_symbol]['high'], ticker['low']], combined_weights)
            combined_ticker_infodai[reverse_symbol]['low'] = np.dot(
                [combined_ticker_infodai[reverse_symbol]['low'], ticker['high']], combined_weights)
            combined_ticker_infodai[reverse_symbol]['open'] = np.dot(
                [combined_ticker_infodai[reverse_symbol]['open'], ticker['open']], combined_weights)
        else:
            combined_ticker_infodai[symbol] = ticker
    
    for basket in baskets:
        ethvolume_info, ethcurrencyvolume = getcurrencyvolumeinfo(basket, volblock, latestblock, 1440, "vETH")
        basket_addr_eth = get_currencyid_by_ticker(basket)
        if ethvolume_info is not None:
            for pair in ethvolume_info:
                # Remove .vETH suffix and 'v' prefix from currency names
                if pair['currency'] == "Bridge.vETH" or pair['convertto'] == "Bridge.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                elif pair['currency'] == "NATI.vETH" or pair['convertto'] == "NATI.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                else:
                    currency = pair['currency'].replace(".vETH", "").lstrip('v')
                    convertto = pair['convertto'].replace(".vETH", "").lstrip('v')
                if currency == "ETH" or convertto == "ETH":
                    # Reverse currency and convertto in the pair
                    if currency == "Bridge.vETH" or convertto == "Bridge.vETH":
                        currency_pair = f"Bridge.vETH_ETH" if currency == "Bridge.vETH" else f"{convertto}_ETH"
                    else:
                        currency_pair = f"{convertto}_{currency}"
                    weights = pair['volume'] / np.sum(pair['volume'])
                    # Invert values if VRSC is the quote currency (second position)
                    if convertto == "ETH":
                        volume = pair['volume']
                        last = np.dot(weights, 1 / pair['close']) / np.sum(weights)
                        high = np.dot(weights, 1 / pair['high']) / np.sum(weights)
                        low = np.dot(weights, 1 / pair['low']) / np.sum(weights)
                        openn = np.dot(weights, 1 / pair['open']) / np.sum(weights)
                    else:
                        volume = pair['volume']
                        last = np.dot(weights, pair['close']) / np.sum(weights)
                        high = np.dot(weights, pair['high']) / np.sum(weights)
                        low = np.dot(weights, pair['low']) / np.sum(weights)
                        openn = np.dot(weights, pair['open']) / np.sum(weights)
                    base_currency, target_currency = currency_pair.split("_")
                    ticker_infoeth.append({
                        'ticker_id': currency_pair,
                        'base_currency': base_currency,
                        'target_currency': target_currency,
                        'pool_id': basket_addr_eth,
                        'volume': volume,
                        'liquidity_in_usd': result * volume,
                        'last_price': last,
                        'high': high,
                        'low': low,
                        'open': openn
                    })
        
    # Combine reverse pairs
    combined_ticker_infoeth = {}
    for ticker in ticker_infoeth:
        symbol = ticker['ticker_id']
        reverse_symbol = "-".join(symbol.split("-")[::-1])
        if symbol in combined_ticker_infoeth:
            combined_volume = combined_ticker_infoeth[symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infoeth[symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infoeth[symbol]['volume'] = combined_volume
            combined_ticker_infoeth[symbol]['last_price'] = np.dot(
                [combined_ticker_infoeth[symbol]['last_price'], ticker['last_price']], combined_weights)
            combined_ticker_infoeth[symbol]['high'] = np.dot(
                [combined_ticker_infoeth[symbol]['high'], ticker['high']], combined_weights)
            combined_ticker_infoeth[symbol]['low'] = np.dot(
                [combined_ticker_infoeth[symbol]['low'], ticker['low']], combined_weights)
            combined_ticker_infoeth[symbol]['open'] = np.dot(
                [combined_ticker_infoeth[symbol]['open'], ticker['open']], combined_weights)
        elif reverse_symbol in combined_ticker_infoeth:
            combined_volume = combined_ticker_infoeth[reverse_symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infoeth[reverse_symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infoeth[reverse_symbol]['volume'] = combined_volume
            combined_ticker_infoeth[reverse_symbol]['last_price'] = np.dot(
                [combined_ticker_infoeth[reverse_symbol]['last_price'], ticker['last_price']], combined_weights)
            combined_ticker_infoeth[reverse_symbol]['high'] = np.dot(
                [combined_ticker_infoeth[reverse_symbol]['high'], ticker['low']], combined_weights)
            combined_ticker_infoeth[reverse_symbol]['low'] = np.dot(
                [combined_ticker_infoeth[reverse_symbol]['low'], ticker['high']], combined_weights)
            combined_ticker_infoeth[reverse_symbol]['open'] = np.dot(
                [combined_ticker_infoeth[reverse_symbol]['open'], ticker['open']], combined_weights)
        else:
            combined_ticker_infoeth[symbol] = ticker


    for basket in baskets:
        mkrvolume_info, mkrcurrencyvolume = getcurrencyvolumeinfo(basket, volblock, latestblock, 1440, "MKR.vETH")
        basket_addr_mkr = get_currencyid_by_ticker(basket)
        if mkrvolume_info is not None:
            for pair in mkrvolume_info:
                # Remove .vETH suffix and 'v' prefix from currency names
                if pair['currency'] == "Bridge.vETH" or pair['convertto'] == "Bridge.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                elif pair['currency'] == "NATI.vETH" or pair['convertto'] == "NATI.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                else:
                    currency = pair['currency'].replace(".vETH", "").lstrip('v')
                    convertto = pair['convertto'].replace(".vETH", "").lstrip('v')
                if currency == "MKR" or convertto == "MKR":
                    # Reverse currency and convertto in the pair
                    if currency == "Bridge.vETH" or convertto == "Bridge.vETH":
                        currency_pair = f"Bridge.vETH_MKR" if currency == "Bridge.vETH" else f"{convertto}_MKR"
                    else:
                        currency_pair = f"{convertto}_{currency}"
                    weights = pair['volume'] / np.sum(pair['volume'])
                    # Invert values if VRSC is the quote currency (second position)
                    if convertto == "MKR":
                        volume = pair['volume']
                        last = np.dot(weights, 1 / pair['close']) / np.sum(weights)
                        high = np.dot(weights, 1 / pair['high']) / np.sum(weights)
                        low = np.dot(weights, 1 / pair['low']) / np.sum(weights)
                        openn = np.dot(weights, 1 / pair['open']) / np.sum(weights)
                    else:
                        volume = pair['volume']
                        last = np.dot(weights, pair['close']) / np.sum(weights)
                        high = np.dot(weights, pair['high']) / np.sum(weights)
                        low = np.dot(weights, pair['low']) / np.sum(weights)
                        openn = np.dot(weights, pair['open']) / np.sum(weights)
                    base_currency, target_currency = currency_pair.split("_")
                    ticker_infomkr.append({
                        'ticker_id': currency_pair,
                        'base_currency': base_currency,
                        'target_currency': target_currency,
                        'pool_id': basket_addr_mkr,
                        'volume': volume,
                        'liquidity_in_usd': result * volume,
                        'last_price': last,
                        'high': high,
                        'low': low,
                        'open': openn
                    })
        
    # Combine reverse pairs
    combined_ticker_infomkr = {}
    for ticker in ticker_infomkr:
        symbol = ticker['ticker_id']
        reverse_symbol = "-".join(symbol.split("-")[::-1])
        if symbol in combined_ticker_infomkr:
            combined_volume = combined_ticker_infomkr[symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infomkr[symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infomkr[symbol]['volume'] = combined_volume
            combined_ticker_infomkr[symbol]['last_price'] = np.dot(
                [combined_ticker_infomkr[symbol]['last_price'], ticker['last_price']], combined_weights)
            combined_ticker_infomkr[symbol]['high'] = np.dot(
                [combined_ticker_infomkr[symbol]['high'], ticker['high']], combined_weights)
            combined_ticker_infomkr[symbol]['low'] = np.dot(
                [combined_ticker_infomkr[symbol]['low'], ticker['low']], combined_weights)
            combined_ticker_infomkr[symbol]['open'] = np.dot(
                [combined_ticker_infomkr[symbol]['open'], ticker['open']], combined_weights)
        elif reverse_symbol in combined_ticker_infomkr:
            combined_volume = combined_ticker_infomkr[reverse_symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infomkr[reverse_symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infomkr[reverse_symbol]['volume'] = combined_volume
            combined_ticker_infomkr[reverse_symbol]['last_price'] = np.dot(
                [combined_ticker_infomkr[reverse_symbol]['last_price'], ticker['last_price']], combined_weights)
            combined_ticker_infomkr[reverse_symbol]['high'] = np.dot(
                [combined_ticker_infomkr[reverse_symbol]['high'], ticker['low']], combined_weights)
            combined_ticker_infomkr[reverse_symbol]['low'] = np.dot(
                [combined_ticker_infomkr[reverse_symbol]['low'], ticker['high']], combined_weights)
            combined_ticker_infomkr[reverse_symbol]['open'] = np.dot(
                [combined_ticker_infomkr[reverse_symbol]['open'], ticker['open']], combined_weights)
        else:
            combined_ticker_infomkr[symbol] = ticker

    for basket in baskets:
        tbtcvolume_info, tbtccurrencyvolume = getcurrencyvolumeinfo(basket, volblock, latestblock, 1440, "tBTC.vETH")
        basket_addr_tbtc = get_currencyid_by_ticker(basket)
        if tbtcvolume_info is not None:
            for pair in tbtcvolume_info:
                # Remove .vETH suffix and 'v' prefix from currency names
                if pair['currency'] == "Bridge.vETH" or pair['convertto'] == "Bridge.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                elif pair['currency'] == "NATI.vETH" or pair['convertto'] == "NATI.vETH":
                    currency = pair['currency']
                    convertto = pair['convertto']
                else:
                    currency = pair['currency'].replace(".vETH", "").lstrip('v')
                    convertto = pair['convertto'].replace(".vETH", "").lstrip('v')

                    if currency.lower() == "tbtc":
                        currency = "TBTC"
                    if convertto.lower() == "tbtc":
                        convertto = "TBTC"

                if currency == "TBTC" or convertto == "TBTC":
                    # Reverse currency and convertto in the pair
                    if currency == "Bridge.vETH" or convertto == "Bridge.vETH":
                        currency_pair = f"Bridge.vETH_TBTC" if currency == "Bridge.vETH" else f"{convertto}_TBTC"
                    else:
                        currency_pair = f"{convertto}_{currency}"
                    weights = pair['volume'] / np.sum(pair['volume'])
                    # Invert values if VRSC is the quote currency (second position)
                    if convertto == "TBTC":
                        volume = pair['volume']
                        last = np.dot(weights, 1 / pair['close']) / np.sum(weights)
                        high = np.dot(weights, 1 / pair['high']) / np.sum(weights)
                        low = np.dot(weights, 1 / pair['low']) / np.sum(weights)
                        openn = np.dot(weights, 1 / pair['open']) / np.sum(weights)
                    else:
                        volume = pair['volume']
                        last = np.dot(weights, pair['close']) / np.sum(weights)
                        high = np.dot(weights, pair['high']) / np.sum(weights)
                        low = np.dot(weights, pair['low']) / np.sum(weights)
                        openn = np.dot(weights, pair['open']) / np.sum(weights)
                    base_currency, target_currency = currency_pair.split("_")
                    ticker_infotbtc.append({
                        'ticker_id': currency_pair,
                        'base_currency': base_currency,
                        'target_currency': target_currency,
                        'pool_id': basket_addr_tbtc,
                        'volume': volume,
                        'liquidity_in_usd': result * volume,
                        'last_price': last,
                        'high': high,
                        'low': low,
                        'open': openn
                    })
        
    # Combine reverse pairs
    combined_ticker_infotbtc = {}
    for ticker in ticker_infotbtc:
        symbol = ticker['ticker_id']
        reverse_symbol = "-".join(symbol.split("-")[::-1])
        if symbol in combined_ticker_infotbtc:
            combined_volume = combined_ticker_infotbtc[symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infotbtc[symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infotbtc[symbol]['volume'] = combined_volume
            combined_ticker_infotbtc[symbol]['last_price'] = np.dot(
                [combined_ticker_infotbtc[symbol]['last_price'], ticker['last_price']], combined_weights)
            combined_ticker_infotbtc[symbol]['high'] = np.dot(
                [combined_ticker_infotbtc[symbol]['high'], ticker['high']], combined_weights)
            combined_ticker_infotbtc[symbol]['low'] = np.dot(
                [combined_ticker_infotbtc[symbol]['low'], ticker['low']], combined_weights)
            combined_ticker_infotbtc[symbol]['open'] = np.dot(
                [combined_ticker_infotbtc[symbol]['open'], ticker['open']], combined_weights)
        elif reverse_symbol in combined_ticker_infotbtc:
            combined_volume = combined_ticker_infotbtc[reverse_symbol]['volume'] + ticker['volume']
            combined_weights = np.array([combined_ticker_infotbtc[reverse_symbol]['volume'], ticker['volume']]) / combined_volume
            combined_ticker_infotbtc[reverse_symbol]['volume'] = combined_volume
            combined_ticker_infotbtc[reverse_symbol]['last_price'] = np.dot(
                [combined_ticker_infotbtc[reverse_symbol]['last_price'], ticker['last_price']], combined_weights)
            combined_ticker_infotbtc[reverse_symbol]['high'] = np.dot(
                [combined_ticker_infotbtc[reverse_symbol]['high'], ticker['low']], combined_weights)
            combined_ticker_infotbtc[reverse_symbol]['low'] = np.dot(
                [combined_ticker_infotbtc[reverse_symbol]['low'], ticker['high']], combined_weights)
            combined_ticker_infotbtc[reverse_symbol]['open'] = np.dot(
                [combined_ticker_infotbtc[reverse_symbol]['open'], ticker['open']], combined_weights)
        else:
            combined_ticker_infotbtc[symbol] = ticker


    final_ticker_infovrsc = list(combined_ticker_infovrsc.values())
    final_ticker_infodai = list(combined_ticker_infodai.values())
    final_ticker_infoeth = list(combined_ticker_infoeth.values())
    final_ticker_infomkr = list(combined_ticker_infomkr.values())
    final_ticker_infotbtc = list(combined_ticker_infotbtc.values())
    return final_ticker_infovrsc, final_ticker_infodai, final_ticker_infoeth, final_ticker_infomkr, final_ticker_infotbtc
