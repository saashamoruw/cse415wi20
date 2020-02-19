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
  '''We return the number of tiles out of place.'''
  count = 0
  goal = [[[0,1,2],[3,4,5],[6,7,8]]]
  for i in range(3):
      for j in range(3):
          if goal[i][j] != s.b[i][j]:
              count=count+1
  return count