"""
A minimal example which demonstrates how parallel computations can be done
within classes and with shared NumPy arrays.
"""

from parallel import mapp
from shmarray import zeros

class Foo:
	def __init__(self):
		self.values = zeros(10)

	def sequential(self):
		for i in range(self.values.size):
			self.values[i] = i

	def parallel(self):
		def parfor(i):
			self.values[i] = i
		mapp(parfor, range(self.values.size))

if __name__ == '__main__':
	foo = Foo()
	foo.parallel()

	def f():
		print 'x'
	mapp(f, range(10))

	print foo.values
