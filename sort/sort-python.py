#!/usr/bin/env python

import random

size = 10000
strings = []

i = 0

while i < size:

    length = random.randint(0,1000)
    my_string = length * '!'
    strings.append(my_string)

    i += 1


sorted_by_length = sorted(strings, key=lambda item: len(item))
