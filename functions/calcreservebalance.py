from functions.getimports import get_imports
from functions.tickerfunc import get_ticker_by_currency_id

def calculate_reserve_balance(currencyid: str, currency: str):
    total_reservein = 0.0
    total_reserveout = 0.0
    json_data = get_imports(currency)

    try:
        results = json_data["result"]
        for result in results:
            importnotarization = result["importnotarization"]
            currencystate = importnotarization["currencystate"]
            currencies = currencystate["currencies"]

            for currency_id, currency_data in currencies.items():
                if currency_id == str(currencyid):
                    if "reservein" in currency_data:
                        total_reservein += currency_data["reservein"]
                    if "reserveout" in currency_data:
                        total_reserveout += currency_data["reserveout"]
        ticker = get_ticker_by_currency_id(str(currencyid))
        return {
            "currencyid": ticker,
            "currency": currency,
            "reservein": total_reservein,
            "reserveout": total_reserveout
        }
    except KeyError as e:
        return {"error": f"KeyError: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}