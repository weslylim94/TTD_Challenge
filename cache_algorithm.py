##########################################################
# cache_algorithm.py:
#	This program is all of the replacement algorithms. To 
#	add a new replacement algorithm (i.e. FIFO), just add
#	a new class with the same arguments as the LRU and MRU
#	replacement classes, and change up 'item' to fit your
#	replacement algorithm needs. This is the new version 
#	where the user does not directly edit the internals of
#	the cache.
##########################################################

from operator import attrgetter
from datetime import datetime

##########################################################
# LRU_replacement:
#	This class creates the initial cache, declaring the 
#	size and number of sets
##########################################################
class LRU_replacement:

	def replacement_alg(self, ordered_queue):
		try:
			item = ordered_queue[0]
			return item
		except IndexError:
			print >> sys.stderr, 'IndexError'


##########################################################
# MRU_replacement:
#	This class creates the initial cache, declaring the 
#	size and number of sets
##########################################################
class MRU_replacement:

	def replacement_alg(self, ordered_queue):
		try:
			item = ordered_queue[-1]
			return item
		except IndexError:
			print >> sys.stderr, 'IndexError'

# To implement new replacement algorithms, maninulate item 
# to return. The attrgetter is imported to allow new algorithms
# to be evicted differently. 
# 	Example: 
#		temp = (item for item in ordered_queue)
#		item = sorted(temp, key=attrgetter('freq'))[0]
