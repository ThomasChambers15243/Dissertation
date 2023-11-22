def P6(arr1, arr2):
    combined_arr = arr1 + arr2
    combined_arr.sort(key=lambda x: (len(x), sum(ord(c) for c in x)))
    return combined_arr

def P6(arr1, arr2):
    combined_arr = arr1 + arr2
    combined_arr.sort(key=lambda x: (len(x), sum(ord(c) for c in x)))
    return combined_arr