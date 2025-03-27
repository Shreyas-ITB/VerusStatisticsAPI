import os
import json

def cacheinfo(data, filename="cachedmarketdata.json"):
    def should_exclude(existing_pairs, new_pair):
        # Create a sorted tuple of the new pair symbol to identify unique pairs
        new_pair_sorted = tuple(sorted(new_pair["symbol"].split("-")))
        for pair in existing_pairs:
            # Create a sorted tuple of the existing pair symbol
            existing_pair_sorted = tuple(sorted(pair["symbol"].split("-")))
            if existing_pair_sorted == new_pair_sorted:
                return True
        return False
    folder = "cached"
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    if data:
        filtered_data = []
        for item in data:
            if not should_exclude(filtered_data, item):
                filtered_data.append(item)
        modified_data = []
        for item in filtered_data:
            modified_item = item.copy()
            modified_item["volume"] = 0
            modified_data.append(modified_item)
        with open(filepath, 'w') as f:
            json.dump(modified_data, f, indent=4)
        return filtered_data
    else:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                cached_data = json.load(f)
            return cached_data
        else:
            return []

def cacheinfonew(data, filename="cachednewmarketdata.json"):
    def should_exclude(existing_pairs, new_pair):
        # Create a sorted tuple of the new pair symbol to identify unique pairs
        new_pair_sorted = tuple(sorted(new_pair["symbol"].split("-")))
        for pair in existing_pairs:
            # Create a sorted tuple of the existing pair symbol
            existing_pair_sorted = tuple(sorted(pair["symbol"].split("-")))
            if existing_pair_sorted == new_pair_sorted:
                return True
        return False
    folder = "cached"
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    if data:
        filtered_data = []
        for item in data:
            if not should_exclude(filtered_data, item):
                filtered_data.append(item)
        modified_data = []
        for item in filtered_data:
            modified_item = item.copy()
            modified_item["volume"] = 0
            modified_data.append(modified_item)
        with open(filepath, 'w') as f:
            json.dump(modified_data, f, indent=4)
        return filtered_data
    else:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                cached_data = json.load(f)
            return cached_data
        else:
            return []
        
def cacheinfo_newendpoint(data, filename="cachedmarketdata_newendpoint.json"):
    def should_exclude(existing_pairs, new_pair):
        # Create a sorted tuple of the new pair symbol to identify unique pairs
        new_pair_sorted = tuple(sorted(new_pair["ticker_id"].split("-")))
        for pair in existing_pairs:
            # Create a sorted tuple of the existing pair symbol
            existing_pair_sorted = tuple(sorted(pair["ticker_id"].split("-")))
            if existing_pair_sorted == new_pair_sorted:
                return True
        return False
    folder = "cached"
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    if data:
        filtered_data = []
        for item in data:
            if not should_exclude(filtered_data, item):
                filtered_data.append(item)
        modified_data = []
        for item in filtered_data:
            modified_item = item.copy()
            modified_item["volume"] = 0
            modified_data.append(modified_item)
        with open(filepath, 'w') as f:
            json.dump(modified_data, f, indent=4)
        return filtered_data
    else:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                cached_data = json.load(f)
            return cached_data
        else:
            return []

def cacheinfonew_newendpoint(data, filename="cachednewmarketdata_newendpoint.json"):
    def should_exclude(existing_pairs, new_pair):
        # Create a sorted tuple of the new pair symbol to identify unique pairs
        new_pair_sorted = tuple(sorted(new_pair["ticker_id"].split("-")))
        for pair in existing_pairs:
            # Create a sorted tuple of the existing pair symbol
            existing_pair_sorted = tuple(sorted(pair["ticker_id"].split("-")))
            if existing_pair_sorted == new_pair_sorted:
                return True
        return False
    folder = "cached"
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    if data:
        filtered_data = []
        for item in data:
            if not should_exclude(filtered_data, item):
                filtered_data.append(item)
        modified_data = []
        for item in filtered_data:
            modified_item = item.copy()
            modified_item["volume"] = 0
            modified_data.append(modified_item)
        with open(filepath, 'w') as f:
            json.dump(modified_data, f, indent=4)
        return filtered_data
    else:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                cached_data = json.load(f)
            return cached_data
        else:
            return []
