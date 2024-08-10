import requests

def send_request(method, url, headers, data):
    response = requests.request(method, url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# def send_request(method, url, headers, data):
#     response = requests.request(method, url, headers=headers, json=data, auth=(RPCUSER, RPCPASS))
#     return response.json()