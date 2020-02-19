'''EightPuzzleWithHamming.py
by Saasha Mor
UWNetID: saashm
Student number: 1738927

Assignment 2, in CSE 415, Winter 2020.

This file contains heurisic definition for the Eigh Puzzle
With Hamming distance. It counts the count the number of
tiles out of place, but not the blank, in order to
maintain admissibility
'''

from EightPuzzle import *
def h(s):
    count = 0
    for i, t1 in enumerate(s.b):
        for j, t2 in enumerate(t1):
            if t2 == 0:
                continue
            else:
                row = (t2) // 3
                col = (t2) % 3
                count += abs(row - i) + abs(col - j)
    return count