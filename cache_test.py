###########################################################
# cache_test.py
# 	Using test driven development, this program tests all 
#	basic cases of the n-way set associative cache and its 
# 	replacement algorithms and the creation of each item 
# 	for the cache. There is also a long trial that tries
# 	to mimic a system by inserting random variables.
###########################################################

# import custom replacement algorithms when used
from cache_setup import CacheSetup
from cache_algorithm import LRU_replacement, MRU_replacement
from random import randint

class Foo:
    def __init__(self, foo):
        self.foo = foo

def setup_test():
	# verifying size and associativity
	cache = CacheSetup(10, 10, LRU_replacement())
	assert cache.get_cap() == 10
	assert cache.get_assoc() == 10

	# verify setting works, with key and value fits for all 
	# immutable types int, floats, strings, tuples, classes
	my_class = Foo('class')
	my_tuple = (1, 2)
	cache.set_item(1, 1)
	cache.set_item(3.14159, 3.14159)
	cache.set_item('string', 'string')
	cache.set_item(my_class, my_class)
	cache.set_item(my_tuple, my_tuple)
	assert cache.get_item(1).get_val() == 1
	assert cache.get_item(3.14159).get_val() == 3.14159
	assert cache.get_item('string').get_val() == 'string'
	assert cache.get_item(my_class).get_val() == my_class
	assert cache.get_item(my_tuple).get_val() == my_tuple

	# verify removing works
	cache.remove_item(1)
	cache.remove_item(3.14159)
	cache.remove_item('string')
	cache.remove_item(my_class)
	cache.remove_item(my_tuple)
	assert cache.is_contained(1) == False
	assert cache.is_contained(3.14159) == False
	assert cache.is_contained('string') == False
	assert cache.is_contained(my_class) == False
	assert cache.is_contained(my_tuple) == False

	print("Passed basic setup tests.")

def MRU_test():
	cache = CacheSetup(2, 2, MRU_replacement())

	# verify initial insertion works
	cache.set_item(1, 'val1')
	cache.set_item(2, 'val2')
	assert cache.get_item(1).get_val() == 'val1'
	assert cache.get_item(2).get_val() == 'val2'

	# verify that both caches are full
	cache.set_item(3, 'val3')
	cache.set_item(4, 'val4')
	assert cache.get_item(3).get_val() == 'val3'
	assert cache.get_item(4).get_val() == 'val4'

	# verify that the most recently used item is evicted for 
	# the new entry after hashed into the set
	cache.set_item(5, 'val5')
	assert cache.get_item(5).get_val() == 'val5'
	assert cache.is_contained(3) == False

	print("Passed basic MRU replacement algorithm tests.")

def LRU_test():
	cache = CacheSetup(2, 2, LRU_replacement())

	# verify initial insertion works
	cache.set_item(1, 'val1')
	cache.set_item(2, 'val2')
	assert cache.get_item(1).get_val() == 'val1'
	assert cache.get_item(2).get_val() == 'val2'

	# verify that both caches are full
	cache.set_item(3, 'val3')
	cache.set_item(4, 'val4')
	assert cache.get_item(3).get_val() == 'val3'
	assert cache.get_item(4).get_val() == 'val4'

	# verify that the least recently used item is evicted for 
	# the new entry after hashed into the set
	cache.set_item(5, 'val5')
	assert cache.get_item(5).get_val() == 'val5'
	assert cache.is_contained(1) == False

	print("Passed basic LRU replacement algorithm tests.")

def long_trial():
	# LRU trial; debug data printed
	LRU_cache = CacheSetup(10, 10, LRU_replacement())
	for i in range(500):
		LRU_cache.set_item(randint(0, 100), 'foo')
	LRU_cache.debug_print()

	# MRU trial; debug data printed
	MRU_cache = CacheSetup(10, 10, MRU_replacement())
	for i in range(500):
		MRU_cache.set_item(randint(0, 100), 'foo')
	MRU_cache.debug_print()

if __name__ == "__main__": 
	setup_test()
	MRU_test()
	LRU_test()
	for i in range(200):
		long_trial()

