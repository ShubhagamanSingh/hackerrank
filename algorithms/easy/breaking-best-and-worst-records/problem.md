# Breaking the Records

[Read the full problem on HackerRank](https://www.hackerrank.com/challenges/breaking-best-and-worst-records/problem)

- **Category:** Algorithms
- **Difficulty:** Easy

## Problem in your own words

Process a player's game scores in order. The first score sets both the highest and lowest records. Count how many later scores exceed the current high and how many fall below the current low. Scores equal to a record do not count.

## Input and output

The function receives `scores`, an array of game scores, and returns `[high_breaks, low_breaks]`.

## Example

For `scores = [10, 5, 20, 20, 4]`, the high record changes once and the low record changes twice. The result is `[1, 2]`.

## Solution

See [solution.py](solution.py).
