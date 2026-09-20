#!/bin/python3

import math
import os
import random
import re
import sys
from math import gcd
from functools import reduce


#
# Complete the 'getTotalX' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY a
#  2. INTEGER_ARRAY b
#

def getTotalX(a, b):
    # LCM of all elements in array a.
    # Any valid number must be a multiple of this value.
    lcm_a = reduce(lambda x, y: (x * y) // gcd(x, y), a)

    # GCD of all elements in array b.
    # Any valid number must divide this value.
    gcd_b = reduce(gcd, b)

    # If LCM(a) does not divide GCD(b),
    # no number can satisfy both conditions.
    if gcd_b % lcm_a != 0:
        return 0

    count = 0
    multiple = lcm_a

    # Check only multiples of LCM(a) up to GCD(b).
    while multiple <= gcd_b:
        if gcd_b % multiple == 0:
            count += 1
        multiple += lcm_a

    return count    
    

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    m = int(first_multiple_input[1])

    arr = list(map(int, input().rstrip().split()))

    brr = list(map(int, input().rstrip().split()))

    total = getTotalX(arr, brr)

    fptr.write(str(total) + '\n')

    fptr.close()
