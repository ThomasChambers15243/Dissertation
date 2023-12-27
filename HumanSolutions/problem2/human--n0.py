def P3(inputs):
    if not inputs:
        return 0

    max_count = -1
    start_idx = 0
    for idx, char in enumerate(inputs,1):
        print( "> ", start_idx, idx, inputs[start_idx], inputs[idx] )
        if inputs[start_idx] != inputs[idx]:
            max_count = max( idx - start_idx, max_count )
            start_idx = idx
    return max_count