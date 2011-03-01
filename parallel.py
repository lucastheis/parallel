"""
Tools for simplified parallel processing.
"""

__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@tuebingen.mpg.de>'
__docformat__ = 'epytext'

from multiprocessing import Process, Queue
from numpy import iterable

def map(function, arguments):
	"""
	Applies a function to a list of arguments in parallel.

	A single thread is created for each argument. If an argument in the list of
	arguments is iterable, it will be assumed that it is a list of multiple
	arguments to the function.

	B{Example:}

	The first example will create three processes, the second example ten.

		>>> add = lambda x, y: x + y
		>>> print map(add, [(1, 2), (2, 3), (3, 4)])

		>>> square = lambda x: x * x
		>>> print map(square, range(10))

	@type  arguments: list
	@param arguments: a list which contains the arguments

	@type  result: list
	@param result: a list of return values
	"""

	def run(function, queue, idx, *args):
		"""
		A helper function for handling return values.
		"""

		queue.put((idx, function(*args)))

	processes = []

	# queue for storing return values
	queue = Queue(len(arguments))

	# create processes
	for idx, elem in enumerate(arguments):
		# make sure arguments are packed into tuples
		if not iterable(elem):
			args = (function, queue, idx, elem)
		else:
			args = [function, queue, idx]
			args.extend(elem)
			args = tuple(args)

		# store and start process
		processes.append(Process(target=run, args=args))
		processes[-1].start()

	# wait for processes to finish
	for process in processes:
		process.join()

	# wrap up results
	results = {}
	while not queue.empty():
		idx, result = queue.get()
		results[idx] = result

	return results.values()
