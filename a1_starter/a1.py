'''a1.py.
CSE 415, Winter 2020, Assignment 1
Saasha Mor 
'''

import math
def is_multiple_of_3(n):
  "Return True if n is a multiple of 3; False otherwise."
  return bool (n % 3 == 0)

def isPrime(n):
  if(n <= 1): 
        return False
  if(n <= 3): 
        return True
  if(n % 2 == 0 or n % 3 == 0): 
        return False
      
  for i in range(5,int(math.sqrt(n) + 1), 6):
      if(n % i == 0 or n % (i + 2) == 0): 
          return False
      
  return True


def next_prime(m):
  '''Return an integer p that is prime, and such that
  p > m, and there does not exist any n, with n > m
  and n < p such that n is prime. In other words, return
  the next prime number after m.'''
  if (m <= 1): 
        return 2
  prime = m
  found = False
  while(not found): 
    prime = prime + 1 
    if(isPrime(prime) == True): 
        found = True
  return prime 

import wordscraper
url = "http://courses.cs.washington.edu/courses/cse415/20wi/desc.html"
def empirical_probabilities(url):
  '''Return a dictionary whose keys are words in a reference vocabulary,
  and whose values are PROBABILITIES of those words, based on the
  number of occurrences on the webpage at the given URL.'''
  html_bytes = wordscraper.fetch()
  word_list = wordscraper.html_bytes_to_word_list(html_bytes)
  count_dict = wordscraper.make_word_count_dict(word_list)
  # pairs_list = wordscraper.to_sorted_pairs_list(count_dict)
  # Print out the word-count pairs, in alphabetical order.
#  print("Words and their counts from the fetched page:")
#  for (word, count) in pairs_list:
#    print(word, '\t', count)

  # Print out the word-count pairs, in alphabetical order,
  # again, but now using only the reference vocabulary words.
  ref_counts = wordscraper.init_counts_for_ref_vocab()
  wordscraper.combine_page_counts_with_ref_counts(count_dict, ref_counts)
  sorted_wordlist = list(ref_counts.keys())
  sorted_wordlist.sort()
  #print("-----------------------------------------------------")
  #print("Reference vocabulary words, and their biased counts in the fetched page:")
  final_dict = ref_counts
  for word in sorted_wordlist:
      final_dict[word] = 1.0 - math.exp(- ref_counts[word])
  return final_dict

#print(empirical_probabilities(url))
