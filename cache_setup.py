##########################################################
# cache_setup.py:
#	This program sets up all of the data structures and
#	objects needed to create an n-way set associative cache
##########################################################

from datetime import datetime
from collections import defaultdict
import cache_algorithm
import sys

##########################################################
# CacheSetup:
#	This class creates the initial cache, declaring the 
#	size and number of sets. Each item is hashed and placed 
#	accordingly to each set.
##########################################################
class CacheSetup:

	##########################################################
	# cap: The number of sets in the cache
	# assoc: The associativity of the cache; the set size
	# set: The data structure to hold all of the sets
	# alg: The replacement algorithm used
	##########################################################

	def __init__(self, cap, assoc, alg):
		self.__cap = cap
		self.__assoc = assoc
		self.__set = defaultdict(lambda: Cache(cap, alg))
		self.__alg = alg

	def get_cap(self):
		return self.__cap
  
	def get_assoc(self):
		return self.__assoc  
	
	def get_set(self):
		return self.__set

	def is_contained(self, key):
		for cache in self.__set.values():
			if key in cache.get_cache():
				return True
		return False

	def set_item(self, key, val):
		hashed_key = hash(key) % self.__assoc
		self.__set[hashed_key].set_item(key, val)

	def get_item(self, key):
		hashed_key = hash(key) % self.__assoc
		if self.is_contained(key) == True:
			return self.__set[hashed_key].get_item(key)

	def remove_item(self, key):
		hashed_key = hash(key) % self.__assoc
		if self.is_contained(key) == True:
			self.__set[hashed_key].remove_item(key)
		else:
			return -1

	# debugging print: long format
	def debug_print(self):
		print('\n')
		print("{0:^28} {1:>15} {2:>15} {3:>20} {4:>15}".format(
			'Time Visited:',
			'Set Key:',
			'Item Key:',
			'Item Value:',
			'Frequency:'
		))

		print("=" * 100)

		for set_key, set_val in self.__set.items():
			for item_key, item_val in set_val.get_cache().items():
				print("{0} {1:>15} {2:>15} {3:>20} {4:>15}".format(
					item_val.get_visited(), 
					set_key, item_key, 
					item_val.get_val(), 
					item_val.get_freq(),
				))
		print('\n')

##########################################################
# Cache:
#	This class is the individual set in the cache, and puts  
#	the actual cached items into these sets and puts cached
#	items in sorted order in a list that is later referenced
##########################################################
class Cache:

	##########################################################
	# cap: The number of items the set can hold
	# cache: The set itself, with its keys and values
	# ordered_queue: List to keep sorted CacheItems
	# alg: The replacement algorithm used
	# cur_size: The current size of the set
	##########################################################

	def __init__(self, cap, alg):
		self.__cap = cap
		self.__cache = defaultdict()
		self.__ordered_queue = []
		self.__alg = alg
		self.__cur_size = 0

	def pop_ordered(self):
		return self.__alg.replacement_alg(self.__ordered_queue).get_key()

	def push_ordered(self, item):
		self.__ordered_queue.append(item)
			

	def get_cache(self):
		return self.__cache

	def set_item(self, key, val):
		if self.__cur_size >= self.__cap:
			index = self.__cap - 1
		elif self.__cur_size < 0:
			index = 0
		else:
			index = self.__cur_size
		if key in self.__cache:
			try:
				self.__ordered_queue.pop(self.__cache[key].get_index())
				self.__cache[key].set_index(index - 1)
				self.__cache[key].set_visited(datetime.now())
				self.__cache[key].inc_freq()
				self.push_ordered(self.__cache[key])
			except KeyError:
				print >> sys.stderr,"KeyError 1"
		else:
			if self.__cur_size >= self.__cap:
				try:
					del self.__cache[self.pop_ordered()]
				except KeyError:
					print >> sys.stderr, "The key", self.pop_ordered(), "does not exist."
				self.__cur_size = self.__cur_size - 1
			self.__cache[key] = CacheItem(key, val, index)
			self.push_ordered(self.__cache[key])
			self.__cur_size = self.__cur_size + 1

	def get_item(self, key):
		return self.__cache[key]
	
	def remove_item(self, key):
	  	del self.__cache[key]

	def print_queue(self):
	 	print(self.__ordered_queue)

##########################################################
# CacheItem:
#	This class is the item with the data put in each set.
#	Any object or datatype can be a CacheItem. Each item
#	is referenced from the queue via an index.
##########################################################
class CacheItem:

	##########################################################
	# key: The key for the dictionary
	# val: The value associated with the key
	# index: Index to point to sorted CacheItem position
	# time_visited: The time this item was last visited
	# time_created: The time this item was created
	# freq: How often this item is visited
	##########################################################

	def __init__(self, key, val, index):
		self.__key = key
		self.__val = val
		self.__index = index
		self.time_visited = datetime.now()
		self.time_created = datetime.now()
		self.freq = 1

	def set_index(self, index):
		self.__index = index

	def get_index(self):
		return self.__index

	def set_visited(self, access):
		self.time_visited = access

	def get_visited(self):
		return self.time_visited

	def get_created(self):
		return self.time_created

	def get_key(self):
		return self.__key

	def get_val(self):
		return self.__val
    
	def inc_freq(self):
		self.freq = self.freq + 1
        
	def get_freq(self):
		return self.freq

