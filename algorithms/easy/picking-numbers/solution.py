def pickingNumbers(a):
    # Frequency of each possible value (0 <= a[i] < 100)
    freq = [0] * 100

    for num in a:
        freq[num] += 1

    max_length = 0

    # Valid subset can contain only x and x + 1
    # because the absolute difference must be <= 1.
    for x in range(99):
        max_length = max(max_length, freq[x] + freq[x + 1])

    return max_length