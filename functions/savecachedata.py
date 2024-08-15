import os
import json

def cacheinfo(data, filename="cachedmarketdata.json"):
    folder = "cached"
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    if data:
        with open(filepath, 'w') as f:
            json.dump(data, f)
        return data
    else:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                cached_data = json.load(f)
            return cached_data
        else:
            return []