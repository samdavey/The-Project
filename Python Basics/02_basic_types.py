# This is just a bunch of basic routines and building blocksa while I learn
# the syntax and functrions of Python.
# Loosely based on the Python for Data Science examples.

# Lists
print('==================================================')
print('= Lists                                          =')
print('= Ordered, mutable collections. Multi-type.      =')
print('==================================================')
test_list = [1,2,3,5,8,13,21,'thirty four',55.0]
print('test_list is:\t', test_list) # whole list
print('len(test_list)\t',len(test_list))
print('\nList index and slicing\n')
print('test_list[0]\t', test_list[0]) # first element by index
print('test_list[:]\t', test_list[:]) # whole list as a slice
print('test_list[3:4]\t', test_list[3:4]) # slice
print('test_list[2:]\t', test_list[2:]) # slice 2..
print('test_list[:3]\t', test_list[:3]) # slice ..3
print('test_list[-0]\t', test_list[-0]) # FIST BECAUSE IT WRAPS>
print('test_list[-1]\t', test_list[-1]) # last
print('test_list[::2]\t', test_list[::2]) # all, step by 2
print('test_list[::-1]\t', test_list[::-1]) # step -1 = reverse
print('\nList setting\n')
test_list.append('eighty-nine')
print("test_list.append('eighty-nine')", test_list)
test_list[0] = 100
print('test_list[0] = 100\t',test_list)
test_list[1:3] = [99,98]
print('test_list[1:3] = [99,98]', test_list)

# Tuples
print('\n\n')
print('==================================================')
print('= Tuples                                         =')
print('= Ordered, immutable, Multi-type                 =')
print('==================================================')
test_tuple = (1, 2, 3)
print('test_tuple = (1, 2, 3)')
print('test_tuple is:\t', test_tuple)
test_tuple2 = 4, 5, 6
print('test_tuple2 = 4, 5, 6')
print('test_tuple2 is:\t', test_tuple2)
print('\nTuple Indexing\n')
print('len(test_tuple)\t', len(test_tuple))
print('test_tuple[0]\t', test_tuple[0])
print('test_tuple[0:3]\t', test_tuple[0:3])
print('test_tuple[1:]\t', test_tuple[1:])
print('test_tuple[:1]\t', test_tuple[:1])
print('test_tuple[-1]\t', test_tuple[-1])

# Dictionaries
print('\n\n')
print('==================================================')
print('= Dictionaries                                   =')
print('= Unordered, mutable, key:value pairs            =')
print('==================================================')
test_dictionary = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'ten':10}
print('test_dictionary = {"one":1, "two":2, "three":3, "four":4, "five":5, "ten:10"}')
print('test_dictionary is:\t', test_dictionary)
print('len(test_dictionary)', len(test_dictionary))
print('\nDictionary indexing\n')
print("test_dictionary['one']", test_dictionary['one'])
print('\nDictionary editing\n')
test_dictionary['ninety-nine'] = 99
print("test_dictionary['ninety-nine'] = 99\t", test_dictionary)

# Sets
print('\n\n')
print('==================================================')
print('= Sets                                           =')
print('= Unordered collection of unique items           =')
print('==================================================')
test_set_primes = {2, 3, 5, 7}
test_set_odds = {1, 3, 5, 7, 9}
print('test_set_primes = {2, 3, 5, 7}\t', test_set_primes)
print('test_set_odds = {1, 3, 5, 7, 9}\t', test_set_odds)
print('Union (|): test_set_primes | test_set_odds', test_set_primes | test_set_odds)
print('test_set_primes.union(test_set_odds)\t', test_set_primes.union(test_set_odds))
print('Intersection (&): test_set_primes & test_set_odds', test_set_primes & test_set_odds)
print('test_set_primes.intersection(test_set_odds)\t', test_set_primes.intersection(test_set_odds))
print('Difference (-): test_set_primes - test_set_odds', test_set_primes - test_set_odds)
print('test_set_primes.difference(test_set_odds)\t', test_set_primes.difference(test_set_odds))
print('Symmetric Difference (^): test_set_primes ^ test_set_odds', test_set_primes ^ test_set_odds)
print('test_set_primes.symmetric_difference(test_set_odds)\t', test_set_primes.symmetric_difference(test_set_odds))
