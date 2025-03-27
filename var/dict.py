latestblock = []
reservecurrencies = []
mempool_res = []
rawtransaction = []
decodedrawtransaction = []
mempool_count = 0
res = []

arr_currencies = [
    {"currencyid": "iQ3NQaPQRtJ4KamYkWEJfuiggkCbnmFW1z", "ticker": "VerusNFT"},
    {"currencyid": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV", "ticker": "VRSC"},
    {"currencyid": "i3f7tSctFkiPpiedY8QR5Tep9p4qDVebDx", "ticker": "Bridge.vETH"},
    {"currencyid": "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X", "ticker": "vETH"},
    {"currencyid": "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM", "ticker": "DAI.vETH"},
    {"currencyid": "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4", "ticker": "MKR.vETH"},
    {"currencyid": "iEnQEjjozf1HZkqFT9U4NKnzz1iGZ7LbJ4", "ticker": "TRAC.vETH"},
    {"currencyid": "iJczmut8fHgRvVxaNfEPm7SkgJLDFtPcrK", "ticker": "vLINK.vETH"},
    {"currencyid": "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd", "ticker": "vUSDC.vETH"},
    {"currencyid": "i9oCSqKALwJtcv49xUKS2U2i79h1kX6NEY", "ticker": "vUSDT.vETH"},
    {"currencyid": "iNtUUdjsqV34snGZJerAvPLaojo6tV9sfd", "ticker": "vMars4"},
    {"currencyid": "iS3NjE3XRYWoHRoovpLhFnbDraCq7NFStf", "ticker": "vwBTC.vETH"},
    {"currencyid": "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU", "ticker": "tBTC.vETH"},
    {"currencyid": "i4YYnZvzhaQPJvQsVMsDPjPouLSEpZS6vP", "ticker": "OIL.vETH"},
    {"currencyid": "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE", "ticker": "vEURC.vETH"},
    {"currencyid": "iSUD6kGQKDaFUfK6EMYRtR4SNU4wjhEpMi", "ticker": "vOVERRIDE.vETH"},
    {"currencyid": "i9A4wBXUastzupqZwkich4zhCtziZS1JoF", "ticker": "BAT.vETH"},
    {"currencyid": "iExBJfZYK7KREDpuhj6PzZBzqMAKaFg7d2", "ticker": "vARRR"},
    {"currencyid": "iSYJ5L91bURKemiuALK1uBUXad3ZKCpDX7", "ticker": "paxg.vETH"},
    {"currencyid": "i7eFvyL44S2iWz9EZjd6HTaBioFqhALcdi", "ticker": "xaut.vETH"},
    {"currencyid": "iL62spNN42Vqdxh8H5nrfNe8d6Amsnfkdx", "ticker": "NATI"},
    {"currencyid": "i4Xr5TAMrDTD99H69EemhjDxJ4ktNskUtc", "ticker": "Switch" },
    {"currencyid": "i9kVWKU2VwARALpbXn4RS9zvrhvNRaUibb", "ticker": "Kaiju"},
    {"currencyid": "iHax5qYQGbcMGqJKKrPorpzUBX2oFFXGnY", "ticker": "Pure"},
    {"currencyid": "iD5WRg7jdQM1uuoVHsBCAEKfJCKGs1U3TB", "ticker": "Bridge.vARRR"},
    {"currencyid": "i6j1rzjgrDhSmUYiTtp21J8Msiudv5hgt9", "ticker": "Bridge.vDEX"},
    {"currencyid": "i3nokiCTVevZMLpR3VmZ7YDfCqA5juUqqH", "ticker": "Bridge.CHIPS"},
    {"currencyid": "i6SapneNdvpkrLPgqPhDVim7Ljek3h2UQZ", "ticker": "SUPERNET"},
    {"currencyid": "i9nLSK4S1U5sVMq4eJUHR1gbFALz56J9Lj", "ticker": "scrvUSD.vETH"},
    {"currencyid": "iAik7rePReFq2t7LZMZhHCJ52fT5pisJ5C", "ticker": "vYIELD"},
    {"currencyid": "iH37kRsdfoHtHK5TottP1Yfq8hBSHz9btw", "ticker": "NATI🦉"},
    {"currencyid": "iHnYAmrS45Hb8GVgyzy7nVQtZ5vttJ9N3X", "ticker": "SUPERVRSC"},
    {"currencyid": "iJ3WZocnjG9ufv7GKUA4LijQno5gTMb7tP", "ticker": "CHIPS"},
    {"currencyid": "iHog9UCTrn95qpUBFCZ7kKz7qWdMA8MQ6N", "ticker": "vDEX"},
    {"currencyid": "iFrFn9b6ctse7XBzcWkRbpYMAHoKjbYKqG", "ticker": "SUPER🛒"},
    {"currencyid": "iCDjBN71SbSppgsNTpwwMBT69399DpV4hA", "ticker": "Kek🐸"},
    {"currencyid": "i5VVBEi6efBrXMaeqFW3MTPSzbmpNLysGR", "ticker": "PEPE"},
]

arr_token_contracts = {
    "0x18084fbA666a33d37592fA2633fD49a74DD93a88": 18,  # tBTC
    "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2": 18,  # MKR
    "0xdAC17F958D2ee523a2206206994597C13D831ec7": 6,   # USDT
    "0x1aBaEA1f7C830bD89Acc67eC4af516284b1bC33c": 6,   # EURC
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48": 6    # USDC
}

arr_token_holders = [
    "0x71518580f36FeCEFfE0721F06bA4703218cD7F63",
    "0x197E90f9FAD81970bA7976f33CbD77088E5D7cf7"
]

COINGECKO_GETCURRENCYCONVERTERS_CURRENCY_FORMATS = {
    "Bridge.vETH": ["VRSC", "DAI", "MKR", "ETH"],
    "NATI🦉": ["VRSC", "TBTC", "ETH", "NATI.vETH"],
    "Pure": ["VRSC", "TBTC"],
    "SUPERVRSC": ["VRSC", "SUPERNET"],
    "SUPER🛒": ["SUPERNET", "VRSC", "TBTC", "ETH", "ARRR", "DEX", "CHIPS", "scrvUSD"],
    "vYIELD": ["VRSC", "scrvUSD"],
    "Kaiju": ["VRSC", "USDT", "ETH", "TBTC"],
    "Switch": ["VRSC", "DAI", "USDC", "EURC"],
    "NATI": ["VRSC", "NATI.vETH"],
    "Bridge.CHIPS": ["VRSC", "CHIPS"],
    "Bridge.vARRR": ["VRSC", "ARRR", "BridgevETH", "TBTC"],
    "Bridge.vDEX": ["VRSC", "DEX", "ETH", "DAI", "TBTC"],
    "whales": ["VRSC"]
}
