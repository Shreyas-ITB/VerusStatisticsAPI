def extract_i_address(data):
    for item in data:
        for key in item.keys():
            if key.startswith('i'):
                return key
    return None