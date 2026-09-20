def formingMagicSquare(s):
    # All possible 3x3 magic squares using numbers 1 to 9.
    magic_squares = (
        ((8, 1, 6), (3, 5, 7), (4, 9, 2)),
        ((6, 1, 8), (7, 5, 3), (2, 9, 4)),
        ((4, 9, 2), (3, 5, 7), (8, 1, 6)),
        ((2, 9, 4), (7, 5, 3), (6, 1, 8)),
        ((8, 3, 4), (1, 5, 9), (6, 7, 2)),
        ((4, 3, 8), (9, 5, 1), (2, 7, 6)),
        ((6, 7, 2), (1, 5, 9), (8, 3, 4)),
        ((2, 7, 6), (9, 5, 1), (4, 3, 8)),
    )

    # Calculate the conversion cost for each possible magic square
    # and return the minimum.
    return min(
        sum(
            abs(s[i][j] - magic[i][j])
            for i in range(3)
            for j in range(3)
        )
        for magic in magic_squares
    )