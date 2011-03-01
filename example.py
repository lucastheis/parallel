"""
A minimal example which demonstrates how parallel computations can be done
within classes and with shared NumPy arrays.
"""

from parallel import map
from shmarray import zeros

class Foo:
	def __init__(self):
		self.values = zeros(10)

	def sequential(self):
		for i in range(self.values.size):
			self.values[i] = i

	def parallel(self):
		def function(i):
			self.values[i] = i
		map(function, range(self.values.size))

if __name__ == '__main__':
	foo = Foo()
	foo.parallel()

	print foo.values
