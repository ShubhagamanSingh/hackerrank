def breakingRecords(scores):
    # First game's score establishes both initial records.
    highest = lowest = scores[0]

    # Counters for record breaks.
    high_breaks = 0
    low_breaks = 0

    # Start from the second game.
    for score in scores[1:]:
        if score > highest:
            highest = score
            high_breaks += 1

        elif score < lowest:
            lowest = score
            low_breaks += 1

    # Index 0 -> most points record breaks
    # Index 1 -> least points record breaks
    return [high_breaks, low_breaks]