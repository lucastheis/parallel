Tools for Parallel Processing in Python
=======================================

Basically a parallel implementation of the `map` function.

This implementation is simple and easy to use. It uses the multiprocessing module which
works well with classes and NumPy arrays, in contrast to many other solutions.

The ideal use case consists of an *embarassingly parallel* problem which can be
split up into a handful of tasks, each task requiring a lot of computations.
For problems with more fine-grained parallelism other solutions will probably
be more efficient. Also, this implementation only utilizes a single machine.


Getting started
---------------

Here's a simple first example.

	f = lambda x: x * x
	print map(f, range(10))

If you want to pass multiple arguments to the function, use tuples or lists.

	g = lambda x, y: x + y
	print map(f, [[x, x + 1] for x in range(10)])

A for-loop can easily be parallelized using the following pattern.

	# sequential
	for i in range(num_tasks):
		do_something(i)

	# parallel
	def parfor(i):
		do_something(i)
	map(parfor, range(num_tasks))

The easiest way to limit the number of forked processes is to set the argument
`max_processes`.

	map(function, range(10), max_processes=2)

By default, the maximum number of forked processes is the number of available
CPUs. You can change this default value by setting `map.max_processes`.

If you want to write to a variable which was defined outside of the function,
you have to make sure it is stored in *shared memory*. See the Python
documentation on the *multiprocessing* module for more information.  To store a
NumPy array in shared memory, use the functions from the included *shmarray*
module.

	from shmarray import zeros

	values = zeros(10)

	def parfor(i):
		values[i] = i
	map(parfor, range(values.size))


Requirements
------------

This implementation has been tested with

* Python >= 2.6.6
* NumPy >= 1.5.1

but older versions will probably also work.
