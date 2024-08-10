from functions.send_request import send_request
from var.vars import RPCURL

def getallbaskets():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencyconverters",
            "params": ["VRSC"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    if isinstance(response, dict) and 'result' in response and isinstance(response['result'], list):
        fully_qualified_names = []
        i_strings = []
        for item in response['result']:
            fully_qualified_name = item.get("fullyqualifiedname")
            i_string = next((key for key in item if key.startswith('i') and len(key) == 34), None)
            if fully_qualified_name and i_string:
                fully_qualified_names.append(fully_qualified_name)
                i_strings.append(i_string)
        return fully_qualified_names, i_strings
    else:
        print("Unexpected response format")
        return [], []