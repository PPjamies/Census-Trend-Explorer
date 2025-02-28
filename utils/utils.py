def remove_none_values(arr: []):
    arr = {k: v for k, v in arr.items() if v is not None}
    return arr
