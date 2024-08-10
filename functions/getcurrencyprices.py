import yfinance as yf
from decimal import Decimal

def get_dai_price():
    dai = yf.Ticker("DAI-USD")
    data = dai.history(period="1d")
    return Decimal(data['Close'].iloc[-1])

def get_eth_price():
    eth = yf.Ticker("ETH-USD")
    data = eth.history(period="1d")
    return Decimal(data['Close'].iloc[-1])

def get_verus_coin_price():
    # Get Verus Coin price from Yahoo Finance
    verus = yf.Ticker("VRSC-USD")  # Replace with correct symbol if needed
    return Decimal(verus.history(period="1d")["Close"].iloc[-1])