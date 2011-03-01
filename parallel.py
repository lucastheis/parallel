"""
Tools for simplified parallel processing.
"""

__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@tuebingen.mpg.de>'
__docformat__ = 'epytext'
__version__ = '0.0.2'

from multiprocessing import Process, Queue
from numpy import iterable

def map(function, arguments):
	"""
	Applies a function to a list of arguments in parallel.

	A single thread is created for each argument. Iterable arguments will be
	assumed to contain multiple arguments to the function.

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

	return [results[key] for key in sorted(results.keys())]



def chunkify(lst, num_chunks):
	"""
	Splits a list into chunks of equal size (or, if that's not possible, into
	chunks whose sizes are as equal as possible). The returned elements are in
	no particular order.

	@type  lst: list
	@param lst: a list of arbitrary elements

	@type  num_chunks: integer
	@param num_chunks: number of chunks

	@rtype: list
	@param: a list of lists (the chunks)
	"""

	return [lst[i::num_chunks] for i in range(num_chunks)]



def chunks(num_indices, num_chunks):
	"""
	Creates chunks of indices for use with L{map}.

	B{Example:}

		>>> def function(indices):
		>>>    for i in indices:
		>>>        do_something(i)
		>>> map(function, chunks(100, 4))

	@type  num_indices: integer
	@param num_indices: number of indices

	@type  num_chunks: integer
	@param num_chunks: number of chunks

	@rtype: list
	@param: a list of lists (the chunks)
	"""

	indices = range(num_indices)

	return [[chunk] for chunk in chunkify(indices, num_chunks)]
