Parallel Map
============

A parallel implementation of the `map` function.


Getting started
---------------

A simple example:

	print mapp(lambda x: x + x, range(10))

This is how you pass multiple arguments to your function:

	print mapp(lambda x, y: x + y, range(10), range(10))

A for-loop can easily be parallelized using the following pattern.

	# sequential
	for i in range(10):
		do_something(i)

	# parallel
	def parfor(i):
		do_something(i)
	mapp(parfor, range(10))

To limit the number of processes, set `mapp.max_processes`.

	mapp.max_processes = 2
	mapp(parfor, range(10))

By default, the maximum number of forked processes is the number of available CPUs.

If you want to write to a variable which was defined outside the target function,
you have to make sure it is stored in *shared memory*. See the Python
documentation on the *multiprocessing* module for more information. To store a
NumPy array in shared memory, use the functions from the included *shmarray*
module.

	from shmarray import zeros

	values = zeros(10)

	def parfor(i):
		values[i] = i
	mapp(parfor, range(values.size))
