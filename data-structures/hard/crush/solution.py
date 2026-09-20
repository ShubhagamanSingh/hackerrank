def arrayManipulation(n, queries):
    # Difference array:
    # For each query [a, b, k], add k at a
    # and subtract k immediately after b.
    diff = [0] * (n + 2)

    for a, b, k in queries:
        diff[a] += k
        diff[b + 1] -= k

    max_value = 0
    current = 0

    # Prefix sum reconstructs the final array values.
    for i in range(1, n + 1):
        current += diff[i]
        max_value = max(max_value, current)

    return max_value